Week 2 Assignments

This directory contains two python projects for Week 2.

Project Structure
- Assignment 04 - Efficient OpenAI API Usage.py: Main script executing batch requests with function calling and rate-limit handling.
- Assignment 05 - Local Resume Generator.py: Main script to load a local model file (GGUF format) and generate resumes from user input.
- readme.txt: Simplified description of the approach, design, and challenges.


Assignment 04: Efficient OpenAI API Usage

Design Choices
1. Function Calling: We specified a travel itinerary schema containing the fields: destination, days, and activities_by_day. We use this schema to enforce structured itinerary output directly from the model using the function_call parameter.
2. Batching: Requests are processed sequentially through a loop. A safety time delay (time.sleep) is included between calls to limit the likelihood of hitting concurrency/TPM rate limits on the endpoint.
3. Retries and Rate Limits: We integrated the tenacity library using the retry decorator. The system catches RateLimitError and APIError, applies exponential random backoffs starting at 1 second up to 10 seconds, and retries up to 5 times. It re-raises the error if all attempts fail, facilitating clean logs.

Challenges Faced
1. Connection and Rate Limits: Interacting with remote API endpoints can lead to sudden rate limits. Introducing the tenacity decorator ensures the script waits and automatically retries rather than crashing immediately.
2. Environment Config: The script dynamically retrieves API keys from the .env file in the root workspace. This allows the CLI to execute correctly using customized endpoints.

How to Run
Run the script using Python:
python "Assignment 04 - Efficient OpenAI API Usage.py"


Assignment 05: Build Resume Generation Using LLaMA3 Locally

Design Choices
1. Local Model: The script utilizes llama-cpp-python to load GGUF format weights locally on the guest machine. This ensures data privacy and offline capability.
2. Object Oriented Structure: The execution logic is organized into two main classes: LlamaModel (responsible for model initialization and text generation) and ResumeGenerator (responsible for prompt formatting and structured resume assembly).
3. Auto Processing: Loops over a list of three dummy profile dictionaries containing mock user experience, education, and target job titles.

Challenges Faced
1. Environment Compatibility & Precompiled Wheels: Local compilation of llama-cpp-python on Windows systems requires VS C++ Build Tools and can easily fail. To circumvent compilation hurdles in a CPU-only environment on Windows, install the precompiled wheel from the official index:
   pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
2. Model Download Size: Downloading 8B models can be slow, so using a smaller 1B/1.5B GGUF model of LLaMA 3.2 is recommended. We downloaded the 1B Instruct quantized model (`Llama-3.2-1B-Instruct-Q4_K_M.gguf`).
3. Hardware Performance: Running LLM generation on CPU-only machines with limited memory (e.g. 8 GB RAM) is slow. The generation task for 3 complete profiles took approximately 8 minutes in total (~2.7 minutes per resume) under the current CPU-only hardware environment.

How to Run
To run this project:
1. Install requirements using the precompiled CPU wheels:
   pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
2. Download the GGUF model file and place it in the Week2 directory as: llama-3.2-1b-instruct-q4_k_m.gguf
   You can download it via CLI using:
   curl.exe -L -o llama-3.2-1b-instruct-q4_k_m.gguf https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q4_K_M.gguf
3. Run the script:
   python "Assignment 05 - Local Resume Generator.py"


Assignment 06: Delay Reason Classification using Maintenance Logs

Design Choices
1. Hybrid Classification Pipeline: The system uses a two-stage approach:
   - Stage 1: A fast, rule-based keyword pre-classifier maps incident logs to initial categories.
   - Stage 2: An LLM-based refiner (powered by Azure OpenAI proxy) takes the log entry and the initial category, validates or corrects it, and returns the final normalized category.
2. Direct API Integration: Initializes the client using the parameters configured in the project's root .env file (OPENAI_API_KEY and OPENAI_API_BASEURL), ensuring standard integration patterns.

Challenges Faced
1. Output Consistency: Restricting LLM completions to exactly the eight predefined categories without extra text, labels, or formatting was achieved by using clear prompt instructions and temperature=0.0.

How to Run
1. Configure credentials in the .env file in the project root:
   OPENAI_API_KEY, OPENAI_API_BASEURL, OPENAI_API_MODEL
   Or configure Azure credentials:
   AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_DEPLOYMENT_NAME
2. Run the script:
   python "Assignment 06 - Delay Reason Classification.py"

Classification Output for 10 Mock Logs
No.  | Log Entry                                                    | Initial                   | Final                    
-----------------------------------------------------------------------------------------------------------------------------
1    | Driver reported heavy traffic on highway due to construction | Traffic                   | Traffic                  
2    | Package not accepted, customer unavailable at given time     | Customer Issue            | Customer Issue           
3    | Vehicle engine failed during route, replacement dispatched   | Vehicle Issue             | Vehicle Issue            
4    | Unexpected rainstorm delayed loading at warehouse            | Weather                   | Weather                  
5    | Sorting label missing, required manual barcode scan          | Sorting/Labeling Error    | Sorting/Labeling Error   
6    | Driver took a wrong turn and had to reroute                  | Human Error               | Human Error              
7    | No issue reported, arrived on time                           | Other                     | Other                    
8    | Address was incorrect, customer unreachable                  | Customer Issue            | Customer Issue           
9    | System glitch during check-in at loading dock                | Technical System Failure  | Technical System Failure 
10   | Road accident caused a long halt near delivery point         | Traffic                   | Traffic                  

Difference from Retrieval-Based Pipelines (e.g. RAG)
1. Context Retrieval vs. Direct Inference: Retrieval-based systems (like RAG) query an external dataset index (using vector libraries or hybrid search) to inject relevant content chunks into the context window before asking the LLM to generate answers. This classification pipeline uses direct zero-shot inference with a local rule pre-classifier, requiring no document databases or searching.
2. Goal & Output: RAG is designed to generate rich, free-form answers from documents. This pipeline is tailored to classify unstructured text into a fixed, structured taxonomy (eight predefined incident categories) with high precision and low output latency.
3. Best Fit: Where RAG fits best for Q&A chatbots and documentation assistants, this hybrid classification pipeline fits best for automated tagging, log analysis, alert routing, and support ticket triage where speed, standardization, and deterministic categories are crucial.
