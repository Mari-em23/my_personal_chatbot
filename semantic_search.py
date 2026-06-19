from sentence_transformers import SentenceTransformer
import numpy as np
from SQLite.connection import get_connection


MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
model = SentenceTransformer(MODEL_NAME)


def get_all_embeddings():
    connection = get_connection()
    cursor = connection.cursor()
    embeddings_fetch_query = "SELECT * FROM embeddings_table"
    cursor.execute(embeddings_fetch_query)
    return cursor.fetchall()


def get_passage_by_id(id):
    connection = get_connection()
    cursor = connection.cursor()
    embeddings_fetch_query = "SELECT passage FROM embeddings_table WHERE passage_id = :id"
    cursor.execute(embeddings_fetch_query, {'id': id})
    return cursor.fetchone()[0]


def _parse_embedding(emb):
    return np.array(list(map(float, emb.split(","))))


def generate_query_embedding(query):
    vec = model.encode([query])[0]
    vec = vec / np.linalg.norm(vec)
    return vec


def semantic_search(query_vec, top_k=20):
    # Cosine similarity search over embeddings_table.

    all_embeddings = get_all_embeddings()
    q = np.array(query_vec)

    scores = []

    for row in all_embeddings:
        id, passage, emb = row
        if not emb:
            continue

        v = _parse_embedding(emb)

        sim = float(np.dot(q, v))  # vectors already normalized → dot = cosine similarity
        scores.append((id, sim))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]


def filter_results(results, threshold=0.4):
    # Increasing can result in more results but potentially irrelevant ones

    filtered = []

    # Semantic filtering
    for post_id, score in results:
        if score >= threshold:
            filtered.append((post_id, score))

    return filtered


def main_search(query, top_k=10):
    """
    Main entry point.
    Returns list of (passage_id, score) tuples.
    """
    query_vec = generate_query_embedding(query)

    results = semantic_search(query_vec, top_k=top_k * 2)
    results = filter_results(results)

    return results


def search_with_details(query, top_k=10):
    results = main_search(query, top_k)

    results_scores = sorted(
        results,
        key=lambda x: x[1],
        reverse=True
    )[:top_k]

    final_results = []

    for id, score in results_scores:
        passage = get_passage_by_id(id)

        if passage:
            final_results.append({
                "passage": passage,
                "score": score
            })
    print("I have searched :" + query +" in the internal DB")
    print(final_results)

    return final_results


if __name__ == "__main__":
    query = input("Search query: ")
    results = search_with_details(query, top_k=5)
    print(results)