import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_voyageai import VoyageAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

# Put your discrete math PDFs here: src/data/dmt_2/*.pdf
DATA_DIR = Path(__file__).parent.parent / "data" / "dmt_2"
CHROMA_DIR = Path(__file__).parent.parent / "data" / "chroma_dmt_2"


def build_vectorstore() -> None:
    """Run manually when PDFs change: python -m service.rag"""
    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True,
    )
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )
    splits = splitter.split_documents(docs)

    embeddings = VoyageAIEmbeddings(
        model="voyage-multimodal-3",
        voyage_api_key=os.getenv("VOYAGE_API_KEY"),
    )

    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
    )
    vectordb.persist()


# --- Runtime: reuse persisted DB (no re-embedding of docs) ---

_embeddings = VoyageAIEmbeddings(
    model="voyage-multimodal-3",
    voyage_api_key=os.getenv("VOYAGE_API_KEY"),
)

_vectordb = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=_embeddings,
)


def get_retriever():
    return _vectordb.as_retriever(search_kwargs={"k": 5})


if __name__ == "__main__":
    build_vectorstore()
    print("Built vector store from PDFs in", DATA_DIR)
