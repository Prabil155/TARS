import sqlite3
from datetime import datetime
import re


class Memory:

    def __init__(self, database="tars_memory.db"):
        self.database = database
        self.create_database()

    # ==========================================
    # CREATE DATABASE
    # ==========================================

    def create_database(self):

        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    # ==========================================
    # SAVE MEMORY
    # ==========================================

    def save(self, memory):

        if not memory:
            return

        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO memories
            (memory, created_at)
            VALUES (?, ?)
            """,
            (
                memory.strip(),
                datetime.now().isoformat()
            )
        )

        connection.commit()
        connection.close()

    # ==========================================
    # GET ALL MEMORIES
    # ==========================================

    def get_all(self):

        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT memory, created_at
            FROM memories
            ORDER BY id ASC
            """
        )

        results = cursor.fetchall()

        connection.close()

        return results

    # ==========================================
    # SEARCH MEMORY
    # ==========================================

    def search(self, query):

        if not query:
            return []

        # ------------------------------------------
        # Extract useful words from the query
        # ------------------------------------------

        words = re.findall(
            r"[a-zA-Z0-9]+",
            query.lower()
        )

        # Ignore common question words
        stop_words = {
            "what",
            "is",
            "my",
            "the",
            "a",
            "an",
            "who",
            "am",
            "i",
            "are",
            "do",
            "does",
            "did",
            "you",
            "me",
            "your",
            "tell",
            "about",
            "please",
            "can",
            "could",
            "would",
            "should",
            "how",
            "where",
            "when",
            "why"
        }

        keywords = [
            word
            for word in words
            if word not in stop_words
            and len(word) >= 2
        ]

        if not keywords:
            return []

        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        # ------------------------------------------
        # Search each useful keyword
        # ------------------------------------------

        conditions = []

        parameters = []

        for keyword in keywords:

            conditions.append(
                "LOWER(memory) LIKE ?"
            )

            parameters.append(
                f"%{keyword}%"
            )

        query_sql = f"""
            SELECT memory, created_at
            FROM memories
            WHERE {" OR ".join(conditions)}
            ORDER BY id DESC
        """

        cursor.execute(
            query_sql,
            parameters
        )

        results = cursor.fetchall()

        connection.close()

        return results

    # ==========================================
    # CLEAR MEMORY
    # ==========================================

    def clear(self):

        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM memories"
        )

        connection.commit()
        connection.close()


# ==============================================
# TEST
# ==============================================

if __name__ == "__main__":

    memory = Memory()

    print("🧠 TARS Memory System")
    print("---------------------")

    print("\nExisting memories:")

    for item in memory.get_all():

        print(
            f"- {item[0]}"
        )

    print("\nSearching for 'What is my name?':")

    results = memory.search(
        "What is my name?"
    )

    for item in results:

        print(
            f"- {item[0]}"
        )

    print("\nSearching for 'What project am I building?':")

    results = memory.search(
        "What project am I building?"
    )

    for item in results:

        print(
            f"- {item[0]}"
        )

    print("\n✅ Memory search test complete.")
