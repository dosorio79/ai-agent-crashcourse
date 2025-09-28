from typing import List, Dict, Any, Union
from minsearch import Index, VectorSearch
from sentence_transformers import SentenceTransformer
import numpy as np


def create_text_index(
    chunks: List[Dict[str, Any]],
    text_fields: List[str] = ["chunk", "title", "description", "filename"],
    keyword_fields: List[str] = [],
) -> Index:
    """
    Creates a text index from chunks using minsearch.

    Args:
        chunks: The data to be indexed.
        text_fields: Fields to be indexed as text fields.
        keyword_fields: Fields to be indexed as keyword fields.

    Returns:
        Index: The created text index.
    """
    index = Index(
        text_fields=text_fields,
        keyword_fields=keyword_fields,
    )
    return index.fit(chunks)


def load_embedding_model(model_name: str = "multi-qa-distilbert-cos-v1") -> SentenceTransformer:
    """Load and return a SentenceTransformer embedding model."""
    return SentenceTransformer(model_name)


def embed_text(
    text: Union[str, List[str]],
    model: SentenceTransformer,
) -> np.ndarray:
    """
    Embed a string or list of strings using a preloaded model.

    Args:
        text: Single string or list of strings.
        model: A SentenceTransformer model.

    Returns:
        np.ndarray of embeddings.
    """
    return model.encode(text, convert_to_numpy=True)


def create_vector_index(
    chunks: List[Dict[str, Any]],
    model: SentenceTransformer,
    text_field: str = "chunk",
) -> VectorSearch:
    """
    Create a vector index using minsearch.VectorSearch.

    Args:
        chunks: The data to be indexed.
        model: Preloaded SentenceTransformer model.
        text_field: Field of the chunk to embed.

    Returns:
        VectorSearch object fitted with embeddings and chunks.
    """
    texts = [c[text_field] for c in chunks]
    embeddings = embed_text(texts, model)
    vindex = VectorSearch()
    vindex.fit(embeddings, chunks)
    return vindex


def text_search(index: Index, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search the text index.

    Args:
        index: Fitted Index object.
        query: Query string.
        top_k: Number of results to return.

    Returns:
        List of search results.
    """
    return index.search(query, num_results=top_k)


def vector_search(
    vindex: VectorSearch,
    model: SentenceTransformer,
    query: str,
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Search chunks using vector similarity.

    Args:
        vindex: VectorSearch object (fitted).
        model: Preloaded SentenceTransformer model.
        query: Search query.
        top_k: Number of results to return.

    Returns:
        List of dicts with scores and chunk metadata.
    """
    query_vec = embed_text(query, model)
    return vindex.search(query_vec, num_results=top_k)

def hybrid_search(
    index: Index,
    vindex: VectorSearch,
    model: SentenceTransformer,
    query: str,
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Combine text and vector search results, deduplicated by filename+start.

    Args:
        index: Fitted text Index.
        vindex: Fitted VectorSearch.
        model: Preloaded SentenceTransformer model.
        query: Query string.
        top_k: Number of results to return.

    Returns:
        List of combined results.
    """
    text_results = text_search(index, query, top_k)
    vector_results = vector_search(vindex, model, query, top_k)

    seen = set()
    merged = []
    # Deduplicate results by (filename, start)
    for r in text_results + vector_results:
        ident = (r.get("filename"), r.get("start"))
        if ident not in seen:
            seen.add(ident)
            merged.append(r)

    return merged[:top_k]
