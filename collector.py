import requests
import time

from database import get_db

API = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

while True:

    try:

        conn = get_db()
        cur = conn.cursor()

        data = requests.get(API, timeout=10).json()

        rows = data["data"]["list"]

        for row in rows:

            cur.execute("""
            INSERT OR IGNORE INTO history
            (issue,number,color)
            VALUES(?,?,?)
            """,(
                row["issueNumber"],
                int(row["number"]),
                row["color"]
            ))

        conn.commit()

        print("Updated")

    except Exception as e:
        print(e)

    time.sleep(30)
