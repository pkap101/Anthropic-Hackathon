import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.embeddings.base import Embeddings

from voyageai import Client

load_dotenv()

#DATA_DIR = Path(__file__).parent.parent / "data" / "dmt_2"
#CHROMA_DIR = Path(__file__).parent.parent / "data" / "chroma_dmt_2"

DATA_DIR = Path(__file__).parent.parent / "data" / "qa"
CHROMA_DIR = Path(__file__).parent.parent / "data" / "chroma_qa"


class VoyageEmbeddings(Embeddings):
    def __init__(self, model: str = "voyage-2", api_key: str | None = None):
        self.client = Client(api_key=api_key or os.getenv("VOYAGE_API_KEY"))
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.client.embed(texts=texts, model=self.model).embeddings

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]


def _load_pdf_docs() -> List[Document]:
    docs: List[Document] = []
    for pdf_path in DATA_DIR.glob("*.pdf"):
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


def build_vectorstore() -> None:
    docs = _load_pdf_docs()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )
    splits = splitter.split_documents(docs)

    embeddings = VoyageEmbeddings()
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
    )


_embeddings = VoyageEmbeddings()
_vectordb = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=_embeddings,
)


def get_retriever():
    return _vectordb.as_retriever(search_kwargs={"k": 5})


if __name__ == "__main__":
    build_vectorstore()
    print(f"Built vector store from PDFs in {DATA_DIR}")
