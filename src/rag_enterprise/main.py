from fastapi import FastAPI

from rag_enterprise.api.routes.chat import router as chat_router
from rag_enterprise.api.routes.health import router as health_router


app = FastAPI(title="Enterprise RAG Blueprint", version="0.1.0")

app.include_router(health_router)
app.include_router(chat_router, prefix="/v1")
