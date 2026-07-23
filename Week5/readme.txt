Week 5 Assignments

This directory contains 2 python projects for Week 5.

Project Structure
- Assignment 13 - Patient Information Collection and Advisory Chatbot Agent.py: AI patient information collection and health advisory chatbot using LangGraph, AzureChatOpenAI/OpenAI, FAISS retriever, and Tavily web search tool.
- Assignment 14 - Retail RAG Chatbot.py: LangGraph & FAISS RAG chatbot for Walmart product and policy support.
- readme.txt: Comprehensive documentation of approach, design choices, challenges, how to run, and sample outputs for Week 5 assignments.


Assignment 13: Patient Information Collection and Advisory Chatbot Agent

Approach / Design Choices
1. Conversational Dialogue State Management with LangGraph: Built a StateGraph workflow using MessagesState to control dialogue flow, managing user queries, model responses, conditional tool routing, and agent execution nodes.
2. Dual Knowledge RAG Architecture: Combined internal FAISS vector search (`retrieve_advice`) initialized with clinical mock guidelines and real-time web search (`tavily_search_tool`) for supplemental health context.
3. System Prompt Persona & Information Gathering: Formulated a clinical assistant prompt instructing the agent to interactively collect patient Name, Age, Symptoms, and Duration before issuing advice.
4. Resilient Network & API Integration: Utilized `tenacity` exponential backoff retries for LLM invocation. Enforced strict error raising when `TAVILY_API_KEY` is missing or invalid.

Challenges Faced / Challenges & Limitations
1. LangChain Module Deprecation & Version Compatibility: Updated imports from deprecated `langchain.docstore.document` to `langchain_core.documents` and `langchain_core.tools`.
2. Multi-turn Tool Invocation Context: Ensured message history is updated properly across graph iterations so tool calls (`retrieve_advice`, `tavily_search_tool`) execute conditionally when patient details are provided.

How to Run
1. Setup virtual environment:
   python -m venv .venv
2. Install dependencies:
   .\.venv\Scripts\pip.exe install langchain langchain-openai langchain-community langgraph faiss-cpu tavily-python tenacity openai
3. Execute assignment:
   python "Week5/Assignment 13 - Patient Information Collection and Advisory Chatbot Agent.py"


Real Execution Outputs / Interactive Dialogue Logs

Scenario 1: Sore Throat & Fever (2-Turn Interactive Intake)
--------------------------------------------------------------------------------
Turn 1:
Patient: Hello doctor bot, I feel really unwell. I've had a sore throat and fever.
AI Chatbot: I'm sorry to hear that you're feeling unwell. To provide you with the best possible advice, could you please share your name, age, and how long you've been experiencing these symptoms?

Turn 2:
Patient: My name is John Doe, I am 34 years old, and these symptoms started 3 days ago.
  [Tool Call] retrieve_advice tool calling for: 'sore throat and fever for 3 days'

AI Chatbot:
Thank you for providing your details, John. Based on your symptoms of a sore throat and fever lasting for 3 days, here are some preliminary health advice and self-care steps you can consider:

### Self-Care Steps:
1. Stay Hydrated: Drink plenty of warm fluids, such as herbal teas or broths, to soothe your throat and stay hydrated.
2. Gargle with Salt Water: This can help reduce throat inflammation and discomfort.
3. Rest: Ensure you get plenty of rest to help your body recover.
4. Avoid Irritants: Stay away from smoke and other irritants that can worsen your throat.

### Potential Causes:
- Viral infections (like the common cold or flu)
- Bacterial infections (like strep throat)
- Allergies or irritants

### Red Flag Warnings:
Please seek urgent medical attention if you experience any of the following:
- Severe chest pain
- Shortness of breath
- Sudden confusion
- High fever over 39°C (102.2°F)

### Disclaimer:
This advice is preliminary and should not replace evaluation by a qualified medical professional. If your symptoms persist or worsen, please consult a healthcare provider.


Scenario 2: Dizziness & Fatigue (2-Turn Intake & Consultation)
--------------------------------------------------------------------------------
Turn 1:
Patient: Hi, I'm Sarah Connor, age 28. For the past week, I've been feeling extremely dizzy and tired whenever I stand up.
AI Chatbot: Thank you for sharing that information, Sarah. Before I proceed to provide you with some preliminary health advice, could you please confirm if there are any other symptoms you are experiencing, or if there are any specific details you think might be relevant?

Turn 2:
Patient: No other pre-existing health conditions or symptoms, just dizziness when standing up and fatigue.
  [Tool Call] retrieve_advice tool calling for: 'dizziness and fatigue when standing up'

AI Chatbot:
Thank you for the additional information, Sarah. Based on your symptoms of dizziness and fatigue when standing up, here are some preliminary health advice and considerations:

### Self-Care Steps:
1. Hydration: Ensure you are drinking enough fluids throughout the day. Dehydration can contribute to dizziness and fatigue.
2. Position Changes: When standing up, do so slowly to allow your body to adjust.
3. Nutrition: Ensure you are getting enough iron and other essential nutrients.
4. Rest: Make sure you are getting adequate sleep and rest to help combat fatigue.

### Potential Causes:
- Orthostatic Hypotension: Blood pressure drops significantly when standing up, leading to dizziness.
- Dehydration: Not drinking enough fluids can lead to both dizziness and fatigue.
- Nutritional Deficiencies: Low iron levels or other deficiencies can cause fatigue and dizziness.
- Thyroid Issues: An underactive thyroid can lead to fatigue.

### Red Flag Warnings:
- Seek immediate medical attention if dizziness worsens, is accompanied by fainting, severe headache, chest pain, or difficulty breathing.

### Disclaimer:
Please remember that this advice is preliminary and not a substitute for a thorough evaluation by a qualified medical professional.

================================================================================


Assignment 14: Retail RAG Chatbot

Approach / Design Choices
1. LangGraph StateGraph Orchestration: Structured the RAG application as a two-stage Graph workflow (RAGState -> retrieve node -> generate node -> END). This guarantees deterministic control flow and explicit context state passing.
2. Dense Vector Indexing via FAISS: Hardcoded 15 Walmart retail policy and product documents into a FAISS in-memory vector store powered by `text-embedding-3-small` (1536 dims) for cosine similarity retrieval (k=2).
3. Dual-Endpoint Resilience & Tenacity Retries: Wrapped network API calls with `tenacity` exponential backoff retries and built an API wrapper supporting both AzureChatOpenAI/AzureOpenAIEmbeddings and standard OpenAI proxy endpoints.
4. Non-Interactive Automated Evaluation: Implemented automated headless execution across 5 realistic customer/employee query scenarios.

Challenges Faced / Challenges & Limitations
1. Synthesizing Overlapping Return Rules: Queries regarding electronics without a receipt retrieved Doc 1 (30-day electronics return with receipt) and Doc 7 (no-receipt store credit). Prompt engineering was refined to instruct the LLM to synthesize both policies without contradiction.
2. In-Memory Vector Store Scope: FAISS in-memory store is local and ephemeral. In enterprise deployment, this would be replaced by ChromaDB, Azure AI Search, or Pinecone with real-time CMS synchronization.

How to Run
1. Setup virtual environment:
   python -m venv .venv
2. Install dependencies:
   .\.venv\Scripts\pip.exe install langchain langchain-openai langchain-community langgraph faiss-cpu tenacity openai
3. Execute assignment:
   python "Week5/Assignment 14 - Retail RAG Chatbot.py"


Real Execution Outputs & Evaluation Results

================================================================================
  SCENARIO 1: "Can I return a Walmart bicycle if I've ridden it outdoors?"
================================================================================
--- RETRIEVED CONTEXT ---
[Doc 13]: Bicycles purchased at Walmart can be returned within 90 days if not used outdoors and with all accessories present.
[Doc 15]: Walmart reserves the right to deny returns suspected of fraud or abuse.

--- GENERATED ANSWER ---
No, you cannot return a Walmart bicycle if you have ridden it outdoors. According to the policy, bicycles can only be returned within 90 days if they have not been used outdoors and all accessories are present.
--------------------------------------------------------------------------------

================================================================================
  SCENARIO 2: "What is the return policy for electronics if I don't have a receipt?"
================================================================================
--- RETRIEVED CONTEXT ---
[Doc 1]: Walmart customers may return electronics within 30 days with a receipt and original packaging.
[Doc 7]: If a Walmart customer does not have a receipt, most returns are eligible for store credit with valid photo identification.

--- GENERATED ANSWER ---
If you don't have a receipt for returning electronics at Walmart, you may still be eligible for store credit, provided you have valid photo identification. However, please note that the standard return policy for electronics allows returns within 30 days with a receipt and original packaging.
--------------------------------------------------------------------------------

================================================================================
  SCENARIO 3: "Are prescription medications purchased at Walmart eligible for return or exchange?"
================================================================================
--- RETRIEVED CONTEXT ---
[Doc 5]: Prescription medications purchased at Walmart are not eligible for return or exchange.
[Doc 9]: Walmart Vision Center purchases may be returned or exchanged within 60 days with a receipt.

--- GENERATED ANSWER ---
No, prescription medications purchased at Walmart are not eligible for return or exchange, as stated in the policy: "Prescription medications purchased at Walmart are not eligible for return or exchange."
--------------------------------------------------------------------------------

================================================================================
  SCENARIO 4: "How does free shipping work for Walmart Plus members?"
================================================================================
--- RETRIEVED CONTEXT ---
[Doc 4]: Walmart Plus members get free shipping with no minimum order amount.
[Doc 14]: For online Walmart orders, customers can return items in store or by mail using the prepaid label.

--- GENERATED ANSWER ---
Walmart Plus members enjoy free shipping with no minimum order amount. This means that as a member, you can place an order of any size and qualify for free shipping on your items.
--------------------------------------------------------------------------------

================================================================================
  SCENARIO 5: "What requirements must be met to return an open-box item or a cell phone?"
================================================================================
--- RETRIEVED CONTEXT ---
[Doc 6]: Open-box items are eligible for return at Walmart within the standard return period, but must include all original accessories.
[Doc 10]: Returns on cell phones at Walmart require the device to be unlocked and all personal data erased.

--- GENERATED ANSWER ---
To return an open-box item at Walmart, it must be within the standard return period and include all original accessories. For returning a cell phone, the device must be unlocked and all personal data must be erased.
--------------------------------------------------------------------------------

Reflection on RAG vs. Traditional FAQs / Keyword Search:
1. Beyond Keyword Matching: Traditional keyword search fails when user queries use different phrasing (e.g. "ridden outdoors" vs "used outdoors"). Vector embeddings capture semantic intent.
2. Grounded & Hallucination-Free Synthesis: Instead of providing static generic FAQ answers, RAG synthesizes exact matching policies directly into a human-friendly response while staying grounded in enterprise facts.
3. Operational Efficiency: Reduces call-center and in-store service desk handling times by instantly delivering accurate, context-aware policy answers.

Suggestions for Future Expansion:
- Multi-Turn Conversational Memory: Add persistent thread checkpointers using LangGraph `MemorySaver` for natural follow-up questions.
- Hybrid Retrieval (Sparse + Dense): Combine BM25 keyword matching with FAISS vector search to capture exact model numbers and warranty SKUs.
- Enterprise Database Integration: Connect RAG retriever to real-time inventory, user purchase history, and barcode scanners for instant barcode-level return verification.

