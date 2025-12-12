import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()

def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("PASSWORD_SQL"),
    )
    cursor = conn.cursor()

    # Création de la DB si elle n'existe pas
    cursor.execute("CREATE DATABASE IF NOT EXISTS haiku_db")
    cursor.execute("USE haiku_db")

    # Création de la table haikus si elle n'existe pas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS haikus (
        id INT AUTO_INCREMENT PRIMARY KEY,
        mots_cles TEXT NOT NULL,
        haiku TEXT NOT NULL,
        image_path TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
    print("✅ Base de données initialisée.")

if __name__ == "__main__":
    init_db()
