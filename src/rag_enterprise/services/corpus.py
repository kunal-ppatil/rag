from dataclasses import dataclass
from pathlib import Path

from rag_enterprise.core.config import get_documents_path


@dataclass(frozen=True)
class KnowledgeDocument:
    document_id: str
    title: str
    text: str
    allowed_groups: list[str]


def _parse_metadata_line(line: str) -> tuple[str, str] | None:
    if ":" not in line:
        return None
    key, value = line.split(":", 1)
    key = key.strip().lower()
    value = value.strip()
    if not key or not value:
        return None
    return key, value


def _read_document_file(path: Path) -> KnowledgeDocument | None:
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return None

    metadata: dict[str, str] = {}
    body_lines: list[str] = []
    in_metadata = True

    for line in content.splitlines():
        stripped = line.strip()
        if in_metadata and not stripped:
            in_metadata = False
            continue
        if in_metadata:
            parsed = _parse_metadata_line(stripped)
            if parsed is not None:
                key, value = parsed
                metadata[key] = value
                continue
            in_metadata = False
        body_lines.append(line)

    title = metadata.get("title") or path.stem.replace("-", " ").title()
    document_id = metadata.get("document_id") or path.stem
    allowed_groups = [group.strip() for group in metadata.get("allowed_groups", "engineering,admin").split(",") if group.strip()]
    body = "\n".join(body_lines).strip()
    if not body:
        return None

    return KnowledgeDocument(
        document_id=document_id,
        title=title,
        text=body,
        allowed_groups=allowed_groups,
    )


def load_local_documents() -> list[KnowledgeDocument]:
    documents_path = get_documents_path()
    if not documents_path.exists():
        return []

    documents: list[KnowledgeDocument] = []
    for path in sorted(documents_path.rglob("*")):
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        document = _read_document_file(path)
        if document is not None:
            documents.append(document)
    return documents


DEFAULT_CORPUS: list[KnowledgeDocument] = [
    KnowledgeDocument(
        document_id="hr-001",
        title="HR Policy Overview",
        text=(
            "Employees can request PTO through the HR portal. Managers approve requests within "
            "three business days. Sensitive HR documents are restricted to the hr group."
        ),
        allowed_groups=["hr", "admin"],
    ),
    KnowledgeDocument(
        document_id="finance-001",
        title="Finance Expense Policy",
        text=(
            "Expenses over 500 dollars require manager approval and a receipt. Finance reviews "
            "submissions every Friday. Access is limited to finance and admin groups."
        ),
        allowed_groups=["finance", "admin"],
    ),
    KnowledgeDocument(
        document_id="eng-001",
        title="Engineering Release Notes",
        text=(
            "Production releases happen on Tuesdays after the release checklist is complete. "
            "Rollback steps are documented in the incident playbook."
        ),
        allowed_groups=["engineering", "admin"],
    ),
]


def load_corpus() -> list[KnowledgeDocument]:
    local_documents = load_local_documents()
    if local_documents:
        return local_documents + DEFAULT_CORPUS
    return DEFAULT_CORPUS
