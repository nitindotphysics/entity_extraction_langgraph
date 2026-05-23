# Financial Document AI Workflow Platform

AI-powered financial document processing platform using:

- FastAPI
- Streamlit
- LangGraph
- PostgreSQL
- Docker
- Docling
- PaddleOCR

---

# Project Setup

## 1. Clone or Extract Project

```bash
cd financial_doc_ai
```

---

# 2. Create Virtual Environment

## Mac/Linux

```bash
python3 -m venv venv
```

## Windows

```bash
python -m venv venv
```

---

# 3. Activate Virtual Environment

## Mac/Linux

```bash
source venv/bin/activate
```

## Windows

```bash
venv\Scripts\activate
```

---

# 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 5. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
# OpenAI / LLM Configuration
OPENAI_API_KEY=your_openai_api_key

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/financial_doc_ai
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=financial_doc_ai
```

Update all values with your own credentials/configuration before running the project.

---

# 6. Start PostgreSQL using Docker

```bash
docker compose up -d
```

Verify container is running:

```bash
docker ps
```

You should see:

```text
financial_doc_postgres
```

---

# 7. Start FastAPI Backend

```bash
uvicorn app.api.main:app --reload
```

Backend will run on:

```text
http://127.0.0.1:8000
```

Swagger API Docs:

```text
http://127.0.0.1:8000/docs
```

---

# 8. Start Streamlit UI

Open a NEW terminal.

Activate virtual environment again:

## Mac/Linux

```bash
source venv/bin/activate
```

## Windows

```bash
venv\Scripts\activate
```

Run Streamlit:

```bash
streamlit run app/ui/dashboard.py
```

UI will run on:

```text
http://localhost:8501
```

---

# Project Workflow

1. Upload financial documents from UI
2. FastAPI triggers LangGraph workflow
3. OCR + parsing + classification executed
4. Entities extracted and normalized
5. Alerts generated
6. Results stored in PostgreSQL
7. Investigation + Observability dashboards updated

---

# Important Files to Configure

| File | Purpose |
|---|---|
| `.env` | API keys and DB configs |
| `docker-compose.yml` | PostgreSQL container config |
| `requirements.txt` | Python dependencies |

---

# Stop Project

## Stop Streamlit / FastAPI

Press:

```text
CTRL + C
```

in terminal.

---

# Stop PostgreSQL Container

```bash
docker compose down
```

---

# Reset Database Completely

WARNING: This deletes all stored data.

```bash
docker compose down -v
```

# Demo Files Included

Sample demo documents are available in:

```text
data/input/
```

These files can be directly used to test the workflow and dashboards.

Examples:
- Bank Statements
- AML Reports
- Loan Agreements
- Invoice Documents

---

# Important Note on Entity Extraction

Currently, entity extraction is implemented ONLY for:

```text
Bank Statement Documents
```

The workflow extracts:
- Customer Details
- Account Information
- Transactions
- Balances
- Financial Alerts

from bank statement PDFs.

---

# Workflow Behavior for Non-Bank Documents

The LangGraph workflow processes all uploaded documents through:
- OCR
- Parsing
- Quality Check
- Classification

However, for NON-bank-statement documents:

```text
Entity Extraction Node is skipped
```

This means:
- document still appears in dashboards
- workflow still executes successfully
- classification still occurs

BUT:
- normalized entities are not generated
- financial transaction extraction does not occur
- alert generation is skipped

---

# Important Testing Guidance

If you want to test:
- entity extraction
- normalization
- alert generation
- investigation dashboard

then upload:
# bank statement documents only

Use the sample bank statement PDFs available in:

```text
data/input/
```

for best demo/testing results.
