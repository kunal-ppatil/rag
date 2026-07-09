from dataclasses import dataclass


@dataclass(frozen=True)
class VectorRecord:
    document_id: str
    chunk_id: str
    text: str
    allowed_groups: list[str]


async def upsert_vectors(records: list[VectorRecord]) -> int:
    return len(records)
