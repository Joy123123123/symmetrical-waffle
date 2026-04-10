import csv
import os
import threading
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Lead Collection App")

# Directory containing static files
STATIC_DIR = Path(__file__).parent / "static"
LEADS_CSV = Path(__file__).parent / "leads.csv"
CSV_HEADERS = ["name", "email", "phone"]

# Lock to prevent concurrent writes corrupting the CSV
_csv_lock = threading.Lock()


def ensure_csv():
    """Create leads.csv with headers if it does not exist."""
    if not LEADS_CSV.exists():
        with open(LEADS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()


ensure_csv()


class Lead(BaseModel):
    name: str
    email: EmailStr
    phone: str = ""


@app.get("/")
def index():
    """Serve the lead collection form."""
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/leads", status_code=201)
def create_lead(lead: Lead):
    """Append a new lead to leads.csv."""
    with _csv_lock:
        with open(LEADS_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writerow({"name": lead.name, "email": lead.email, "phone": lead.phone})
    return JSONResponse({"status": "ok", "message": "Lead saved successfully."}, status_code=201)


@app.get("/leads/download")
def download_leads():
    """Download all leads as a CSV file."""
    ensure_csv()
    return FileResponse(
        LEADS_CSV,
        media_type="text/csv",
        filename="leads.csv",
    )
