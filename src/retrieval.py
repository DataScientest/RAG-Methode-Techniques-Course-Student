"""Index the chunks in a local Qdrant base and search them, with the improvements of chapters 3 and 4."""
import os
import sys

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from src.chunking import STRATEGIES, section_key

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


def search(question: str, k: int = 5, strategy: str = "titled") -> list[Document]:
    """Return the k chunks closest to the question."""
    store = QdrantVectorStore.from_existing_collection(strategy, EMBEDDINGS, path=QDRANT_PATH)
    docs = store.similarity_search(question, k=k)
    store.client.close()
    return docs


def expand_to_sections(docs: list[Document], sections: dict[str, str], max_chars: int = 6000) -> list[Document]:
    """Replace each chunk by the text of its whole section, without duplicates.

    A section longer than max_chars characters is kept as the chunk found.
    """
    expanded = []
    seen = set()
    for doc in docs:
        key = section_key(doc.metadata["doc_id"], doc.metadata["section_path"])
        text = sections.get(key)
        if text is None or len(text) > max_chars:
            text = doc.page_content
            key = text
        if key not in seen:
            seen.add(key)
            expanded.append(Document(page_content=text, metadata=doc.metadata))
    return expanded


if __name__ == "__main__":
    strategy = sys.argv[1]
    if len(sys.argv) > 2:
        for doc in search(sys.argv[2], strategy=strategy):
            print(doc.metadata["doc_id"], "|", doc.metadata["section_path"] or doc.page_content[:60].replace("\n", " "))
    else:
        print(build_store(strategy), "chunks indexés dans la collection", strategy)
