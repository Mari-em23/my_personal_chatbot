import sqlite3

def create_database():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings_table(
            passage_id INTEGER PRIMARY KEY AUTOINCREMENT,
            passage TEXT UNIQUE,
            embedding TEXT
        )
    """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_database()
    print("database.db created")