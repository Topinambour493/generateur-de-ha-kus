from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

from init_db import init_db

load_dotenv()
app = Flask(__name__)

def db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("PASSWORD_DB"),
        database="haiku_db"
    )
@app.get("/")
def haikus():
    mots = request.args.get("mots")  # ex: /?mots=lune,vent
    conn = db()
    cursor = conn.cursor(dictionary=True)

    if mots:
        mots_liste = mots.split(",")  # transforme "lune,vent" en ["lune", "vent"]
        # Construction dynamique de la clause WHERE
        conditions = " OR ".join(["haiku LIKE %s" for _ in mots_liste])
        query = f"SELECT * FROM haikus WHERE {conditions} ORDER BY created_at DESC"
        params = [f"%{mot}%" for mot in mots_liste]
        cursor.execute(query, params)
    else:
        cursor.execute("SELECT * FROM haikus ORDER BY created_at DESC")

    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
