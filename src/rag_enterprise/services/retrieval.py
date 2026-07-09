from dataclasses import dataclass, field

from rag_enterprise.services.rbac import Principal, build_vector_filter


@dataclass(frozen=True)
class RetrievalResult:
    query: str
    metadata_filter: dict[str, object]
    chunks: list[dict[str, object]] = field(default_factory=list)


async def retrieve_context(query: str, user_roles: list[str]) -> RetrievalResult:
    principal = Principal(user_id="unknown", roles=user_roles, groups=user_roles)
    metadata_filter = build_vector_filter(principal)
    return RetrievalResult(query=query, metadata_filter=metadata_filter, chunks=[])
