"""Three ways to cut the fiches into chunks: by size, on the titles, on the titles with the title in front."""
import statistics
from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.corpus import count_tokens


def size_splitter(chunk_size: int = 500) -> RecursiveCharacterTextSplitter:
    """A splitter that cuts a text into pieces of at most chunk_size tokens."""
    return RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base", chunk_size=chunk_size, chunk_overlap=0)


def chunk_fixed(corpus_dir: str = "data/corpus", chunk_size: int = 500) -> list[Document]:
    """Cut each fiche into pieces of chunk_size tokens, without looking at its titles."""
    chunks = []
    for path in sorted(Path(corpus_dir).glob("*.md")):
        for text in size_splitter(chunk_size).split_text(path.read_text(encoding="utf-8")):
            chunks.append(Document(page_content=text, metadata={"doc_id": path.stem, "section_path": ""}))
    return chunks


STRATEGIES = {
    "fixed": lambda: chunk_fixed(),
}


if __name__ == "__main__":
    for name, make_chunks in STRATEGIES.items():
        sizes = [count_tokens(chunk.page_content) for chunk in make_chunks()]
        print(name.ljust(8), len(sizes), "chunks | médiane", int(statistics.median(sizes)), "tokens | max", max(sizes))
