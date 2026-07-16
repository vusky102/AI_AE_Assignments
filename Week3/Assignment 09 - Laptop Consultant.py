# Assignment 09 - Laptop Consultant Chatbot in Python

import os
import sys

# Helper function to read environment variables from a .env file if it exists
def load_env():
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

# Load credentials
load_env()

# Import required libraries
try:
    import chromadb
    from openai import OpenAI
except ImportError as e:
    print(f"Error: Missing prerequisites. {e}")
    sys.exit(1)

# ---- CONFIGURATION SETUP ----
# Initialize OpenAI client directly using the parameters configured in .env
openai_key = os.getenv("OPENAI_API_KEY")
openai_base = os.getenv("OPENAI_API_BASEURL")

if not openai_key:
    print("[ERROR] OPENAI_API_KEY environment variable is not set. Please check your .env file.")
    sys.exit(1)

client = OpenAI(
    api_key=openai_key,
    base_url=openai_base
)

# Hardcoded model names as requested
embed_model = "text-embedding-3-small"
llm_model = "gpt-4o-mini"

# ---- GET EMBEDDING ----
def get_embedding(text):
    try:
        response = client.embeddings.create(
            input=text,
            model=embed_model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"[ERROR] Embedding creation failed: {e}")
        sys.exit(1)

# ---- CALL LLM ----
def ask_llm(context, user_input):
    system_prompt = (
        "You are a helpful assistant specializing in laptop recommendations. "
        "Use the provided context to recommend the best laptop(s) for the user needs."
    )
    user_prompt = (
        f"User requirements: {user_input}\n\n"
        f"Context (top relevant laptops):\n{context}\n\n"
        "Based on the above, which laptop(s) would you recommend and why?"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    try:
        response = client.chat.completions.create(
            model=llm_model,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[ERROR] LLM chat completion failed: {e}")
        sys.exit(1)

# ---- CHROMADB SETUP ----
print("[INFO] Configuring ChromaDB client and populating products dataset...")
try:
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="laptops")
except Exception as e:
    print(f"[ERROR] ChromaDB initialization failed: {e}")
    sys.exit(1)

# --------- Sample Laptops ---------
laptops = [
    {
        "id": "1",
        "name": "Gaming Beast Pro",
        "description": "A high-end gaming laptop with RTX 4080, 32GB RAM, and 1TB SSD. Perfect for hardcore gaming.",
        "tags": "gaming, high-performance, windows"
    },
    {
        "id": "2",
        "name": "Business Ultrabook X1",
        "description": "A lightweight business laptop with Intel i7, 16GB RAM, and long battery life. Great for productivity.",
        "tags": "business, ultrabook, lightweight"
    },
    {
        "id": "3",
        "name": "Student Basic",
        "description": "Affordable laptop with 8GB RAM, 256GB SSD, and a reliable battery. Ideal for students and general use.",
        "tags": "student, budget, general"
    }
]

# ---- ADD LAPTOPS TO CHROMADB ----
for laptop in laptops:
    print(f"  Indexing laptop description: {laptop['name']}")
    embedding = get_embedding(laptop["description"])
    collection.add(
        embeddings=[embedding],
        documents=[laptop["description"]],
        ids=[laptop["id"]],
        metadatas=[{
            "name": laptop["name"],
            "tags": laptop["tags"]
        }]
    )
print("[INFO] Chroma DB indexing completed.\n")

# ---- AUTOMATED MOCK INPUTS ----
user_queries = [
    "I want a lightweight laptop with long battery life for business trips.",
    "I need a laptop for gaming with the best graphics card available.",
    "Looking for a budget laptop suitable for student tasks and general browsing."
]

def build_context(results, n_context=3):
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    context_str = ""
    for doc, meta in zip(docs, metas):
        context_str += (
            f"Name: {meta['name']}\n"
            f"Description: {doc}\n"
            f"Tags: {meta['tags']}\n\n"
        )
    return context_str.strip()

# ---- MAIN RAG LOOP ----
def main():
    print("STARTING LAPTOP CONSULTANT CHATBOT SIMULATION\n")
    for user_input in user_queries:
        print("=" * 60)
        print(f"User input: {user_input}")
        
        # Step 1: Retrieve relevant laptops via vector search
        print("[INFO] Generating query embedding and querying ChromaDB...")
        query_embedding = get_embedding(user_input)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        
        # Step 2: Build context for LLM
        context = build_context(results)
        
        # Step 3: Get recommendation from LLM
        print("[INFO] Fetching recommendation from LLM consultant...")
        llm_output = ask_llm(context, user_input)
        
        print("\nLLM Recommendation:")
        print(llm_output)
        print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
