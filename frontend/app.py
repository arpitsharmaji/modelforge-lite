"""
ModelForge Lite — Streamlit demo app

Pick a question from the held-out eval set and see all four model variants'
real, precomputed answers side by side, with their relevance/faithfulness
scores and latency. Talks to the FastAPI backend, which serves precomputed
Phase 6 results (see backend/main.py for why this is precomputed rather
than live inference).
"""

import requests
import streamlit as st
import pandas as pd

API_BASE_URL = "https://YOUR-BACKEND-URL.onrender.com"  # replace after deploying the backend

st.set_page_config(page_title="ModelForge Lite", layout="wide")

st.title("ModelForge Lite")
st.caption(
    "Base model vs RAG vs Fine-tuned vs Fine-tuned+RAG — "
    "a real comparison on held-out customer support questions."
)

VARIANT_LABELS = {
    "base_model": "Base Model (zero-shot)",
    "rag": "Base + RAG",
    "finetuned": "Fine-tuned (LoRA)",
    "finetuned_rag": "Fine-tuned + RAG",
}


@st.cache_data(ttl=3600)
def fetch_questions():
    resp = requests.get(f"{API_BASE_URL}/questions", timeout=15)
    resp.raise_for_status()
    return resp.json()


@st.cache_data(ttl=3600)
def fetch_summary():
    resp = requests.get(f"{API_BASE_URL}/summary", timeout=15)
    resp.raise_for_status()
    return resp.json()


def fetch_comparison(question_id):
    resp = requests.get(f"{API_BASE_URL}/compare/{question_id}", timeout=15)
    resp.raise_for_status()
    return resp.json()


# --- Summary table at the top ---
st.subheader("Overall results across 40 held-out questions")
try:
    summary_data = fetch_summary()
    summary_df = pd.DataFrame(summary_data)
    summary_df["variant"] = summary_df["variant"].map(VARIANT_LABELS).fillna(summary_df["variant"])
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Could not load summary — is the backend URL set correctly? ({e})")
    st.stop()

st.divider()

# --- Question picker ---
st.subheader("Compare answers on a specific question")
questions = fetch_questions()
question_labels = [f"{q['id']}: {q['question'][:80]}" for q in questions]
selected_label = st.selectbox("Pick a held-out question:", question_labels)
selected_id = int(selected_label.split(":")[0])

comparison = fetch_comparison(selected_id)

st.markdown(f"**Question:** {comparison['question']}")
if comparison.get("intent"):
    st.caption(f"Intent: {comparison['intent']}")

cols = st.columns(4)
for col, (variant_key, label) in zip(cols, VARIANT_LABELS.items()):
    data = comparison["variants"][variant_key]
    with col:
        st.markdown(f"**{label}**")
        st.markdown(
            f"Relevance: `{data['relevance']}/5` &nbsp;|&nbsp; "
            f"Faithfulness: `{data['faithfulness']}/5` &nbsp;|&nbsp; "
            f"Latency: `{data['latency_sec']}s`"
        )
        st.info(data["answer"])

st.divider()
st.caption(
    "Answers shown here are real model outputs from evaluation runs, "
    "not generated live — see the project README for why."
)
