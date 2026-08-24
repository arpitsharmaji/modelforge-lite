# Phase 7 — Deploying the Demo App

## What you're deploying
- **Backend** (`backend/main.py`) — a FastAPI service that serves your precomputed Phase 6 results. Deploys to Render.
- **Frontend** (`frontend/app.py`) — a Streamlit app that calls the backend and shows the 4-way comparison. Deploys to Streamlit Community Cloud.

Both deploy straight from your GitHub repo — nothing runs on your Mac.

## Step 1 — Update the placeholders
Before uploading, open `backend/main.py` and replace `YOUR_HF_USERNAME` with your actual Hugging Face username (same as every previous phase).

You'll update `frontend/app.py`'s `API_BASE_URL` in Step 4, after the backend is deployed and you have its URL.

## Step 2 — Add these files to your GitHub repo
Keep the folder structure:
```
modelforge-lite/
  backend/
    main.py
    requirements.txt
  frontend/
    app.py
    requirements.txt
```
Upload via **Add file > Upload files**, or drag the whole `backend` and `frontend` folders in if your browser supports it.

## Step 3 — Deploy the backend on Render
1. Go to https://render.com and sign up (free) — sign in with GitHub for the easiest setup
2. Click **New > Web Service**
3. Connect your `modelforge-lite` repo
4. Set:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free
5. Click **Create Web Service** and wait for the build to finish (a few minutes)
6. Once live, copy the public URL Render gives you (looks like `https://modelforge-lite-backend.onrender.com`)
7. Visit `<that-url>/summary` in your browser — you should see your summary table as JSON. If you do, the backend is working.

## Step 4 — Point the frontend at your backend
1. Open `frontend/app.py` in your GitHub repo (edit directly in the GitHub web UI is fine)
2. Replace `API_BASE_URL = "https://YOUR-BACKEND-URL.onrender.com"` with the real URL from Step 3
3. Commit the change

## Step 5 — Deploy the frontend on Streamlit Community Cloud
1. Go to https://share.streamlit.io and sign in with GitHub
2. Click **New app**
3. Select your `modelforge-lite` repo, branch `main`, and set **Main file path** to `frontend/app.py`
4. Click **Deploy**
5. Wait a minute or two — you'll get a public URL like `https://your-app.streamlit.app`

## Step 6 — Test it end to end
Open your Streamlit URL. You should see:
- The summary table at the top (avg relevance/faithfulness/latency per variant)
- A dropdown to pick any of the 40 held-out questions
- All four variants' answers displayed side by side with their scores

## One thing to know about Render's free tier
Free Render web services "spin down" after 15 minutes of no traffic, and take 30-60 seconds to wake up on the next request. **Before your call with Irfan, open your Streamlit app yourself a few minutes early** to wake the backend up, so it's instant when he clicks through it live. This is worth mentioning if he asks about production readiness — it's a free-tier limitation, not a design flaw, and you can name it directly ("on a paid tier this would stay warm, or I'd add a scheduled ping to keep it alive").

## What to be able to explain on the call
- **Why precomputed results instead of live generation?** Your RAG variants averaged 48-64 seconds per answer — too slow for a responsive demo and risky against free-tier request timeouts. Serving precomputed, real evaluation results keeps the demo fast and reliable while still showing genuine model outputs, not mockups.
- **How would you make it live in production?** You'd move generation to an async job queue (e.g. Celery + Redis — which is already in your stated skill set) so the API responds immediately with a job ID, and the frontend polls or gets pushed the result when ready, instead of holding a request open for a minute.
