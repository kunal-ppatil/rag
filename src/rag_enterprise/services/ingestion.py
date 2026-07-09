from pathlib import Path

from rag_enterprise.core.config import get_documents_path


async def ingest_document(source: str) -> str:
    source_path = Path(source)
    if not source_path.exists():
        return f"source not found: {source}"

    destination_dir = get_documents_path()
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination_path = destination_dir / source_path.name
    destination_path.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")
    return f"ingested {source_path.name}"
