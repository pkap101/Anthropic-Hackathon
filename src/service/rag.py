import os
from pathlib import Path
from typing import List, Dict

from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.embeddings.base import Embeddings

from voyageai import Client

load_dotenv()

BASE_DATA_DIR = Path(__file__).parent.parent / "data"

# Map course id -> where PDFs live + where Chroma store is
COURSE_CONFIG: Dict[str, Dict[str, Path]] = {
    # PDFs in:  src/data/dmt_2
    # Chroma in: src/data/chroma_dmt2
    "dmt_2": {
        "pdf_dir": BASE_DATA_DIR / "dmt_2",
        "chroma_dir": BASE_DATA_DIR / "chroma_dmt_2",
    },
    # PDFs in:  src/data/qa
    # Chroma in: src/data/chroma_qa
    "qa": {
        "pdf_dir": BASE_DATA_DIR / "qa",
        "chroma_dir": BASE_DATA_DIR / "chroma_qa",
    },
}


class VoyageEmbeddings(Embeddings):
    def __init__(self, model: str = "voyage-2", api_key: str | None = None):
        self.client = Client(api_key=api_key or os.getenv("VOYAGE_API_KEY"))
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.client.embed(texts=texts, model=self.model).embeddings

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]


def _load_pdf_docs(course: str) -> List[Document]:
    cfg = COURSE_CONFIG[course]
    pdf_dir = cfg["pdf_dir"]
    docs: List[Document] = []

    for pdf_path in pdf_dir.glob("*.pdf"):
        reader = PdfReader(str(pdf_path), strict=False)
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if not text.strip():
                continue
            docs.append(
                Document(
                    page_content=text,
                    metadata={"source": str(pdf_path), "page": i},
                )
            )
    return docs


def build_vectorstore(course: str) -> None:
    """Run manually per course, e.g.: python -m src.service.rag dmt_2"""
    if course not in COURSE_CONFIG:
        raise ValueError(f"Unknown course: {course}")

    docs = _load_pdf_docs(course)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )
    splits = splitter.split_documents(docs)

    embeddings = VoyageEmbeddings()
    chroma_dir = COURSE_CONFIG[course]["chroma_dir"]
    chroma_dir.mkdir(parents=True, exist_ok=True)

    # For langchain-chroma >=0.1.x, this writes to disk automatically
    Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=str(chroma_dir),
    )

    print(f"Built vector store for course={course} from PDFs in {COURSE_CONFIG[course]['pdf_dir']}")


# --- Runtime: load all available course vector stores ---

_embeddings = VoyageEmbeddings()
_vectordbs: Dict[str, Chroma] = {}

for course, cfg in COURSE_CONFIG.items():
    chroma_dir = cfg["chroma_dir"]
    if chroma_dir.exists():
        _vectordbs[course] = Chroma(
            persist_directory=str(chroma_dir),
            embedding_function=_embeddings,
        )


def get_retriever(course: str):
    """Used by FastAPI: get retriever for a specific course."""
    if course not in _vectordbs:
        raise ValueError(f"No vector store found for course: {course}")
    return _vectordbs[course].as_retriever(search_kwargs={"k": 5})


if __name__ == "__main__":
    #to run:
    # python -m src.service.rag dmt_2
    # python -m src.service.rag qa
    import sys

    if len(sys.argv) != 2:
        print("Usage: python -m src.service.rag <course_id>")
        print(f"Known courses: {list(COURSE_CONFIG.keys())}")
        raise SystemExit(1)

    build_vectorstore(sys.argv[1])

    