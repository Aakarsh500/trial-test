# Step-by-Step Render Hosting Guide

This guide explains how your project folder was prepared for Render, how to complete the hosting process on the Render dashboard, and how to access your API documentation.

---

## Part 1: Folder Preparation (Completed)

The following modifications were made to prepare your project for Render:

1. **Created `requirements.txt`**: Added all Python dependencies required to run the API on Render, including:
   - `fastapi` and `uvicorn[standard]`
   - `sqlalchemy` (with `psycopg2-binary` for PostgreSQL compatibility)
   - `python-jose[cryptography]` and `passlib[bcrypt]` for secure JWT authentication
   - `python-multipart` to support Form-based logins
2. **Created `.gitignore`**: Excluded temporary files (`__pycache__`), virtual environments (`test_env`), and local database files (`app.db`) from being uploaded to Git.
3. **Updated [database.py](file:///c:/Users/Aakarsh/Documents/fastapi-course-udemy/Section%2006%20-%20Capstone%20Secure%20User%20Auth%20API/capstone_project/database.py)**: Configured the database connection string to read from the `DATABASE_URL` environment variable, while defaulting to a local SQLite database for development.
4. **Updated [security.py](file:///c:/Users/Aakarsh/Documents/fastapi-course-udemy/Section%2006%20-%20Capstone%20Secure%20User%20Auth%20API/capstone_project/security.py)**: Refactored the signature validation key to load from the `SECRET_KEY` environment variable.

---

## Part 2: Step-by-Step Render Deployment Guide

Follow these steps to host your application on Render:

### Step 1: Push Changes to GitHub
Make sure all changes in this folder are pushed to your GitHub repository:
`https://github.com/Aakarsh500/trial-test` *(Already completed)*.

### Step 2: Create a Web Service on Render
1. Sign in to your [Render Dashboard](https://dashboard.render.com/).
2. Click the blue **New +** button in the top right and select **Web Service**.
3. Under **Connect a repository**, select your repository: `Aakarsh500/trial-test`. (If it is not visible, click *Connect window* to authorize Render on your GitHub account).

### Step 3: Configure Web Service Settings
Fill in the deployment details:
- **Name**: `capstone-auth-api` (or any name you prefer)
- **Region**: Choose the region closest to you (e.g., Oregon, Frankfurt, Singapore)
- **Branch**: `main`
- **Root Directory**: Leave blank (defaults to project root)
- **Runtime**: `Python 3` (or Python)
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```
- **Instance Type**: Select **Free** (or your preferred paid tier)

### Step 4: Configure Environment Variables
Scroll down to the **Environment** section (or click the **Environment** tab on the left menu after creating) and add the following two key-value pairs:

| NAME_OF_VARIABLE | value |
| :--- | :--- |
| `SECRET_KEY` | `SUPER_SECRET_RANDOM_STRING_HERE` |
| `DATABASE_URL` | `sqlite:///./app.db` |

*Note: If you wish to use a persistent PostgreSQL database on Render later, you can create a PostgreSQL service on Render and swap the `DATABASE_URL` value with your database's **Internal Database URL**.*

### Step 5: Deploy
Click **Deploy Web Service** at the bottom of the page.

---

## Part 3: Accessing the API & `/docs`

1. **Watch the Build Logs**: Render will start installing dependencies and building your app. Wait until the logs show:
   ```text
   ==> Docs on dev-center: https://render.com/docs/deploy-fastapi
   ==> Uploading build...
   ==> Deploying...
   ==> Your service is live ✨
   ```
2. **Get your Live URL**: Near the top-left of the Render dashboard, you will find your application's public URL (it will look like `https://capstone-auth-api.onrender.com`).
3. **Open API Documentation**:
   - Click the link, or copy it into your browser.
   - Append `/docs` to the end of the URL (e.g., `https://capstone-auth-api.onrender.com/docs`).
   - You should see the interactive Swagger UI showing your endpoints (`/register`, `/login`, `/users/me`, `/logout`).
4. **Test the Hosted API**:
   - Expand the `/register` endpoint, click **Try it out**, fill in user details, and click **Execute**.
   - Expand the `/login` endpoint, click **Try it out**, enter the registered email as username and password, and click **Execute** to initialize a secure session.
