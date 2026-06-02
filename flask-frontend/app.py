from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "foodvotes")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/vote", methods=["POST"])
def vote():
    food_option = request.form["food_option"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO votes (food_option) VALUES (%s)",
        (food_option,)
    )

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("results"))


@app.route("/results")
def results():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT food_option, COUNT(*)
        FROM votes
        GROUP BY food_option
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    amala_votes = 0
    afang_votes = 0

    for row in rows:
        if row[0] == "amala":
            amala_votes = row[1]
        elif row[0] == "afang":
            afang_votes = row[1]

    total = amala_votes + afang_votes

    amala_percent = (
        round((amala_votes / total) * 100, 1)
        if total > 0 else 0
    )

    afang_percent = (
        round((afang_votes / total) * 100, 1)
        if total > 0 else 0
    )

    return render_template(
        "results.html",
        amala_votes=amala_votes,
        afang_votes=afang_votes,
        amala_percent=amala_percent,
        afang_percent=afang_percent
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
