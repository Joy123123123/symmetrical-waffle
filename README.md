# Lead Collection App

A lightweight **FastAPI** app that collects visitor leads (name, email, phone) via a web form and persists them to a local `leads.csv` file.  
Ready to deploy for free on [Koyeb](https://www.koyeb.com/) or [Render](https://render.com/).

---

## Project Structure

```
.
├── main.py            # FastAPI application
├── requirements.txt   # Python dependencies
├── Procfile           # Process file for Koyeb / Render
├── static/
│   └── index.html     # Lead collection form (served at /)
└── leads.csv          # Auto-created on first run
```

---

## Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open **http://localhost:8000** in your browser to see the lead form.

| Endpoint | Description |
|----------|-------------|
| `GET  /` | Lead collection form |
| `POST /leads` | Save a new lead (JSON body: `name`, `email`, `phone`) |
| `GET  /leads/download` | Download `leads.csv` |
| `GET  /docs` | Interactive API docs (Swagger UI) |

---

## Deploy to Koyeb (free)

1. Push this repo to GitHub.
2. Go to [koyeb.com](https://www.koyeb.com/) → **Create Web Service** → select your GitHub repo.
3. Choose **Buildpack** as the builder.
4. Set the **Run command** to:
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. Click **Deploy**. Koyeb will give you a permanent `*.koyeb.app` URL.

## Deploy to Render (free)

1. Push this repo to GitHub.
2. Go to [render.com](https://render.com/) → **New Web Service** → connect your repo.
3. Set **Start command** to:
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
4. Click **Create Web Service**.

> **Note:** On free tiers the service may spin down after inactivity; the first request after sleep may be slower.

---

## Download Leads

Visit `GET /leads/download` (or open `https://YOUR_APP/leads/download`) to download all collected leads as a CSV file.
