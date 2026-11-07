from fastapi import FastAPI
import requests
from database import get_db

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/collect")
def collect():

    conn = get_db()
    cur = conn.cursor()

    total_saved = 0

    for page in range(1, 51):

        try:

            url = f"https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json?pageNo={page}"

            data = requests.get(
                url,
                timeout=10
            ).json()

            rows = data["data"]["list"]

            for row in rows:

                cur.execute("""
                INSERT OR IGNORE INTO history
                (issue, number, color)
                VALUES (?, ?, ?)
                """,
                (
                    row["issueNumber"],
                    int(row["number"]),
                    row["color"]
                ))

                total_saved += 1

        except Exception as e:
            print(e)

    conn.commit()

    return {
        "saved": total_saved
    }

@app.get("/api/history")
def history():

    conn = get_db()

    rows = conn.execute("""
    SELECT *
    FROM history
    ORDER BY issue DESC
    LIMIT 500
    """).fetchall()

    return [dict(x) for x in rows]
