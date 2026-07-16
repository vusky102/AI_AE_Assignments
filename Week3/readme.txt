Week 3 Assignments

This directory contains the Hugging Face Text-to-Speech (TTS) model cloning and inference project.

Project Structure
- Assignment 07 - TTS Inference.py: Main script to download the pre-trained TTS model and run inference to generate speech from input text.
- output.wav: The generated audio waveform representing the spoken Vietnamese phrase.
- readme.txt: Simplified description of the approach, design, and challenges.


Assignment 07: Hugging Face TTS Inference using MMS-TTS

Design Choices
1. Pre-trained Model (VITS): We selected the `facebook/mms-tts-vie` model from Meta's Massive Multilingual Speech project. It utilizes the VITS (Variational Inference with adversarial learning for Text-to-Speech) architecture, which integrates a tokenizer, acoustic model, and vocoder into a single end-to-end network, outputting highly natural speech waveforms directly from character sequences without intermediate spectrogram steps.
2. CPU Execution & Virtualization: Running on a guest VM with 8 GB RAM and no CUDA-enabled GPU requires CPU execution. We loaded torch and model execution purely on CPU, which takes less than a second of runtime per sentence.
3. Output Saving: Utilized the Python `soundfile` package to save the floating-point tensor array into a single-channel `16000 Hz` WAV format representation on disk.

Challenges Faced
1. Windows Path Length Limits ([WinError 206]): Unpacking PyTorch's huge packages under the default Windows Store Python paths (`C:\Users\<user>\AppData\Local\Packages\...`) triggers Windows path limit failures. To fix this, we created a local virtual environment (.venv) under the project workspace, shortening target directory prefixes and enabling a successful installation.
2. Library Linking: The standard Windows `soundfile` pip package installs pre-compiled libsndfile DLLs. In environments missing these libraries, referencing alternative libraries (like `scipy.io.wavfile`) is recommended, but native soundfile worked perfectly in the .venv once path length issues were bypassed.

How to Run
To run this project:
1. Create a local virtual environment from the project root:
   python -m venv .venv
2. Install dependencies using the virtual environment's pip:
   .venv\Scripts\pip.exe install torch --index-url https://download.pytorch.org/whl/cpu
   .venv\Scripts\pip.exe install transformers soundfile
3. Run the script from the Week3 directory:
   ..\.venv\Scripts\python.exe "Assignment 07 - TTS Inference.py"
4. View results: The output file `output.wav` is created directly under the Week3 directory.


Assignment 08: Clothing Product Semantic Search Engine

Design Choices
1. Embedding Model: Hardcoded to use Azure OpenAI's "text-embedding-3-small" (1536 dimensions) directly via standard client.embeddings.create requests.
2. Cosine Distance: Used `scipy.spatial.distance.cosine` directly to compute distances, ranking matches in ascending order (where a lower distance indicates a closer match).
3. Pre-defined Catalog: Created a diverse dataset consisting of jackets, hoodies, jeans, summer dresses, grey sweatshirts, and khaki shorts.

How Embeddings are Created and Used
1. Generation: We pass the products' descriptions and query text into the embeddings API. Each text block is mapped to a 1536-dimensional floating-point vector representing its semantic structure.
2. Search & Retrieval: When a user drafts a search query, its text is embedded into the same 1536-dimensional space. The search engine calculates similarity scores, sorts items in descending order, and displays top ranks.

Cosine Similarity for Ranking
1. Logic: Measured by the cosine of the angle between two vectors:
   Similarity(A, B) = (A . B) / (||A|| * ||B||)
   It returns range [-1, 1], with 1 representing identical directional vectors. We use it to rank search matches by mapping text structures to proximity in high-dimensional space.
2. Benefit: Focuses on vector orientation rather than magnitude. This ensures keyword variations or length variations do not distort semantic overlaps.

Challenges & Limitations
1. Exact Code Matching: Semantic search struggles with exact keyword SKU/serial codes (e.g., "SKU-9902"). Hybrid search (combining BM25 keyword match and dense embeddings) is optimal for commercial production.
2. API Latency: Generating embeddings dynamically for catalog items during queries introduces network lag. In production, clothing description embeddings must be pre-indexed into a specialized Vector Database (e.g., pgvector, Chroma, Qdrant).

How to Run
1. Ensure the virtual environment (.venv) is installed with requirements:
   .venv\Scripts\pip.exe install scipy openai python-dotenv
2. Run the script:
   ..\.venv\Scripts\python.exe "Assignment 08 - Clothing Search.py"

Search Outputs for Query: 'warm cotton sweatshirt' (Ranked by Cosine Distance)
Rank #1 [Cosine Distance: 0.3710] | Title: Grey Crewneck Sweatshirt (Description: Warm grey crewneck pullover sweatshirt...)
Rank #2 [Cosine Distance: 0.4885] | Title: Red Hoodie (Description: Cozy red hoodie made from organic cotton.)
Rank #3 [Cosine Distance: 0.5787] | Title: White Summer Dress (Description: Lightweight white cotton summer dress...)


Assignment 09: Laptop Consultant Chatbot using OpenAI & ChromaDB

Design Choices
1. API Config: Connects directly using coordinates set in the unified `.env` file (supporting proxy or standard OpenAI credentials).
2. Vector Indexing (ChromaDB): Deployed ChromaDB client to index structural records. We pass descriptions to the hardcoded `text-embedding-3-small` model to generate and save 1536-dimensional vectors into the `laptops` collection.
3. RAG Architecture: Leveraged ChromaDB vector queries to retrieve context objects based on user requirements. The relevant items are piped into the hardcoded `gpt-4o-mini` template to generate final consultant output.

Why Vector DB RAG improves Chatbot Recommendations
1. Contextual Pinpointing (Reducing Hallucination): Instead of training models on dynamic stocks or expanding prompt sizes with a massive catalogue, vector search computes embeddings to retrieve the top 3 relevant records. The LLM is instructed to recommend ONLY from this context, avoiding catalog hallucinations.
2. Memory Efficiency: Helps search catalogs of arbitrary scale. The database handles semantic lookup mathematically, preserving prompt tokens and lowering API costs.

How to Run
1. Verify the virtual environment carries the required modules:
   .venv\Scripts\pip.exe install chromadb openai
2. Run the script:
   ..\.venv\Scripts\python.exe "Assignment 09 - Laptop Consultant.py"

Example Query Simulation Logs
Query 1: "I want a lightweight laptop with long battery life for business trips."
Recommendation: Business Ultrabook X1 (Highlighted lightweight design, long battery life, i7 cpu/16GB RAM).
Query 2: "I need a laptop for gaming with the best graphics card available."
Recommendation: Gaming Beast Pro (Highlighted Nvidia RTX 4080 GPU, 32GB RAM, 1TB SSD).
Query 3: "Looking for a budget laptop suitable for student tasks and general browsing."
Recommendation: Student Basic (Highlighted affordability, 8GB RAM, 256GB SSD).
