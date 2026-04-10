import csv
import os
import threading
from fastapi import FastAPI, Form, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(title="Amazon Leads Collector")

LEADS_FILE = "leads.csv"
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Admin credentials for the read-only /leads endpoint.
# Override via environment variables in production.
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "changeme")

security = HTTPBasic()
_csv_lock = threading.Lock()

# Serve static files (JS, CSS, images, etc.) from /static
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def _ensure_csv_header():
    """Create leads.csv with header row if it does not exist yet."""
    with _csv_lock:
        if not os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["name", "email", "phone", "message"])


_ensure_csv_header()


def _verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """HTTP Basic auth guard for admin-only endpoints."""
    correct_user = secrets.compare_digest(credentials.username, ADMIN_USER)
    correct_pass = secrets.compare_digest(credentials.password, ADMIN_PASS)
    if not (correct_user and correct_pass):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/", response_class=FileResponse)
async def index():
    """Serve the lead-collection form."""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.post("/leads")
async def submit_lead(
    name: str = Form(..., max_length=120),
    email: str = Form(..., max_length=254),
    phone: str = Form("", max_length=30),
    message: str = Form("", max_length=1000),
):
    """Accept a lead from the HTML form and append it to leads.csv."""
    # Basic email sanity check
    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=422, detail="Invalid email address.")

    with _csv_lock:
        with open(LEADS_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([name, email, phone, message])

    return JSONResponse({"status": "ok", "message": "Lead saved successfully."})


@app.get("/leads", dependencies=[Depends(_verify_admin)])
async def list_leads():
    """Return all collected leads as JSON (admin-only, HTTP Basic auth)."""
    _ensure_csv_header()
    leads = []
    with _csv_lock:
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                leads.append(row)
    return {"leads": leads}
