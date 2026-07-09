from rag_enterprise.services.retrieval import RetrievalResult, retrieve_context


async def answer_with_retrieval(query: str, user_roles: list[str]) -> RetrievalResult:
    return await retrieve_context(query=query, user_roles=user_roles)
