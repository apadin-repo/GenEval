# GenEval

**GENEVAL** is a modular Python application designed to generate red teaming test scripts and checklists for LLM-based GenAI systems. It helps security analysts perform manual evaluations by aligning test plans with trusted frameworks like NIST AI RMF, MITRE ATLAS, and OWASP Top 10 for LLMs.

---

## 📁 Project Structure

```
GENEVAL/
│
├── main.py                      # Entrypoint: GUI / CLI trigger
├── .env                         # Env vars (API keys, paths)
├── .gitignore
├── README.md
│
├── app/                         # Core application
│   ├── __init__.py
│   ├── app.py                   # app launcher
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # Loads env vars with dotenv
│   ├── ingestion/               # Extract keywords or metadata from user/system description
│   ├── generator/               # Builds test scripts and checklists
│   └── reports/                 # Markdown, Excel, and PDF exporters
│
├── knowledge/                   # Knowledge base (framework documents)
│   ├── docs/                    # NIST, MITRE, Google SAIF in .md/.yaml/.txt format
│   └── run.py                   # Script to create vector DB for RAG
```