import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def save_to_db(mots_cles, haiku, image_path):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("PASSWORD_SQL"),
        database="haiku_db"
    )

    cursor = conn.cursor()

    sql = """
    INSERT INTO haikus (mots_cles, haiku, image_path, created_at)
    VALUES (%s, %s, %s, %s)
    """

    values = (", ".join(mots_cles), haiku, image_path, datetime.now())

    cursor.execute(sql, values)
    conn.commit()
    conn.close()

    print("✔ Haiku sauvegardé !")
