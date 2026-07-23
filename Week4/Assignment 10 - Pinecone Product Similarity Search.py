# Assignment 10 - Pinecone Product Similarity Search in Python

import os
import sys
import time

# Step 1: Helper function to load environment variables from .env file
def load_env():
    """Reads environment variables from .env file in parent or current directory."""
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

# Step 2: Import required libraries with defensive checks
try:
    from openai import OpenAI, AzureOpenAI
    from scipy.spatial.distance import cosine
    from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
except ImportError as e:
    print(f"Error: Missing basic prerequisites. {e}")
    print("Troubleshooting: Please ensure required packages (openai, scipy, tenacity) are installed in your virtual environment.")
    sys.exit(1)

try:
    from pinecone import Pinecone, ServerlessSpec
    HAS_PINECONE = True
except ImportError:
    HAS_PINECONE = False
    print("[WARNING] 'pinecone-client' module is not installed. Will run in local fallback mode if needed.")

# Step 3: Initialize OpenAI / Azure OpenAI Client
openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
openai_base = os.getenv("OPENAI_API_BASEURL") or os.getenv("AZURE_OPENAI_ENDPOINT")
azure_deployment = os.getenv("AZURE_DEPLOYMENT_NAME", "text-embedding-3-small")
embed_model = "text-embedding-3-small"

if not openai_key:
    print("[ERROR] OpenAI / Azure OpenAI API key is missing. Please configure OPENAI_API_KEY in your .env file.")
    sys.exit(1)

if os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_API_KEY"):
    client = AzureOpenAI(
        api_version="2024-07-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY")
    )
    embedding_model_name = azure_deployment
else:
    client = OpenAI(
        api_key=openai_key,
        base_url=openai_base
    )
    embedding_model_name = embed_model

# Function to extract vector embeddings with retry logic
@retry(
    wait=wait_random_exponential(min=1, max=10),
    stop=stop_after_attempt(5),
    reraise=True
)
def get_embedding(text):
    """Generates 1536-dimensional vector embedding for input text using text-embedding-3-small."""
    try:
        response = client.embeddings.create(
            input=text,
            model=embedding_model_name
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"[ERROR] Failed to generate embedding: {e}")
        raise e

# Step 4: Sample product dataset as specified in the assignment
products = [
    {"id": "prod1", "title": "Red T-Shirt", "description": "Comfortable cotton t-shirt in bright red"},
    {"id": "prod2", "title": "Blue Jeans", "description": "Stylish denim jeans with relaxed fit"},
    {"id": "prod3", "title": "Black Leather Jacket", "description": "Genuine leather jacket with classic style"},
    {"id": "prod4", "title": "White Sneakers", "description": "Comfortable sneakers perfect for daily wear"},
    {"id": "prod5", "title": "Green Hoodie", "description": "Warm hoodie made of organic cotton"},
]

# Automated sample queries for headless execution
queries = [
    "clothing item for summer",
    "warm casual outerwear for cold weather",
    "comfortable footwear for daily walking"
]

def run_pinecone_pipeline(pinecone_api_key):
    """Executes similarity search pipeline using Pinecone vector database."""
    print("[INFO] Initializing Pinecone client...")
    pc = Pinecone(api_key=pinecone_api_key)
    
    index_name = "product-similarity-index"
    
    # Check if index exists, create if missing
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    if index_name not in existing_indexes:
        print(f"[INFO] Index '{index_name}' not found. Creating Pinecone serverless index (dim=1536, metric=cosine)...")
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        # Give Pinecone index a brief moment to initialize
        time.sleep(5)
        print(f"[INFO] Pinecone index '{index_name}' created successfully.")
    else:
        print(f"[INFO] Connected to existing Pinecone index '{index_name}'.")

    index = pc.Index(index_name)

    # Upsert product vector embeddings
    print("[INFO] Generating embeddings and upserting vectors into Pinecone index...")
    vectors_to_upsert = []
    for p in products:
        text_to_embed = f"{p['title']}: {p['description']}"
        embedding = get_embedding(text_to_embed)
        vectors_to_upsert.append({
            "id": p["id"],
            "values": embedding,
            "metadata": {"title": p["title"], "description": p["description"]}
        })

    index.upsert(vectors=vectors_to_upsert)
    print(f"[INFO] Successfully upserted {len(vectors_to_upsert)} product vectors to Pinecone.\n")

    # Perform similarity search for each test query
    top_k = 3
    for query in queries:
        print("=" * 70)
        print(f"SEARCH QUERY: '{query}'")
        print("=" * 70)
        
        query_embedding = get_embedding(query)
        results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

        print(f"Top {top_k} Most Similar Products (Pinecone Cosine Similarity):")
        print(f"{'Rank':<6} | {'ID':<8} | {'Title':<22} | {'Similarity Score':<16}")
        print("-" * 65)

        for rank, match in enumerate(results.matches, start=1):
            product_id = match.id
            score = match.score
            title = match.metadata.get("title", "") if match.metadata else next(p["title"] for p in products if p["id"] == product_id)
            print(f"{rank:<6} | {product_id:<8} | {title:<22} | {score:.4f}")
        print("\n")

def main():
    print("=" * 70)
    print("ASSIGNMENT 10: PINECONE PRODUCT SIMILARITY SEARCH ENGINE")
    print("=" * 70 + "\n")

    pinecone_key = os.getenv("PINECONE_API_KEY")

    if not HAS_PINECONE:
        raise ImportError("'pinecone' package is missing. Please install it to proceed.")
    if not pinecone_key:
        raise ValueError("PINECONE_API_KEY environment variable is not set. Please configure it in .env")

    try:
        run_pinecone_pipeline(pinecone_key)
    except Exception as e:
        raise e

    print("Process finished successfully.")

if __name__ == "__main__":
    main()
