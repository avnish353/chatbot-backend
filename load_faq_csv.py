# load_faq_csv.py
import csv
from database.db import get_connection  # your MySQL connection function

def load_csv_to_db():
    conn = get_connection()
    cursor = conn.cursor()

    with open("data/FAQ.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute(
                "INSERT INTO faq (question, answer) VALUES (%s, %s)",
                (row["question"], row["answer"])
            )

    conn.commit()
    conn.close()
    print("Data inserted into MySQL successfully!")

if __name__ == "__main__":
    load_csv_to_db()