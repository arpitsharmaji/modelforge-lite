# ModelForge Lite — Setup Instructions (Phase 1)

## What you'll do
Set up your GitHub repo, Hugging Face account, and run the first Colab notebook to prepare the dataset. Nothing gets stored on your Mac — everything runs in the browser and lives in the cloud.

## Step 1 — Create accounts (5 min)
1. **GitHub** — if you don't have one: https://github.com/join
2. **Hugging Face** — https://huggingface.co/join (this is where your models and datasets will live)
3. On Hugging Face, go to https://huggingface.co/settings/tokens and create a new token with **Write** access. Save it somewhere safe — you'll paste it into Colab in a moment.

## Step 2 — Create your GitHub repo
1. Go to https://github.com/new
2. Name it `modelforge-lite`
3. Keep it **Public** (so the CTO can view it, and free hosting services can deploy from it)
4. Click **Create repository**

## Step 3 — Upload the project files
On your repo page, click **Add file > Upload files**, and upload:
- `requirements.txt`
- `01_dataset_setup.ipynb`

Commit directly to the `main` branch.

## Step 4 — Open the notebook in Google Colab
1. Go to https://colab.research.google.com
2. Click **File > Open notebook > GitHub**
3. Paste your repo URL (`https://github.com/YOUR_USERNAME/modelforge-lite`)
4. Select `01_dataset_setup.ipynb`

## Step 5 — Turn on the free GPU
In Colab: `Runtime > Change runtime type > Hardware accelerator > T4 GPU > Save`

(We don't strictly need a GPU for Phase 1, but turn it on now so it's ready for Phase 2 onward.)

## Step 6 — Run the notebook cell by cell
Run each cell in order (Shift+Enter). When you hit the `notebook_login()` cell, paste your Hugging Face token when prompted.

When you reach the "push to Hugging Face Hub" cell, replace `YOUR_HF_USERNAME` with your actual Hugging Face username first.

## What you'll have at the end of Phase 1
- A Hugging Face dataset repo containing three files: `train.csv`, `knowledge_base.csv`, `eval.csv`
- A clear understanding of what each split is for (this matters for the call — see below)

## What to be able to explain on the call
- **Why a subset of intents, not the whole dataset?** Keeps the project focused and the demo easy to reason about — a CTO would rather see a tightly scoped project done well than a broad one done shallowly.
- **Why three separate splits?** This is the difference between a real evaluation and a fake one. If your eval questions leaked into training or into the RAG knowledge base, your fine-tuned model would look artificially good — it'd be "remembering," not "generalizing." Keeping eval strictly held out is what makes your later comparison numbers trustworthy.
- **Why Hugging Face Hub instead of local files?** No local storage needed, and any later notebook (RAG, fine-tuning, eval, deployment) can pull the exact same data with one line of code — reproducibility.

---
Once this phase is running cleanly, come back and we'll do Phase 2: baseline zero-shot evaluation.
