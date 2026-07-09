from collections.abc import AsyncIterator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from rag_enterprise.agents.rag import answer_with_retrieval
from rag_enterprise.agents.router import route_request

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    user_id: str | None = None
    roles: list[str] = ["engineering"]


async def stream_answer(message: str) -> AsyncIterator[str]:
    route = await route_request(message)
    payload = await answer_with_retrieval(message, ["engineering"])
    yield f"Route: {route.name}\n"
    yield f"Next step: {route.next_action}\n"
    yield f"Answer: {payload['answer']}\n"
    if payload["sources"]:
        yield "Sources:\n"
        for source in payload["sources"]:
            yield f"- {source['title']} ({source['document_id']})\n"


@router.post("/chat")
async def chat(payload: ChatRequest) -> StreamingResponse:
    return StreamingResponse(stream_answer(payload.message), media_type="text/plain")
