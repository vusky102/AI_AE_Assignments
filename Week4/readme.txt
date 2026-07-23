Week 4 Assignments

This directory contains three python projects for Week 4 focusing on Vector Similarity Search (Pinecone), Autonomous ReAct AI Agents (LangChain/LangGraph), and Multimodal Visual Scene Analysis (Azure OpenAI).

Project Structure
- Assignment 10 - Pinecone Product Similarity Search.py: Main script to initialize Pinecone, generate product embeddings using OpenAI text-embedding-3-small, upsert vector records, and perform similarity search for top-k results.
- Assignment 11 - AI Agent for Weather and Search.py: Autonomous ReAct AI agent using LangChain and LangGraph to dynamically call weather and web search tools.
- Assignment 12 - Satellite Image Cloud Detection via AzureOpenAI Inference.py: Visual classification of satellite imagery into 'Cloudy' or 'Clear' with confidence scores using Azure OpenAI GPT-4o-mini and LangChain structured outputs.
- readme.txt: Comprehensive documentation detailing the solution approach, step-by-step resolution, technical references, and execution results for Week 4 assignments.


Assignment 10: Pinecone Product Similarity Search Engine

Design Choices
1. Pinecone Vector Database Integration: Utilized the official Pinecone Python client to initialize client connections, manage serverless vector indexes (`product-similarity-index`) configured with 1536 dimensions, and perform fast vector upsert and top-k query operations.
2. Embedding Generation & Metadata Storage: Mapped product titles and descriptions to 1536-dimensional vectors using OpenAI's `text-embedding-3-small` model. Stored title and description metadata alongside vector IDs (`prod1` through `prod5`) for direct metadata retrieval.
3. Resilient Error-Handling Architecture: Embedded `tenacity` exponential retry backoffs for API calls. Enforced strict environment auditing and error raising when `PINECONE_API_KEY` is missing or invalid.

Challenges Faced
1. Pinecone SDK Package Transition: Legacy guides reference `pinecone-client`, which raises deprecation exceptions in modern environments. Upgraded dependencies to the official `pinecone` SDK (v9.1+) to ensure clean initialization.
2. Index Metric & Dimension Alignment: Configured Pinecone serverless index with `dimension=1536` and `metric="cosine"` to align precisely with OpenAI `text-embedding-3-small` output vectors.

How to Run
1. Create virtual environment and install dependencies:
   python -m venv .venv
   .venv\Scripts\pip.exe install pinecone openai scipy tenacity
2. Configure credentials in root `.env` file:
   OPENAI_API_KEY, OPENAI_API_BASEURL, OPENAI_API_MODEL, PINECONE_API_KEY
3. Execute the assignment script:
   ..\.venv\Scripts\python.exe "Assignment 10 - Pinecone Product Similarity Search.py"

Real Similarity Search Results (Pinecone Cloud Execution Output)
Query 1: 'clothing item for summer'
Rank #1 [Score: 0.3497] | ID: prod1 | Title: Red T-Shirt
Rank #2 [Score: 0.3483] | ID: prod5 | Title: Green Hoodie
Rank #3 [Score: 0.3299] | ID: prod2 | Title: Blue Jeans

Query 2: 'warm casual outerwear for cold weather'
Rank #1 [Score: 0.4194] | ID: prod5 | Title: Green Hoodie
Rank #2 [Score: 0.3390] | ID: prod3 | Title: Black Leather Jacket
Rank #3 [Score: 0.3174] | ID: prod4 | Title: White Sneakers

Query 3: 'comfortable footwear for daily walking'
Rank #1 [Score: 0.6772] | ID: prod4 | Title: White Sneakers
Rank #2 [Score: 0.2766] | ID: prod1 | Title: Red T-Shirt
Rank #3 [Score: 0.2572] | ID: prod2 | Title: Blue Jeans


Assignment 11: AI Agent for Weather and Search Queries

Design Choices
1. ReAct Agent Framework: Built an autonomous agent loop using LangChain and LangGraph (`create_react_agent`) to evaluate incoming prompts and dynamically invoke specialized external tools (`get_weather` and `tavily_search_tool`).
2. Live Tool Integrations: Integrated `OpenWeatherMapAPIWrapper` for real-time weather and Tavily Search API (`TavilySearchResults`) for real-time live web search results.
3. Resilient API Execution & Retries: Applied `tenacity` exponential backoff retries (`wait_random_exponential`, `stop_after_attempt`) to handle network latency or rate limit spikes during agent invocations.
4. Lightweight Environment Loader (`load_env`): Reads configuration seamlessly from `.env` in the current or parent directory, supporting both Azure OpenAI and standard OpenAI proxy endpoints.

Challenges Faced & Limitations
1. Library Migration & Warnings: Newer LangChain and LangGraph releases emit deprecation notices for legacy utility locations (`langchain_community` vs `langchain`). Addressed by maintaining compatibility across package versions.
2. Strict Error Raising: Removed all fake simulated responses. If `OPENWEATHERMAP_API_KEY` or `TAVILY_API_KEY` is missing or invalid, the tools explicitly raise `ValueError` or standard API exceptions.

How to Run
1. Install dependencies:
   .venv\Scripts\pip.exe install langchain langchain-openai langchain-community langgraph pyowm tavily-python tenacity
2. Configure credentials in `.env`:
   OPENAI_API_KEY, OPENWEATHERMAP_API_KEY, TAVILY_API_KEY
3. Execute the script:
   ..\.venv\Scripts\python.exe "Assignment 11 - AI Agent for Weather and Search.py"

Real Execution Logs & Live Tool Routing Output
======================================================================
      AI AGENT FOR WEATHER & SEARCH QUERIES (LANGCHAIN / RE-ACT)
======================================================================
[System] Initializing LangGraph ReAct Agent with Weather & Tavily Tools...
[System] Agent initialized successfully.

----------------------------------------------------------------------
User: What's the weather in Hanoi?
  [Tool Call] get_weather tool calling: Getting weather for 'Hanoi'
AI: The current weather in Hanoi is overcast with a temperature of 27.22°C, which feels like 30.9°C. The humidity is at 86%, and there is a light wind blowing at 2.77 m/s from the southeast. The cloud cover is complete at 100%.

----------------------------------------------------------------------
User: Tell me about the latest news in AI.
  [Tool Call] tavily_search tool calling: Searching for 'latest news in AI'
AI: Here are some of the latest news highlights in AI:
1. Anthropic Deploys Claude Sonnet 5: Anthropic has launched Claude Sonnet 5, along with the restoration of Fable and Mythos.
2. Google's Gemini 3.6 Flash: Google is targeting enterprise agent token costs with its Gemini 3.6 Flash.
3. SoundHound AI Acquires LivePerson: SoundHound AI has acquired conversational AI platform LivePerson.

----------------------------------------------------------------------
User: Who won the last World Cup?
  [Tool Call] tavily_search tool calling: Searching for 'last World Cup winner 2023'
AI: The latest World Cup was the 2023 FIFA Women's World Cup, where Spain emerged as champions by defeating England 1-0 in the final on August 20, 2023.

----------------------------------------------------------------------
User: What's the weather in Paris today?
  [Tool Call] get_weather tool calling: Getting weather for 'Paris'
AI: The current weather in Paris is overcast with a temperature of 25.08°C, which feels like 24.74°C. The humidity is at 42%, and there is a light wind blowing at 3.93 m/s from the northeast.

----------------------------------------------------------------------
User: Search for the latest news on AI in healthcare.
  [Tool Call] tavily_search tool calling: Searching for 'latest news on AI in healthcare'
AI: Here are some of the latest news articles on AI in healthcare:
1. AI in Health Care | American Medical Association (AMA)
2. AI in Healthcare: Applications and Impact (Johns Hopkins University)

----------------------------------------------------------------------
User: exit
AI: Goodbye! Agent session ended.
======================================================================
Execution completed successfully.
======================================================================


Assignment 12: Satellite Image Cloud Detection via AzureOpenAI Inference

Step-by-Step Problem Resolution
1. Environment & API Setup:
   - Configured Azure OpenAI parameters using lightweight load_env() searching .env and ../.env.
   - Endpoint: https://aiportalapi.stu-platform.live/jpe
   - Deployment: GPT-4o-mini
   - API Version: 2024-02-15-preview

2. Structured Output Schema:
   - Defined Pydantic BaseModel `WeatherResponse` with attributes:
     * `accuracy` (float): Confidence score percentage (0.0 to 100.0).
     * `result` (str): Scene classification, strictly 'Cloudy' or 'Clear'.
   - Bound LLM instance using `llm.with_structured_output(WeatherResponse)` to enforce structured JSON output matching Pydantic fields.

3. Image Downloading & Base64 Encoding:
   - Implemented `fetch_image_as_base64()` to download image URLs via `requests`.
   - Used Python Imaging Library (`PIL.Image`) to validate image bytes, convert color spaces to RGB, and re-encode to clean JPEG base64 strings.

4. Multimodal Prompt Construction & Execution:
   - Formatted messages using LangChain/OpenAI chat message schema:
     System Message: Operational role and strict response guidelines.
     User Message: Text instruction + multimodal item `{"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,<b64_string>"}}`.
   - Executed non-interactive automated loop over 3 imagery test URLs.

Approach / Design Choices
1. Zero-Shot Visual Classification: Replaced heavy custom visual models with API-driven multimodal LLM inference. No separate satellite API key required as standard multimodal GPT-4o-mini visual processing is used.
2. Guaranteed Schema Compliance: Utilized Pydantic structured outputs (`with_structured_output`) to prevent formatting errors.
3. Resilient Infrastructure: Wrapped image fetching and API invocation with `tenacity` exponential retry logic (`@retry`).

Challenges Faced & Limitations
1. Base64 Payload Overhead: Optimized image streams into JPEG buffers using Pillow before base64 encoding.

How to Run
1. Install dependencies:
   .venv\Scripts\pip.exe install langchain-openai pillow requests pydantic tenacity
2. Execute Script:
   ..\.venv\Scripts\python.exe "Assignment 12 - Satellite Image Cloud Detection via AzureOpenAI Inference.py"

Real Execution Results
Test 1 | Scene: Dense Fluffy Cloud Cover  | Prediction: Cloudy | Accuracy: 95.0%
Test 2 | Scene: Clear Blue Ocean Surface  | Prediction: Clear  | Accuracy: 95.0%
Test 3 | Scene: Overcast Cumulus Scene    | Prediction: Cloudy | Accuracy: 95.0%
