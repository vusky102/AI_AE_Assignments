# Agent Guide: AI AE Assignments Guidelines & Blueprint

This document serves as the official specification and guideline for completing upcoming assignments in the **AI Application Engineer (AI AE)** course. All future scripts, project structures, code formatting, and documentation must adhere strictly to the conventions established across Weeks 1 to 3.

---

## 0. MANDATORY RULE: No Assumptions & Environment Auditing

> [!CRITICAL]
> **NEVER ASSUME CREDENTIALS OR ENVIRONMENT VARIABLES EXIST.**
> 1. **Do Not Rush Completion with Assumptions**: Never assume API keys, services, or credentials exist just to finish a task quickly.
> 2. **Audit `.env` and `.env.example`**: Before implementing or executing any assignment requiring external services, check `.env` and compare against `.env.example` (or assignment instructions) to verify all required variables are present.
> 3. **Prompt User when Credentials are Missing**: If a required API key or environment variable (e.g. `PINECONE_API_KEY`, `TAVILY_API_KEY`, `OPENWEATHERMAP_API_KEY`) is missing or unconfigured in `.env`, **YOU MUST EXPLICITLY TELL THE USER WHICH VARIABLE IS MISSING** and ask for input or clarification before declaring the task finished.
> 4. **Complete All Details Accurately**: All core assignment requirements and integration steps must be executed fully and correctly without skipping steps or relying silently on mock fallbacks when live credentials are required.

---

## 1. Directory Structure & File Naming Conventions

### Workspace Layout
All assignments are organized by week in dedicated directories:
```
AI_AE_Assignments/
├── Week1/
│   ├── Assignment 01 - Command-Line Task Manager.py
│   ├── Assignment 02 - Prompt-Driven Work Instructions.py
│   ├── Assignment 03 - AI-Powered Meeting Summarizer.py
│   └── readme.txt
├── Week2/
│   ├── Assignment 04 - Efficient OpenAI API Usage.py
│   ├── Assignment 05 - Local Resume Generator.py
│   ├── Assignment 06 - Delay Reason Classification.py
│   └── readme.txt
├── Week3/
│   ├── Assignment 07 - TTS Inference.py
│   ├── Assignment 08 - Clothing Search.py
│   ├── Assignment 09 - Laptop Consultant.py
│   ├── output.wav
│   └── readme.txt
├── Week4/
│   ├── Assignment 10 - Pinecone Product Similarity Search.py
│   ├── Assignment 11 - AI Agent for Weather and Search.py
│   ├── Assignment 12 - Satellite Image Cloud Detection via AzureOpenAI Inference.py
│   └── readme.txt
└── .env (Root environment configuration file)
```

### Naming Standards
- **Python Assignment Files:** `Assignment XX - <Descriptive Assignment Name>.py`
  - Index must be zero-padded to 2 digits (`01`, `02`, ..., `10`, `11`).
  - Title Case with clean space hyphen space separators (e.g. `Assignment 10 - Pinecone Product Similarity Search.py`).
- **Weekly Report:** `readme.txt`
  - Plain text file placed in each `WeekX/` directory summarizing all assignments of that week.
- **Environment File:** `.env` located at root level.

---

## 2. Code Architecture & Programming Patterns

### Standard File Header
Every assignment Python script MUST begin with a standardized single-line comment header:
```python
# Assignment XX - <Descriptive Assignment Name> in Python
```

### Environment Configuration (`load_env`) & Key Validation
Do not mandate external dependencies like `python-dotenv` for basic environment loading. Every script requiring environment variables must incorporate the lightweight `load_env()` helper and validate keys explicitly:
```python
import os

def load_env():
    """Reads environment variables from .env file in current or parent directory."""
    paths = [".env", "../.env"]
    for path in paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    parts = line.split("=", 1)
                    key = parts[0].strip()
                    val = parts[1].strip().strip('"').strip("'")
                    os.environ[key] = val
            break

load_env()

def check_required_env_vars(keys):
    """Audits required keys and notifies missing credentials."""
    missing = [k for k in keys if not os.getenv(k)]
    if missing:
        print(f"[ENVIRONMENT NOTICE] Missing environment variables: {', '.join(missing)}")
        print("Please configure them in your .env file.")
```

### OpenAI & Model API Initialization
Construct API clients dynamically using environment configuration:
```python
from openai import OpenAI

openai_key = os.getenv("OPENAI_API_KEY")
openai_base = os.getenv("OPENAI_API_BASEURL")
openai_model = os.getenv("OPENAI_API_MODEL", "gpt-4o-mini")

client = OpenAI(
    api_key=openai_key,
    base_url=openai_base
)
```

### Defensive Import Handling
Wrap optional or specialized library imports (e.g., `torch`, `chromadb`, `scipy`, `llama_cpp`, `transformers`) in `try-except` blocks with clear error outputs and troubleshooting installation commands:
```python
import sys

try:
    import chromadb
    from openai import OpenAI
except ImportError as e:
    print(f"Error: Missing prerequisites. {e}")
    print("Troubleshooting: Please ensure you are running inside the configured virtual environment with required packages installed.")
    sys.exit(1)
```

### Automated Mock Data & Headless Execution
- Scripts must run non-interactively to facilitate automated evaluation.
- Include a set of 3 to 10 sample mock records or automated user query lists inside `if __name__ == "__main__":` or top-level definitions.
- Format console output clearly with dividers (e.g. `print("=" * 60)` and `print("-" * 110)`).

---

## 3. Resiliency & Advanced AI Design Patterns

1. **Rate Limiting & Retries (`tenacity`)**:
   - For batch processing or remote API tasks, wrap network calls using `tenacity` exponential backoff decorators:
   ```python
   from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
   from openai import RateLimitError, APIError

   @retry(
       retry=retry_if_exception_type((RateLimitError, APIError)),
       wait=wait_random_exponential(min=1, max=10),
       stop=stop_after_attempt(5),
       reraise=True
   )
   def call_api_with_retry(...):
       ...
   ```

2. **Structured Outputs & Hybrid Pipelines**:
   - For classification or structured extraction, use function schemas (`functions` / `tools` parameter) or system instructions with `temperature=0.0`.
   - Prefer hybrid 2-stage architectures: Stage 1 (Fast rule/keyword pre-classifier) -> Stage 2 (LLM verification/refinement).

3. **Semantic Search & RAG Best Practices**:
   - Embeddings: Standard model `"text-embedding-3-small"` (1536 dimensions).
   - Distance Metrics: Use cosine similarity / cosine distance (`scipy.spatial.distance.cosine` or ChromaDB native distance).
   - Context Injection: Retrieve top N matching documents (e.g. N=3) and construct structured context strings to ground LLM completions and prevent hallucination.

4. **Local Hardware Constraints & Local LLMs**:
   - CPU-only execution fallback (e.g. PyTorch CPU build, `llama-cpp-python` CPU wheel).
   - Use quantized lightweight models (`Llama-3.2-1B-Instruct-Q4_K_M.gguf` or similar) when local inference is required.

---

## 4. `readme.txt` Documentation Standard

Every week directory must contain a comprehensive plain-text `readme.txt` file structured as follows:

```
Week X Assignments

This directory contains <N> python projects for Week X.

Project Structure
- Assignment XX - <Name>.py: <Short 1-sentence description>
- Assignment YY - <Name>.py: <Short 1-sentence description>
- readme.txt: Simplified description of the approach, design, and challenges.


Assignment XX: <Title>

Approach / Design Choices
1. <Architectural decision 1>
2. <Architectural decision 2>
3. <Architectural decision 3>

Challenges Faced / Challenges & Limitations
1. <Challenge encountered and resolution/workaround>
2. <Performance or hardware limitation insight>

How to Run
1. Setup virtual environment:
   python -m venv .venv
2. Install dependencies:
   .venv\Scripts\pip.exe install <packages>
3. Execute assignment:
   python "Assignment XX - <Name>.py"


[Optional Section] Sample Outputs / Comparison Table / Theoretical Q&A
<Provide exact execution table logs, or conceptual comparisons (e.g., Hybrid Classification vs RAG, Cosine Similarity benefits, Vector DB RAG advantages)>
```

---

## 5. Pre-Flight Checklist for New Assignments

Before considering an assignment complete:
- [ ] Checked `.env` vs `.env.example` for required variables; explicitly notified user of any missing API keys.
- [ ] Folder follows `WeekX/` format.
- [ ] Script named `Assignment XX - <Title>.py` with 2-digit zero padding.
- [ ] Python header comment on line 1 matches `# Assignment XX - <Title> in Python`.
- [ ] Environment loading via `load_env()` implemented.
- [ ] Non-interactive mock input data included for standard automated run.
- [ ] Resiliency (retries/error handling) included for API/hardware calls.
- [ ] Console logs formatted clearly with header/footer borders.
- [ ] Plain-text `readme.txt` generated covering Approach, Challenges Faced, How to Run, and Sample Outputs / Technical Analysis.
