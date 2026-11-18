"""Index the chunks in a local Qdrant base and search them, with the improvements of chapters 3 and 4."""
import os
import sys

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from src.chunking import STRATEGIES

load_dotenv()
QDRANT_PATH = "data/qdrant"
EMBEDDINGS = OpenAIEmbeddings(model="text-embedding-3-small", base_url=os.environ["LLM_BASE_URL"],
                              api_key=os.environ["LLM_API_KEY"], check_embedding_ctx_length=False)


def build_store(strategy: str) -> int:
    """Embed the chunks of one strategy and write them to the Qdrant collection of the same name."""
    chunks = STRATEGIES[strategy]()
    store = QdrantVectorStore.from_documents(chunks, EMBEDDINGS, path=QDRANT_PATH,
                                             collection_name=strategy, force_recreate=True)
    store.client.close()  # only one client at a time can open data/qdrant/
    return len(chunks)


def search(question: str, k: int = 5, strategy: str = "fixed") -> list[Document]:
    """Return the k chunks closest to the question."""
    store = QdrantVectorStore.from_existing_collection(strategy, EMBEDDINGS, path=QDRANT_PATH)
    docs = store.similarity_search(question, k=k)
    store.client.close()
    return docs


if __name__ == "__main__":
    strategy = sys.argv[1]
    if len(sys.argv) > 2:
        for doc in search(sys.argv[2], strategy=strategy):
            print(doc.metadata["doc_id"], "|", doc.metadata["section_path"] or doc.page_content[:60].replace("\n", " "))
    else:
        print(build_store(strategy), "chunks indexés dans la collection", strategy)
