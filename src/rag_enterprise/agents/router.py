from dataclasses import dataclass


@dataclass(frozen=True)
class RouteDecision:
    name: str
    next_action: str


async def route_request(message: str) -> RouteDecision:
    normalized = message.lower()
    if any(keyword in normalized for keyword in ("calculate", "compute", "sum", "table")):
        return RouteDecision(name="analyst", next_action="run_code_analysis")
    if any(keyword in normalized for keyword in ("find", "search", "document", "policy", "jira")):
        return RouteDecision(name="rag", next_action="retrieve_relevant_chunks")
    return RouteDecision(name="clarify", next_action="ask_for_more_context")
