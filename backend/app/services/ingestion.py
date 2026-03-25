from hashlib import sha256


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    if not text:
        return []
    chunks: list[str] = []
    step = max(chunk_size - overlap, 1)
    for i in range(0, len(text), step):
        chunks.append(text[i : i + chunk_size])
    return chunks


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    """Deterministic placeholder embeddings for deployable scaffold."""
    vectors: list[list[float]] = []
    for chunk in chunks:
        digest = sha256(chunk.encode("utf-8")).digest()
        vectors.append([b / 255 for b in digest[:8]])
    return vectors
