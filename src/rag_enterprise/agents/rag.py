import json

import httpx

from rag_enterprise.core.config import get_settings
from rag_enterprise.services.retrieval import RetrievalResult, retrieve_context


def _compose_answer(query: str, retrieval: RetrievalResult) -> str:
    if not retrieval.chunks:
        return (
            "I could not find a matching document in the local knowledge base for your query. "
            "Try asking about HR policy, finance expenses, or engineering releases."
        )

    best_chunk = retrieval.chunks[0]
    return (
        f"Based on {best_chunk['title']}, the answer to '{query}' is: {best_chunk['text']}"
    )


def _build_context(retrieval: RetrievalResult) -> str:
    if not retrieval.chunks:
        return "No relevant documents were retrieved from the local knowledge base."

    lines: list[str] = []
    for chunk in retrieval.chunks:
        lines.append(f"Title: {chunk['title']}")
        lines.append(f"Document ID: {chunk['document_id']}")
        lines.append(f"Text: {chunk['text']}")
        lines.append("")
    return "\n".join(lines).strip()


async def _answer_with_openai(query: str, retrieval: RetrievalResult) -> str:
    settings = get_settings()
    prompt = (
        "You are an enterprise RAG assistant. Answer only from the provided context. "
        "If the context is insufficient, say you cannot determine the answer from the available documents."
    )
    context = _build_context(retrieval)
    payload = {
        "model": settings.openai_model,
        "messages": [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": f"Question: {query}\n\nContext:\n{context}",
            },
        ],
        "temperature": 0.2,
    }

    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{settings.openai_api_base.rstrip('/')}/chat/completions",
            headers=headers,
            content=json.dumps(payload),
        )
        response.raise_for_status()
        data = response.json()

    return data["choices"][0]["message"]["content"].strip()


async def answer_with_retrieval(query: str, user_roles: list[str]) -> dict[str, object]:
    retrieval = await retrieve_context(query=query, user_roles=user_roles)
    settings = get_settings()
    if settings.llm_provider.lower() == "openai" and settings.openai_api_key:
        answer = await _answer_with_openai(query, retrieval)
    else:
        answer = _compose_answer(query, retrieval)

    return {
        "query": query,
        "answer": answer,
        "sources": [
            {
                "document_id": chunk["document_id"],
                "title": chunk["title"],
                "score": chunk["score"],
            }
            for chunk in retrieval.chunks
        ],
        "metadata_filter": retrieval.metadata_filter,
    }

