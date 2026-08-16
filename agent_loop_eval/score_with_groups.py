"""Score an agent-loop run with requirement groups and an LLM judge.

Union recall over a flat reference list -- what the runner reports -- is wrong in three
distinct ways, all of them measured rather than assumed. The first two make it too harsh,
the third makes it too generous, so the errors do not cancel and the direction of the bias
varies by task.

  * Too harsh on SUPERSET NOISE. The `Tools:` lists in top-100-eval-use-cases.md are
    execution logs of past agent sessions, not requirement sets: all 100 descriptions
    narrate a past run, #32 says outright that "the agent repeatedly used tool search to
    find tools", 13 task texts describe attempts rather than successes, and 51 of 100
    contain three or more same-toolkit same-verb tools (one session trying several ways to
    read mail). Auth probes and `*_PROXY_EXECUTE` escape hatches alone are 3.4% of all
    1008 entries. Flat recall penalises search for not returning things no sensible query
    would ever target.

  * Too harsh on VALID ALTERNATIVES. 58% of run-5 executions used a tool outside the
    reference list, and inspection showed many were correct: task 8 needs video
    transcripts and its list contains only GOOGLEDOCS_INSERT_TEXT_ACTION, so
    FIREFLIES_GET_TRANSCRIPTS is right and uncredited; task 9 asks for downloadable
    presentation content and its list has no presentation tool, so GAMMA_GENERATE_GAMMA
    is right and uncredited.

  * Too GENEROUS on INCOMPLETE lists. A logged list only names tools the past session
    called, so any capability it solved outside Composio -- or never solved at all -- is
    absent, and flat recall cannot see the gap. Task 3 needs four capabilities and its
    list covers three: nothing in it modifies a workbook, because that session did the
    edit in a sandbox. Flat recall scores 4/4 = 100% while a real requirement went unmet.
    Task 8 is starker: four capabilities, one listed tool, flat recall 1/1 = 100%.

Grouping is derived from the TASK rather than from the log, so it is immune to all three.

This scorer mirrors the primary benchmark's two-stage approach, with one deliberate
difference: there, requirement groups attach to each decomposed query, because the
decomposition produces them. Here queries are emergent and often exploratory, so groups
attach to the TASK. That also makes the headline number answer the question worth asking
-- was this task achievable with what search returned -- rather than scoring each query in
isolation.

  Stage A  task + its reference tools (with real descriptions) -> requirement groups.
           Alternatives share a group; distinct capabilities get separate groups; superset
           noise is dropped. Grounded in the reference pool, so no slug can be invented.
  Stage B  strict recall = groups satisfied by any tool the session actually surfaced.
  Stage C  judged recall = Stage B, plus unmet groups re-checked against the tools search
           really returned. Vendor-scoped, so a same-capability tool from the wrong vendor
           cannot be credited.

Reads existing traces, so it costs no agent quota and can re-score any completed run.

    python score_with_groups.py run5_real_reads_20tasks
"""
from __future__ import annotations

import json, os, sys
from pathlib import Path
from typing import Any

from composio import Composio
from dotenv import load_dotenv
from google import genai

from agent_loop_evaluation import (
    COMPOSIO_API_KEY, GEMINI_API_KEY, GEMINI_MODEL, GEMINI_RPM, ROOT,
    QuotaExhaustedError, RateLimiter, ToolMetadata, load_json, retry, save_json,
)

DESCRIPTION_CHARS = 300
MAX_GROUPS = 12          # complex tasks legitimately need more; 8 rejected 3 of 100
MAX_TOOLS_PER_GROUP = 8


def strip_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0]
    start, end = text.find("{"), text.rfind("}")
    return text[start:end + 1] if start >= 0 and end > start else text


GROUP_PROMPT = '''You are defining what a task genuinely REQUIRES, for evaluating a tool-search engine.

Task:
{task}

Tools that a past agent session logged while working this task. This is a LOG, not a
specification: it includes tools called during exploration, retries, dead ends, auth
checks, and generic API passthroughs. Judge each on its description, not its name.
{catalog}

Group the tools into REQUIREMENT GROUPS:
- One group per distinct capability the task genuinely needs.
- Tools that could EACH independently satisfy the same need go in the SAME group -- they
  are alternatives, and finding any one of them is a success.
- Distinct capabilities the task needs go in SEPARATE groups.
- DROP tools that the task does not actually require: auth or identity probes
  (test auth, get profile, list granted scopes, get current time), generic
  *_PROXY_EXECUTE passthroughs, and near-duplicate variants already covered by a group.
- Do not invent slugs. Use only the slugs listed above.
- A capability the task clearly needs but which NO listed tool provides should still be a
  group, with an empty slug list and a purpose describing the need.

Return exactly this JSON:
{{"groups":[{{"purpose":"short phrase for the capability","acceptable_tool_slugs":["..."]}}],
  "dropped":[{{"slug":"...","why":"probe | proxy | duplicate | not required"}}]}}

Aim for the smallest set of groups that honestly covers the task. Most tasks need 2-6.
'''


JUDGE_PROMPT = '''Decide whether a tool-search engine actually delivered a needed capability.

Task the agent was working:
{task}

The capability that was NOT matched by any expected tool:
  {purpose}
  (tools that would have been accepted: {expected})

Tools the search engine actually returned across the session, with descriptions:
{returned}

Question: does any returned tool GENUINELY provide the capability described above?

Rules:
- Judge on the description, not the name.
- The tool must do the actual job, not merely relate to the same area. A tool that lists
  records does not satisfy a need to update one.
- VENDOR SCOPE: if the task names a specific application, only a tool from that same
  application counts. A Stripe payment tool never satisfies a HubSpot payment need.
- If the capability is only partly covered, answer false.

Return exactly this JSON:
{{"satisfied": true or false, "slug": "the tool that satisfies it, or null", "why": "one sentence"}}
'''


def call_gemini(client, limiter: RateLimiter, prompt: str) -> dict[str, Any] | None:
    def once():
        limiter.wait()
        return (client.models.generate_content(model=GEMINI_MODEL, contents=prompt).text or "").strip()
    try:
        return json.loads(strip_json(retry(once, max_retries=4, base_delay=3.0)))
    except QuotaExhaustedError:
        raise
    except Exception as exc:
        print(f"    [gemini] failed: {exc!r}")
        return None


def describe(metadata: ToolMetadata, slugs: list[str]) -> str:
    records = metadata.get_many(slugs)
    lines = []
    for slug in slugs:
        record = records.get(slug)
        text = (record or {}).get("description", "") or "(no description available)"
        lines.append(f"- {slug}: {text[:DESCRIPTION_CHARS]}")
    return "\n".join(lines)


def validate_groups(payload: Any, allowed: set[str]) -> str | None:
    """Reject only what makes a task unscoreable; repair what is merely untidy.

    An over-long alternatives list is not a correctness problem -- a 25-tool task can
    legitimately have eight interchangeable tools for one capability -- so it is truncated
    rather than rejected. Rejecting cost two whole tasks (11 and 16, the two largest) on
    the first run, which is exactly the wrong trade: the biggest tasks are the ones whose
    scores matter most. An invented slug IS rejected, because a group referencing a tool
    outside the pool cannot be scored against what search returned.
    """
    if not isinstance(payload, dict) or not isinstance(payload.get("groups"), list):
        return "missing groups list"
    groups = payload["groups"]
    if not groups or len(groups) > MAX_GROUPS:
        return f"group count {len(groups)} outside 1..{MAX_GROUPS}"
    for group in groups:
        if not isinstance(group, dict) or not str(group.get("purpose", "")).strip():
            return "group missing purpose"
        slugs = group.get("acceptable_tool_slugs")
        if not isinstance(slugs, list):
            return "group slug list is not a list"
        if not set(slugs) <= allowed:
            return f"invented slug: {sorted(set(slugs) - allowed)[:3]}"
        if len(slugs) > MAX_TOOLS_PER_GROUP:
            print(f"    [groups] truncating '{group['purpose'][:40]}' "
                  f"from {len(slugs)} alternatives to {MAX_TOOLS_PER_GROUP}")
            group["acceptable_tool_slugs"] = slugs[:MAX_TOOLS_PER_GROUP]
    return None


def score_run(run_dir: Path) -> None:
    composio = Composio(api_key=COMPOSIO_API_KEY)
    client = genai.Client(api_key=GEMINI_API_KEY)
    metadata = ToolMetadata(composio)
    limiter = RateLimiter(GEMINI_RPM)

    cache_path = run_dir / "group_cache.json"
    cache = load_json(cache_path, {})
    rows: list[dict[str, Any]] = []

    traces = sorted(run_dir.glob("task-*.json"), key=lambda p: int(p.stem.split("-")[-1]))
    for path in traces:
        trace = json.loads(path.read_text(encoding="utf-8"))
        task_id = str(trace["identifier"])
        reference = list(dict.fromkeys(trace["reference_tools"]))
        surfaced, primary_only = set(), set()
        for query in trace["queries"]:
            p = set(query.get("primary_tool_slugs") or [])
            surfaced |= p | set(query.get("related_tool_slugs") or [])
            primary_only |= p

        # ---- Stage A: requirement groups ------------------------------------------------
        if task_id in cache:
            payload = cache[task_id]
        else:
            print(f"[groups] task {task_id}")
            payload = call_gemini(client, limiter, GROUP_PROMPT.format(
                task=trace["task"], catalog=describe(metadata, reference)))
            rejection = "generation error" if payload is None else validate_groups(payload, set(reference))
            if rejection:
                print(f"    rejected: {rejection}")
                payload = None
            cache[task_id] = payload
            save_json(cache_path, cache)
        if not payload:
            rows.append({"task": trace["identifier"], "error": "no groups"})
            continue

        groups = payload["groups"]
        met, unmet = [], []
        for group in groups:
            hit = sorted(set(group["acceptable_tool_slugs"]) & surfaced)
            (met if hit else unmet).append({**group, "matched": hit})

        # ---- Stage C: judge only the groups nothing expected satisfied -------------------
        judged = []
        extra = sorted(surfaced - set(reference))
        for group in unmet:
            if not extra:
                judged.append({**group, "judged": False, "why": "search returned no other candidate"})
                continue
            verdict = call_gemini(client, limiter, JUDGE_PROMPT.format(
                task=trace["task"], purpose=group["purpose"],
                expected=", ".join(group["acceptable_tool_slugs"]) or "(none listed)",
                returned=describe(metadata, extra[:25])))
            ok = bool(verdict and verdict.get("satisfied"))
            judged.append({**group, "judged": ok,
                           "judged_slug": (verdict or {}).get("slug"),
                           "why": (verdict or {}).get("why", "")})

        total = len(groups)
        strict = len(met)
        judged_ok = strict + sum(1 for g in judged if g["judged"])
        primary_hits = sum(1 for g in groups if set(g["acceptable_tool_slugs"]) & primary_only)
        rows.append({
            "task": trace["identifier"], "groups": total,
            "strict": strict, "judged": judged_ok, "primary": primary_hits,
            "flat_union": len(set(reference) & surfaced), "flat_total": len(reference),
            "dropped": len(payload.get("dropped") or []),
            "met": met, "unmet": judged,
            "queries": len(trace["queries"]),
        })
        print(f"  task {trace['identifier']:>2}: groups {strict}/{total} strict, "
              f"{judged_ok}/{total} judged  (flat was {len(set(reference)&surfaced)}/{len(reference)})")

    write_report(run_dir, rows)


def write_report(run_dir: Path, rows: list[dict[str, Any]]) -> None:
    valid = [r for r in rows if "error" not in r]
    G = sum(r["groups"] for r in valid)
    S = sum(r["strict"] for r in valid)
    J = sum(r["judged"] for r in valid)
    P = sum(r["primary"] for r in valid)
    FU = sum(r["flat_union"] for r in valid)
    FT = sum(r["flat_total"] for r in valid)
    dropped = sum(r["dropped"] for r in valid)

    md = [f"# Group-based scoring — `{run_dir.name}`", "",
          "Requirement groups replace the flat reference list: alternatives share a group, distinct",
          "capabilities get separate groups, and logged-but-unnecessary tools are dropped. A group is",
          "satisfied if search surfaced ANY tool in it. See the module docstring for why flat recall",
          "is biased in both directions.", "",
          "## Summary", "",
          f"- **Tasks scored:** {len(valid)}",
          f"- **Requirement groups:** {G} (from {FT} logged tools; {dropped} dropped as not required)",
          f"- **Strict group recall:** {S}/{G} ({100*S/G:.0f}%)" if G else "",
          f"- **Judged group recall:** {J}/{G} ({100*J/G:.0f}%)" if G else "",
          f"- **Groups hit in `primary`:** {P}/{G} ({100*P/G:.0f}%)" if G else "",
          f"- **Flat union recall, for comparison:** {FU}/{FT} ({100*FU/FT:.0f}%)" if FT else "",
          "",
          "Judged recall is the honest headline: strict recall still misses valid alternatives that",
          "search returned but the logged list never named.", "",
          "## Per task", "",
          "| Task | Queries | Groups | Strict | Judged | Primary | Flat union | Dropped |",
          "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in valid:
        md.append(f"| {r['task']} | {r['queries']} | {r['groups']} | "
                  f"{r['strict']}/{r['groups']} | {r['judged']}/{r['groups']} | "
                  f"{r['primary']}/{r['groups']} | {r['flat_union']}/{r['flat_total']} | {r['dropped']} |")

    md += ["", "## Capabilities search never delivered", "",
           "Groups unmet even after judging — these are the real retrieval failures.", ""]
    for r in valid:
        hard = [g for g in r["unmet"] if not g["judged"]]
        if not hard:
            continue
        md.append(f"**Task {r['task']}**")
        for g in hard:
            expected = ", ".join(f"`{s}`" for s in g["acceptable_tool_slugs"]) or "_(nothing listed provided it)_"
            md.append(f"- {g['purpose']} — expected {expected}")
            if g.get("why"):
                md.append(f"  - judge: {g['why']}")
        md.append("")

    md += ["## Alternatives credited by the judge", "",
           "Groups no expected tool matched, but a tool search actually returned did the job.",
           "Each of these is a flat-recall false negative.", ""]
    any_credited = False
    for r in valid:
        credited = [g for g in r["unmet"] if g["judged"]]
        if not credited:
            continue
        any_credited = True
        md.append(f"**Task {r['task']}**")
        for g in credited:
            md.append(f"- {g['purpose']} — satisfied by `{g.get('judged_slug')}`")
            if g.get("why"):
                md.append(f"  - {g['why']}")
        md.append("")
    if not any_credited:
        md.append("_None._")

    path = run_dir / "group_scoring_report.md"
    path.write_text("\n".join(x for x in md if x is not None) + "\n", encoding="utf-8")
    save_json(run_dir / "group_scores.json", rows)
    print(f"\nwrote {path}")
    if G:
        print(f"strict {S}/{G} ({100*S/G:.0f}%)  judged {J}/{G} ({100*J/G:.0f}%)  "
              f"primary {P}/{G} ({100*P/G:.0f}%)  [flat union was {FU}/{FT} = {100*FU/FT:.0f}%]")


if __name__ == "__main__":
    if not COMPOSIO_API_KEY or not GEMINI_API_KEY:
        raise SystemExit("Set COMPOSIO_API_KEY and GEMINI_API_KEY in .env")
    target = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "run5_real_reads_20tasks")
    if not target.is_dir():
        raise SystemExit(f"no such run directory: {target}")
    score_run(target)
