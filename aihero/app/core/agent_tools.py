from typing import List, Dict, Any, Callable
from minsearch import Index, VectorSearch
from sentence_transformers import SentenceTransformer

from .search import text_search, vector_search, hybrid_search


def make_agent_tools(
    text_index: Index,
    vector_index: VectorSearch,
    embedding_model: SentenceTransformer,
) -> List[Callable[[str, int], List[Dict[str, Any]]]]:
    """
    Return agent-ready versions of the search tools that are proper functions,
    with dependencies bound inside closures.

    Args:
        text_index: A fitted lexical Index.
        vector_index: A fitted VectorSearch.
        embedding_model: Preloaded SentenceTransformer model.

    Returns:
        List of callable search tools (text, vector, hybrid).
    """

    def text_search_tool(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Perform a lexical search over the ingested documentation."""
        return text_search(text_index, query, top_k=num_results)

    def vector_search_tool(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Perform a semantic (vector-based) search over the ingested documentation."""
        return vector_search(vector_index, embedding_model, query, top_k=num_results)

    def hybrid_search_tool(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Perform a hybrid search combining lexical and semantic results."""
        return hybrid_search(text_index, vector_index, embedding_model, query, top_k=num_results)

    return [text_search_tool, vector_search_tool, hybrid_search_tool]
