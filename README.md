# Amazon Leads — FastAPI App

A lightweight lead-collection web app built with **FastAPI**.  
Leads submitted via the HTML form are persisted to **`leads.csv`** on the server.

---

## 📁 Project Structure

```
.
├── main.py            # FastAPI application (entrypoint: main:app)
├── requirements.txt   # Python dependencies
├── Procfile           # Start command for Render / Railway / Koyeb
├── leads.csv          # Auto-created on first run; stores collected leads
└── static/
    └── index.html     # Lead-collection form (served at /)
```

---

## 🚀 Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
uvicorn main:app --reload
```

Open **http://127.0.0.1:8000** in your browser.

- **Form:** `http://127.0.0.1:8000/`
- **View leads (JSON):** `http://127.0.0.1:8000/leads`
- **Interactive API docs:** `http://127.0.0.1:8000/docs`

---

## ☁️ Deploy for Free

### Koyeb

1. Push this repo to GitHub.
2. Go to [koyeb.com](https://www.koyeb.com) → **Create Web Service** → select the GitHub repo.
3. Choose **Buildpack** and set the **Run command**:
   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
4. Click **Deploy**. Koyeb will provide a permanent `*.koyeb.app` URL.

### Render

1. Push this repo to GitHub.
2. Go to [render.com](https://render.com) → **New Web Service** → connect the repo.
3. Render automatically reads the **`Procfile`** which contains:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
4. Click **Create Web Service**.

> **Note:** On free-tier plans (Render, Koyeb) the service may spin down after inactivity.  
> The first request after a cold start may take a few seconds.

---

## 📊 Viewing Leads

Leads are saved to `leads.csv` in the working directory.  
You can also view them as JSON at `/leads` (protected by HTTP Basic auth).

Default credentials (override in production via environment variables):

| Variable | Default |
|---|---|
| `ADMIN_USER` | `admin` |
| `ADMIN_PASS` | `changeme` |

Set strong credentials before deploying:

```bash
export ADMIN_USER=myadmin
export ADMIN_PASS=a-very-strong-password
```