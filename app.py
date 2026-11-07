from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from database import get_db

app = FastAPI()

templates = Jinja2Templates(
    directory="templates"
)

@app.get("/")
def health():
    return {"status":"running"}

@app.get("/api/history")
def history():

    conn = get_db()

    rows = conn.execute("""
    SELECT *
    FROM history
    ORDER BY issue DESC
    LIMIT 100
    """).fetchall()

    return [dict(x) for x in rows]

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    conn = get_db()

    rows = conn.execute("""
    SELECT *
    FROM history
    ORDER BY issue DESC
    LIMIT 50
    """).fetchall()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "rows": rows
        }
    )
