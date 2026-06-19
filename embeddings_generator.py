from sentence_transformers import SentenceTransformer
import numpy as np
from SQLite.connection import get_connection

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
model = SentenceTransformer(MODEL_NAME)

def insert_embedding(passage, embedding):
    # Insert a new embedding into the table
    connection = get_connection()
    cursor = connection.cursor()

    embedding_insertion_query = """
        INSERT OR IGNORE INTO embeddings_table(passage, embedding)
        VALUES (:passage, :embedding)
    """

    cursor.execute(embedding_insertion_query, {
        'embedding': embedding,
        'passage': passage
    })

    connection.commit()

def chunk_text(text, max_chars=800):
    if not text:
        return []

    parts = str(text).split("\n")
    chunks = []
    current = ""

    for p in parts:
        p = p.strip()
        if not p:
            continue

        if len(current) + len(p) < max_chars:
            current += " " + p
        else:
            if current:
                chunks.append(current.strip())
            current = p

    if current:
        chunks.append(current.strip())

    return chunks if chunks else [str(text)[:max_chars]]


def generate_embedding(text):
    chunks = chunk_text(text)
    vectors = model.encode(chunks)

    vectors = np.array(vectors)
    vec = np.mean(vectors, axis=0)

    vec = vec / np.linalg.norm(vec)

    return ",".join(map(str, vec.tolist()))


def _parse_embedding(emb_str):
    return np.array(list(map(float, emb_str.split(","))))


def run():
    with open("internal_data.txt", "r", encoding="utf-8") as data_file:
        passages = data_file.readlines()

        for passage in passages:
            passage = passage.strip()
            if not passage:
                continue

            embedding = generate_embedding(passage)
            insert_embedding(passage, embedding)

    print("[INFO] Done!")


if __name__ == "__main__":
    run()