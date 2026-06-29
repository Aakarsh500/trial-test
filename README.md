# Capstone Secure User Auth API

A secure user authentication REST API built with FastAPI, SQLAlchemy, and python-jose.

## How to Deploy to Render

This application is ready to be hosted as a **Web Service** on [Render](https://render.com/).

### 1. Create a Web Service on Render
1. Sign in to your Render Dashboard and click **New +** -> **Web Service**.
2. Connect your GitHub repository (e.g. `trial-test`).
3. Set the following details:
   - **Name**: `capstone-auth-api` (or any name you prefer)
   - **Environment**: `Python 3` (or Python)
   - **Branch**: `main` (or the branch you pushed to)
   - **Region**: Select the one closest to your users
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 2. Configure Environment Variables
In the **Environment** tab of your Render Web Service, add the following variables:
- `SECRET_KEY`: A long, random secure string for signing JWT tokens (e.g. generated via `openssl rand -hex 32`).
- `DATABASE_URL` (Optional):
  - If not provided, the application will default to a local SQLite database (`app.db`). Note that SQLite storage on Render is ephemeral (cleared on redeploys) unless you attach a Persistent Volume.
  - To use a persistent database, create a **PostgreSQL** instance on Render and copy its **Internal Database URL** into this environment variable. The app automatically configures itself to use PostgreSQL when `DATABASE_URL` is set.

---

## Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd capstone_project
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```
   Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to interact with the API documentation.
