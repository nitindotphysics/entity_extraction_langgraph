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
POSTGRES_DB=financial_doc_ai

# FastAPI Configuration
API_HOST=127.0.0.1
API_PORT=8000

# Streamlit Configuration
STREAMLIT_PORT=8501

# Alert Configuration
DEFAULT_ALERT_CHANNEL=EMAIL

# OCR / Parsing Configuration
OCR_ENABLED=true
PARSER_ENGINE=docling

# Environment
ENV=development
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