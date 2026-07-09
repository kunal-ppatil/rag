from dataclasses import dataclass, field
import re

from rag_enterprise.services.corpus import KnowledgeDocument, load_corpus
from rag_enterprise.services.rbac import Principal, build_vector_filter


@dataclass(frozen=True)
class RetrievalResult:
    query: str
    metadata_filter: dict[str, object]
    chunks: list[dict[str, object]] = field(default_factory=list)


def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 2}


def _score_document(query_tokens: set[str], document: KnowledgeDocument) -> int:
    document_tokens = _tokenize(f"{document.title} {document.text}")
    return len(query_tokens & document_tokens)


def _format_chunk(document: KnowledgeDocument, score: int) -> dict[str, object]:
    return {
        "document_id": document.document_id,
        "title": document.title,
        "text": document.text,
        "allowed_groups": document.allowed_groups,
        "score": score,
    }


async def retrieve_context(query: str, user_roles: list[str]) -> RetrievalResult:
    principal = Principal(user_id="unknown", roles=user_roles, groups=user_roles)
    metadata_filter = build_vector_filter(principal)
    query_tokens = _tokenize(query)
    candidates: list[dict[str, object]] = []

    for document in load_corpus():
        if not set(principal.groups).intersection(document.allowed_groups):
            continue
        score = _score_document(query_tokens, document)
        if score > 0:
            candidates.append(_format_chunk(document, score))

    candidates.sort(key=lambda item: item["score"], reverse=True)
    return RetrievalResult(query=query, metadata_filter=metadata_filter, chunks=candidates[:3])

