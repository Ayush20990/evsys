"""Agent-loop benchmark: capture the search queries an LLM issues while actually
working a task, instead of asking it to imagine them up front.

The primary benchmark (src/query_level_workflow_evaluation.py) asks Gemini, in one
shot, to predict the queries an agent *would* issue for a task. That prediction is
static: it never sees a search result, so it can't react to one. This script runs a
real tool-calling loop instead -- the model is given the task and two tools, and
whatever queries it issues while genuinely trying to make progress are what we record.

Execution is mocked by default. A tool runs for real only when BOTH conditions hold,
checked against Composio itself rather than guessed from slug names:

  * the tool carries Composio's `readOnlyHint` tag (so it cannot write), AND
  * its toolkit has an ACTIVE connected account under this USER_ID (so it can succeed)

Everything else -- writes, and reads on unconnected toolkits -- gets a schema-conformant
mock built from the tool's declared output_parameters. The mock is also the fallback when
a real read fails for infrastructure reasons, so no path can strand the agent.

The second condition matters more than it looks. A real read against an unconnected
toolkit yields no useful signal -- just "No active connection", whose error text tells the
caller to go find COMPOSIO_MANAGE_CONNECTIONS. The agent obeys, cannot satisfy it, and
abandons the task; in run 1 that consumed 21% of all queries and derailed every task.
Hence infrastructure failures (auth, scope, rate limit, 5xx) never reach the agent, while
semantic failures (404, bad id, validation) do -- only the latter say anything about
whether the tool was the right choice.

One consequence of using real accounts: they are not the accounts these tasks were
written against, so correct tools frequently return empty. The agent is told this
explicitly, and empty reads are flagged in the trace, so a "no data here" result is not
mistaken for "wrong tool" either by the agent or during analysis.

The mock deliberately succeeds on any syntactically valid call. It cannot know that a
tool is the *wrong* tool without consulting the ground truth we're evaluating against,
and consulting it would leak the answer key into trace generation -- the agent would be
corrected by an oracle it would never have in production. The cost of that choice is
that wrong-tool picks don't trigger self-correction, so recovery queries are
undersampled on the write path. Read-path recovery is genuine, because those failures
are real.

Nothing here writes to a connected account.
"""
from __future__ import annotations

import json, os, re, sys, time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from composio import Composio
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-3.5-flash-lite"
GEMINI_RPM = 15
USER_ID = "agent-loop-eval-user"

NUM_TASKS = 10
MAX_STEPS = 36          # was 18; 7 of 10 tasks truncated at 18, capping session recall
MAX_TOOL_CALLS = 40     # hard ceiling on total calls per task

ROOT = Path(__file__).resolve().parent
USE_CASES_FILE = ROOT.parent / "src" / "top-100-eval-use-cases.md"
TRACE_DIR = ROOT / "traces"
TOOL_META_CACHE = ROOT / "tool_metadata_cache.json"
QUERIES_PATH = ROOT / "agent_queries.json"
REPORT_PATH = ROOT / "summary_report.md"

READ_ONLY_TAG = "readOnlyHint"

# A query that is just a tool slug the agent already saw in an earlier response is not
# discovery -- search returns it by exact match, which tests lookup rather than
# retrieval. Flagged so scoring can exclude it; in the first two runs these were 11% of
# queries and inflated recall by 1-2 points.
SLUG_QUERY = re.compile(r"^[A-Z][A-Z0-9]*(_[A-Z0-9]+){2,}$")

# Failures about the CONNECTION rather than about the tool choice. These must never reach
# the agent: they carry no information about whether it picked the right tool, and
# Composio's connection error additionally tells the caller to go find
# COMPOSIO_MANAGE_CONNECTIONS, which is what wrecked run 1.
INFRASTRUCTURE_ERROR = re.compile(
    r"no active connection|not authenticated|unauthoriz|forbidden|invalid[_ ]grant"
    r"|token.{0,20}expir|expired.{0,20}token|rate.?limit|too many requests"
    r"|\b401\b|\b403\b|\b429\b|\b5\d{2}\b|timed? ?out|connection reset",
    re.I,
)


def is_infrastructure_error(exc: Exception) -> bool:
    return bool(INFRASTRUCTURE_ERROR.search(f"{exc!r} {exc}"))


def is_empty_payload(payload: Any) -> bool:
    """Whether a successful read came back with no records.

    Tracked because the connected accounts are not the accounts these tasks were written
    against -- there is no "partner-operations database" in this Notion, no invoice mail in
    this inbox. A correct tool therefore returns empty, and an agent that reads that as
    "wrong tool" would emit a false recovery query. Recorded so those can be told apart
    from genuine recoveries during analysis.
    """
    if payload is None:
        return True
    if isinstance(payload, (list, str)):
        return len(payload) == 0
    if not isinstance(payload, dict):
        return False
    # Records usually arrive wrapped alongside status flags, e.g. Salesforce returns
    # {'done': True, 'records': [], 'totalSize': 0}. Judge on the record containers alone;
    # a truthy status flag next to an empty list must not read as "has data".
    containers = [v for k, v in payload.items()
                  if k in ("records", "items", "data", "results", "values", "messages",
                           "files", "rows", "entries", "response_data", "elements")]
    if containers:
        return all(is_empty_payload(v) for v in containers)
    meaningful = [v for k, v in payload.items()
                  if k not in ("successful", "error", "successfull", "done", "totalSize",
                               "has_more", "next_cursor", "object", "count")]
    if not meaningful:
        return True
    return all(v in (None, [], {}, "") for v in meaningful)


class QuotaExhaustedError(RuntimeError):
    """Raised when the LLM provider's quota is gone; retrying only burns wall-clock."""


def is_quota_error(exc: Exception) -> bool:
    text = repr(exc).lower()
    return any(marker in text for marker in ("resource_exhausted", "429", "quota", "rate limit"))


class RateLimiter:
    def __init__(self, rpm: float): self.interval, self.last = 60 / rpm, 0.0
    def wait(self):
        remaining = self.interval - (time.monotonic() - self.last)
        if remaining > 0: time.sleep(remaining)
        self.last = time.monotonic()


def retry(call, *args, max_retries: int = 4, base_delay: float = 2.0, **kwargs):
    for attempt in range(max_retries):
        try:
            return call(*args, **kwargs)
        except Exception as exc:
            if is_quota_error(exc):
                raise QuotaExhaustedError(str(exc)) from exc
            if attempt == max_retries - 1:
                raise
            time.sleep(base_delay * (2 ** attempt))


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def load_json(path: Path, fallback):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else fallback


def to_plain(value: Any) -> Any:
    """Composio returns pydantic models; the trace has to be JSON-serialisable."""
    if hasattr(value, "model_dump"): return to_plain(value.model_dump())
    if isinstance(value, dict): return {k: to_plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [to_plain(v) for v in value]
    return value


@dataclass
class UseCase:
    identifier: int
    task: str
    tools: list[str]
    description: str


def parse_use_cases(path: Path) -> list[UseCase]:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(\d+)\.\s+\*\*(.*?)\*\*\s*\n\s*-\s*Tools:\s*(.*?)\s*\n\s*-\s*Description:\s*(.*?)(?=\n\d+\.\s+\*\*|\Z)",
        re.DOTALL,
    )
    cases = []
    for ident, task, raw_tools, description in pattern.findall(text):
        tools = [item.strip() for item in raw_tools.replace("`", "").split(",") if item.strip()]
        cases.append(UseCase(int(ident), task.strip(), tools, description.strip()))
    if not cases:
        raise ValueError("No use cases parsed; inspect the Markdown format.")
    return cases


# --------------------------------------------------------------------------------------
# Tool metadata: the readOnlyHint tag is the safety gate, so it is fetched, not guessed.
# --------------------------------------------------------------------------------------

class ToolMetadata:
    def __init__(self, composio: Composio):
        self.composio = composio
        self.cache: dict[str, Any] = load_json(TOOL_META_CACHE, {})

    def get(self, slug: str) -> dict[str, Any] | None:
        if slug in self.cache:
            return self.cache[slug]
        try:
            tools = self.composio.tools.get_raw_composio_tools(tools=[slug])
        except Exception as exc:
            print(f"    [meta] lookup failed for {slug}: {exc!r}")
            return None
        record = None
        for tool in tools:
            if tool.slug == slug:
                toolkit = to_plain(tool.toolkit) or {}
                record = {
                    "slug": tool.slug,
                    "toolkit": (toolkit.get("slug") if isinstance(toolkit, dict) else str(toolkit)) or "",
                    "tags": list(tool.tags or []),
                    "output_parameters": to_plain(tool.output_parameters) or {},
                    "input_parameters": to_plain(tool.input_parameters) or {},
                }
                break
        self.cache[slug] = record
        save_json(TOOL_META_CACHE, self.cache)
        return record

    def is_read_only(self, slug: str) -> bool:
        record = self.get(slug)
        # Unknown tools are treated as writes. Failing closed is the only safe default
        # when the tag that authorises real execution could not be confirmed.
        return bool(record) and READ_ONLY_TAG in record.get("tags", [])

    def toolkit_of(self, slug: str) -> str:
        record = self.get(slug) or {}
        return (record.get("toolkit") or slug.split("_")[0]).lower()


def connected_toolkits(composio: Composio) -> tuple[set[str], dict[str, str]]:
    """Toolkits this USER_ID can actually execute against.

    Both filters below are load-bearing, and getting either wrong reintroduces the run-1
    derailment (a real call fails with "No active connection", whose error text tells the
    agent to go find COMPOSIO_MANAGE_CONNECTIONS, which it then does instead of the task).

    user_ids: Composio scopes connections per user/entity, but connected_accounts.list()
    is account-wide by default. An account connected under a different user_id -- one made
    by a dashboard flow, an MCP connector, or another script -- is listed here yet is
    invisible to session.execute(user_id=USER_ID).

    statuses: a connection can exist and still be EXPIRED or REVOKED. Only ACTIVE can
    actually execute.

    Returns the live toolkit slugs and their connection ids. The ids are required:
    a ToolRouter session only resolves a toolkit when the session is created with
    connected_accounts={slug: connection_id}. Passing toolkits=[...] is NOT sufficient --
    an ACTIVE, correctly-scoped connection still fails with "No active connection for
    toolkit(s) X in this session" unless its id is bound at session creation.
    """
    try:
        accounts = composio.connected_accounts.list(user_ids=[USER_ID], statuses=["ACTIVE"],
                                                    limit=100)
    except Exception as exc:
        print(f"[connections] lookup failed, mocking everything: {exc!r}")
        return set(), {}
    live, ids = set(), {}
    for account in accounts.items or []:
        toolkit = to_plain(getattr(account, "toolkit", None)) or {}
        slug = (toolkit.get("slug") if isinstance(toolkit, dict) else str(toolkit)) or ""
        if slug and getattr(account, "id", None):
            live.add(slug.lower())
            ids.setdefault(slug.lower(), account.id)
    return live, ids


def mock_from_schema(schema: dict[str, Any], depth: int = 0) -> Any:
    """Build a value that conforms to a JSON schema, so mocked output is structurally
    indistinguishable from the real thing even though the values are synthetic."""
    if depth > 4 or not isinstance(schema, dict):
        return None
    kind = schema.get("type")
    if isinstance(kind, list):
        kind = next((k for k in kind if k != "null"), None)
    if "enum" in schema and schema["enum"]:
        return schema["enum"][0]
    if kind == "object" or "properties" in schema:
        properties = schema.get("properties") or {}
        return {key: mock_from_schema(sub, depth + 1) for key, sub in list(properties.items())[:12]}
    if kind == "array":
        item = mock_from_schema(schema.get("items") or {}, depth + 1)
        return [item] if item is not None else []
    if kind == "boolean":
        return True
    if kind in ("integer", "number"):
        return 0
    return "<simulated>"


@dataclass
class TaskTrace:
    identifier: int
    task: str
    reference_tools: list[str]
    queries: list[dict[str, Any]] = field(default_factory=list)
    executions: list[dict[str, Any]] = field(default_factory=list)
    steps_used: int = 0
    stop_reason: str = ""
    final_message: str = ""
    error: str | None = None


class AgentSession:
    """Holds everything one task's loop needs, and records what the agent did."""

    def __init__(self, session, metadata: ToolMetadata, trace: TaskTrace,
                 connected: set[str]):
        self.session = session
        self.metadata = metadata
        self.trace = trace
        self.connected = connected
        self.calls = 0

    def search_tools(self, query: str, intent: str = "") -> dict[str, Any]:
        started = time.monotonic()
        try:
            response = self.session.execute("COMPOSIO_SEARCH_TOOLS", arguments={"query": query})
        except Exception as exc:
            self.trace.queries.append({"query": query, "intent": intent, "error": repr(exc)})
            return {"error": f"search failed: {exc!r}"}
        latency = time.monotonic() - started
        data = to_plain(getattr(response, "data", response)) or {}
        results = (data.get("results") or [{}])[0] if isinstance(data, dict) else {}
        primary = results.get("primary_tool_slugs") or []
        related = results.get("related_tool_slugs") or []
        plan = results.get("recommended_plan_steps") or []
        self.trace.queries.append({
            "query": query,
            "intent": intent,
            "primary_tool_slugs": primary,
            "related_tool_slugs": related,
            "latency_sec": round(latency, 3),
            "is_slug_lookup": bool(SLUG_QUERY.match(query.strip())),
        })
        print(f"    search: {query!r} -> {primary}")
        return {"primary_tool_slugs": primary, "related_tool_slugs": related,
                "recommended_plan_steps": plan[:6]}

    def execute_tool(self, tool_slug: str, arguments: dict[str, Any]) -> dict[str, Any]:
        read_only = self.metadata.is_read_only(tool_slug)
        toolkit = self.metadata.toolkit_of(tool_slug)
        live = toolkit in self.connected
        record = {"tool_slug": tool_slug, "arguments": arguments,
                  "read_only": read_only, "toolkit": toolkit, "toolkit_connected": live}
        if read_only and live:
            try:
                response = self.session.execute(tool_slug, arguments=arguments)
                payload = to_plain(getattr(response, "data", response))
                record["mode"] = "real"
                record["successful"] = True
                record["empty_result"] = is_empty_payload(payload)
                self.trace.executions.append(record)
                print(f"    exec[real] {tool_slug}"
                      + ("  (empty)" if record["empty_result"] else ""))
                return {"successful": True, "data": payload, "error": None}
            except Exception as exc:
                # Split real failures by what they say about the agent's CHOICE of tool.
                #
                # Infrastructure failures (expired token, revoked scope, rate limit) say
                # nothing about whether the tool was right, and their error text actively
                # misleads -- Composio's "No active connection" message instructs the
                # caller to go find COMPOSIO_MANAGE_CONNECTIONS, which derailed 21% of
                # run 1's queries. These fall through to the mock silently, which is also
                # the backup engine for any toolkit that is simply not connected.
                #
                # Semantic failures (404, bad id, validation) DO say something -- they are
                # the signal real execution exists to provide -- so they reach the agent.
                if is_infrastructure_error(exc):
                    record["mode"] = "real-infra-fallback"
                    record["error"] = repr(exc)[:300]
                    print(f"    exec[real->mock] {tool_slug}: infra error, mocking")
                else:
                    record["mode"] = "real-failed"
                    record["error"] = repr(exc)[:400]
                    self.trace.executions.append(record)
                    print(f"    exec[real-failed] {tool_slug}: {repr(exc)[:90]}")
                    return {"successful": False, "data": None, "error": repr(exc)[:400]}
        meta = self.metadata.get(tool_slug) or {}
        # Reject calls the real API would reject. This is a pure schema check against the
        # tool's declared required parameters -- it never consults the ground truth, so it
        # cannot leak the answer key. Without it the mock returns success for an argument-
        # less call to a create endpoint, and the agent proceeds believing it created
        # something.
        required = (meta.get("input_parameters") or {}).get("required") or []
        missing = [name for name in required if name not in arguments]
        if missing:
            record["mode"] = "mock-rejected"
            record["error"] = f"missing required parameters: {missing}"
            self.trace.executions.append(record)
            print(f"    exec[mock-reject] {tool_slug}: missing {missing}")
            return {"successful": False, "data": None,
                    "error": f"Missing required parameters: {', '.join(missing)}"}
        mocked = mock_from_schema(meta.get("output_parameters") or {})
        if not isinstance(mocked, dict):
            mocked = {"result": mocked}
        record["mode"] = "mocked"
        self.trace.executions.append(record)
        print(f"    exec[mock] {tool_slug}")
        return {"successful": True, "data": mocked.get("data", mocked), "error": None}


# Mirrors the one-shot DECOMPOSE_PROMPT in the primary benchmark, which gets well-formed
# queries out of this same model. Two lessons are baked in.
#
# First: ask for "concrete" and "specific", never for "short" or "one at a time". An
# earlier version said "issue one focused query" for "the single capability you need
# right now" and produced single-word searches ('email', 'workflow'). Stripping that
# guidance entirely did not help -- with no quality bar at all the queries stayed just as
# bare. Specificity and brevity are separate axes; the working prompt constrains the first
# and says nothing about the second.
#
# Second: require an `intent` sentence alongside the query. Articulating the capability in
# full is what anchors the query text -- it is the one structural difference between the
# prompt that works and the prompt that does not. Only `query` is ever sent to search;
# `intent` exists to make the model think before it searches.
SEARCH_DECLARATION = types.FunctionDeclaration(
    name="search_tools",
    description=(
        "Search the tool catalogue for a tool that performs a specific action or lookup "
        "this task requires. Searches the catalogue by meaning, so describe the capability "
        "concretely, the way you would describe it to a colleague."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "intent": types.Schema(
                type=types.Type.STRING,
                description=("One precise sentence describing exactly what capability you need "
                             "right now, and in which application."),
            ),
            "query": types.Schema(
                type=types.Type.STRING,
                description=("The search query. A concrete, realistic description of that "
                             "capability. Do not use internal tool or API names."),
            ),
        },
        required=["intent", "query"],
    ),
)

EXECUTE_DECLARATION = types.FunctionDeclaration(
    name="execute_tool",
    description="Run one tool by its exact slug, with its arguments, to make progress on the task.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "tool_slug": types.Schema(type=types.Type.STRING, description="Exact tool slug."),
            "arguments_json": types.Schema(type=types.Type.STRING,
                                           description="JSON object of arguments for the tool."),
        },
        required=["tool_slug", "arguments_json"],
    ),
)

SYSTEM_PROMPT = """You are an autonomous agent completing a real workplace task using external
application tools. You do NOT know what tools or APIs exist -- your only way to find one is
to call search_tools once you know what you need.

How to work:
- Work out what the task requires, then search for a tool for each genuine, distinct
  sub-intent, in the order you need them.
- Search the way you would describe the capability to a colleague: name the application and
  the specific action or lookup you need. The catalogue matches on meaning, so a bare word
  like "email" finds the wrong application entirely.
- After each search, look at what came back, pick the tool that fits, and call execute_tool
  with its real arguments.
- Use what each result actually gives you to decide your next move. If a call fails
  because the tool was the wrong choice, search for a better-suited tool.
- The accounts you are working against are NOT the accounts this task was written for.
  The specific spreadsheet, board, database or message the task mentions will usually not
  exist here, so correct tools will often return empty results or "not found". That means
  the data is absent, NOT that you picked the wrong tool. When it happens, treat the step
  as done and move on to the next part of the task -- do not search for a replacement tool
  and do not retry the same lookup with different ids.
- Work through the whole task, including any verification the task asks for.
- When the task is complete or you genuinely cannot proceed, reply with a short plain-text
  summary of what you did and stop calling tools.

Do not invent tool slugs, and never search for a slug you have already seen -- search for
capabilities, and execute only slugs a search actually returned."""


def run_task(client, session, metadata: ToolMetadata, limiter: RateLimiter,
             case: UseCase, connected: set[str]) -> TaskTrace:
    trace = TaskTrace(identifier=case.identifier, task=case.task, reference_tools=case.tools)
    agent = AgentSession(session, metadata, trace, connected)

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[types.Tool(function_declarations=[SEARCH_DECLARATION, EXECUTE_DECLARATION])],
        temperature=0.4,
    )
    contents = [types.Content(role="user", parts=[types.Part(text=f"Task:\n{case.task}")])]

    for step in range(1, MAX_STEPS + 1):
        trace.steps_used = step
        def call():
            limiter.wait()
            return client.models.generate_content(model=GEMINI_MODEL, contents=contents,
                                                  config=config)
        try:
            response = retry(call)
        except QuotaExhaustedError:
            trace.stop_reason, trace.error = "quota exhausted", "gemini quota exhausted"
            return trace
        except Exception as exc:
            trace.stop_reason, trace.error = "model error", repr(exc)[:400]
            return trace

        candidate = (response.candidates or [None])[0]
        if candidate is None or candidate.content is None:
            trace.stop_reason = "empty model response"
            return trace
        contents.append(candidate.content)

        calls = [part.function_call for part in (candidate.content.parts or [])
                 if getattr(part, "function_call", None)]
        if not calls:
            trace.stop_reason = "agent finished"
            trace.final_message = "".join(part.text or "" for part in (candidate.content.parts or []))
            return trace

        replies = []
        for function_call in calls:
            agent.calls += 1
            if agent.calls > MAX_TOOL_CALLS:
                trace.stop_reason = "tool-call ceiling reached"
                return trace
            arguments = dict(function_call.args or {})
            if function_call.name == "search_tools":
                result = agent.search_tools(str(arguments.get("query", "")).strip(),
                                            str(arguments.get("intent", "")).strip())
            elif function_call.name == "execute_tool":
                try:
                    parsed = json.loads(arguments.get("arguments_json") or "{}")
                    if not isinstance(parsed, dict):
                        parsed = {}
                except json.JSONDecodeError:
                    parsed = {}
                result = agent.execute_tool(str(arguments.get("tool_slug", "")).strip(), parsed)
            else:
                result = {"error": f"unknown function {function_call.name}"}
            replies.append(types.Part.from_function_response(name=function_call.name,
                                                             response=result))
        contents.append(types.Content(role="user", parts=replies))

    trace.stop_reason = "step ceiling reached"
    return trace


def write_report(traces: list[TaskTrace]) -> None:
    import statistics
    done = [t for t in traces if not t.error]
    all_queries = [q for t in traces for q in t.queries]
    counts = [len(t.queries) for t in traces if t.queries]
    executions = [e for t in traces for e in t.executions]
    real = [e for e in executions if e.get("mode") == "real"]
    real_failed = [e for e in executions if e.get("mode") == "real-failed"]
    mocked = [e for e in executions if e.get("mode") == "mocked"]

    md = [
        "# Agent-Loop Query Benchmark\n",
        "## Method",
        "Each task from `top-100-eval-use-cases.md` is handed to a Gemini agent with two tools: "
        "`search_tools` (the real `COMPOSIO_SEARCH_TOOLS`) and `execute_tool`. The agent is told "
        "nothing about which tools exist -- it has to discover them by searching, then react to "
        "what comes back. Every query it issues is recorded. Query count is emergent: no cap, no "
        "formula, the agent stops searching when it stops needing tools.\n",
        "Execution is mocked unless a tool both carries Composio's `readOnlyHint` tag and belongs "
        "to a toolkit with a live connected account. Mocks are generated from the tool's declared "
        "`output_parameters`, so they are structurally indistinguishable from a real response. "
        "With no accounts connected, every call is mocked and no external API is touched.\n",
        "## Summary",
        f"- **Tasks attempted:** {len(traces)}",
        f"- **Tasks completed without error:** {len(done)}",
        f"- **Total queries captured:** {len(all_queries)}",
    ]
    if counts:
        md.extend([
            f"- **Queries per task:** mean {statistics.mean(counts):.1f}, "
            f"median {statistics.median(counts):.0f}, min {min(counts)}, max {max(counts)}",
        ])
    md.extend([
        f"- **Tool executions:** {len(executions)} "
        f"({len(real)} real, {len(real_failed)} real-failed, {len(mocked)} mocked)",
    ])

    md.append("\n## Per-task breakdown\n")
    md.append("| Task | Queries | Executions | Steps | Stop reason |")
    md.append("|---|---:|---:|---:|---|")
    for t in traces:
        md.append(f"| {t.identifier} | {len(t.queries)} | {len(t.executions)} | "
                  f"{t.steps_used} | {t.error or t.stop_reason} |")

    md.append("\n## Queries the agent actually issued\n")
    for t in traces:
        md.append(f"### Task {t.identifier}")
        md.append(f"*{t.task[:200]}{'...' if len(t.task) > 200 else ''}*\n")
        if not t.queries:
            md.append("_(no queries issued)_\n")
            continue
        for index, q in enumerate(t.queries, 1):
            if q.get("error"):
                md.append(f"{index}. `{q['query']}` — **search error**")
            else:
                primary = ", ".join(q.get("primary_tool_slugs") or []) or "(none)"
                md.append(f"{index}. `{q['query']}` → `{primary}`")
        md.append("")

    REPORT_PATH.write_text("\n".join(md) + "\n", encoding="utf-8")


def main() -> None:
    if not COMPOSIO_API_KEY or not GEMINI_API_KEY:
        raise ValueError("Set COMPOSIO_API_KEY and GEMINI_API_KEY in .env")
    TRACE_DIR.mkdir(parents=True, exist_ok=True)

    cases = parse_use_cases(USE_CASES_FILE)[:NUM_TASKS]
    composio = Composio(api_key=COMPOSIO_API_KEY)
    client = genai.Client(api_key=GEMINI_API_KEY)
    metadata = ToolMetadata(composio)
    limiter = RateLimiter(GEMINI_RPM)
    # connected_accounts binding is what actually makes a live connection callable; see
    # connected_toolkits(). Without it every real execution 400s with "No active
    # connection ... in this session" despite the account being ACTIVE.
    session = (composio.create(user_id=USER_ID, connected_accounts=account_ids)
               if account_ids else composio.create(user_id=USER_ID))

    connected, account_ids = connected_toolkits(composio)
    print(f"[connections] live toolkits: {sorted(connected) or 'none -- every tool will be mocked'}")

    traces: list[TaskTrace] = []
    for index, case in enumerate(cases, 1):
        print(f"\n[task {index}/{len(cases)}] #{case.identifier}: {case.task[:80]}...")
        try:
            trace = run_task(client, session, metadata, limiter, case, connected)
        except QuotaExhaustedError as exc:
            print(f"  quota exhausted, stopping early: {exc}")
            break
        traces.append(trace)
        save_json(TRACE_DIR / f"task-{case.identifier:03d}.json", trace.__dict__)
        print(f"  -> {len(trace.queries)} queries, {len(trace.executions)} executions "
              f"({trace.error or trace.stop_reason})")

    save_json(QUERIES_PATH, {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "config": {"model": GEMINI_MODEL, "num_tasks": NUM_TASKS, "max_steps": MAX_STEPS},
        "tasks": [{"identifier": t.identifier, "task": t.task,
                   "reference_tools": t.reference_tools,
                   "queries": [q["query"] for q in t.queries]} for t in traces],
    })
    write_report(traces)
    print(f"\nWrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
