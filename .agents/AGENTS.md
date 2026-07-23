# Workspace Rules for AI AE Assignments

Refer to [agent.md](file:///d:/My%20documents/My%20Projects/AI_AE_Assigment/agent.md) for full guidelines on completing upcoming assignments.

## Core Rules Summary
1. **CRITICAL: Environment & Credentials Auditing**:
   - **Never assume API keys or environment variables exist** to finish tasks fast.
   - Always check `.env` (and compare against `.env.example` or assignment instructions).
   - **If any key is missing or empty in `.env`, MUST explicitly notify the user** and ask for input/key details.
   - Ensure all details are completed accurately and completely without shortcutting.
2. **Directory & Naming**:
   - Place assignments in `WeekX/` folders.
   - Name scripts: `Assignment XX - <Descriptive Title>.py` (padded 2-digit index).
   - Report file: `readme.txt` per week.
3. **Code Structure**:
   - Line 1 header: `# Assignment XX - <Descriptive Title> in Python`.
   - Lightweight `load_env()` checking `[".env", "../.env"]`.
   - Non-interactive automated execution with mock data.
   - Defensive imports with troubleshooting guides.
4. **Resiliency & AI Architecture**:
   - Exponential retries (`tenacity`) on OpenAI API errors.
   - RAG / Vector search using ChromaDB / Pinecone & `text-embedding-3-small`.
   - Hybrid rule + LLM classification.
5. **Documentation**:
   - `readme.txt` covering Approach, Challenges Faced, How to Run, and Sample Outputs / Technical Explanations.
