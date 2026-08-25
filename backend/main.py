"""
ModelForge Lite — FastAPI backend

Serves the precomputed 4-variant comparison results from Phase 6.
Deliberately does NOT run live model inference — the RAG variants averaged
48-64s per answer in testing, which exceeds typical free-tier request
timeouts. Serving precomputed results keeps the demo instant and reliable
for a live call, while still showing real model outputs (not mockups).
"""

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import hf_hub_download

HF_USERNAME = "YOUR_HF_USERNAME"  # replace with your Hugging Face username
DATASET_REPO = f"{HF_USERNAME}/modelforge-lite-support-data"

app = FastAPI(title="ModelForge Lite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Loaded once at startup — small CSVs, no models, no GPU needed
_scored_df = None
_summary_df = None


@app.on_event("startup")
def load_data():
    global _scored_df, _summary_df
    scored_path = hf_hub_download(
        repo_id=DATASET_REPO, filename="results/full_eval_scored.csv", repo_type="dataset"
    )
    summary_path = hf_hub_download(
        repo_id=DATASET_REPO, filename="results/eval_summary.csv", repo_type="dataset"
    )
    _scored_df = pd.read_csv(scored_path)
    _summary_df = pd.read_csv(summary_path)
    print(f"Loaded {len(_scored_df)} scored questions and summary table.")


@app.get("/")
def root():
    return {"status": "ok", "service": "ModelForge Lite API"}


@app.get("/questions")
def list_questions():
    """Return all eval questions with their row index, for the frontend dropdown."""
    return [
        {"id": int(i), "question": str(row["question"]), "intent": str(row.get("intent", ""))}
        for i, row in _scored_df.iterrows()
    ]


@app.get("/compare/{question_id}")
def compare(question_id: int):
    """Return all four variants' answers, scores, and latency for one question."""
    if question_id < 0 or question_id >= len(_scored_df):
        raise HTTPException(status_code=404, detail="question_id out of range")

    row = _scored_df.iloc[question_id]

    def variant_data(prefix):
        return {
            "answer": str(row[f"{prefix}_answer"]),
            "relevance": int(row[f"{prefix}_relevance"]),
            "faithfulness": int(row[f"{prefix}_faithfulness"]),
            "latency_sec": float(row[f"{prefix}_latency_sec"]),
        }

    return {
        "question": str(row["question"]),
        "intent": str(row.get("intent", "")),
        "variants": {
            "base_model": variant_data("base_model"),
            "rag": variant_data("rag"),
            "finetuned": variant_data("finetuned"),
            "finetuned_rag": variant_data("finetuned_rag"),
        },
    }


@app.get("/summary")
def summary():
    """Return the averaged summary table across all 40 questions — the 'punchline' data."""
    return _summary_df.to_dict(orient="records")
