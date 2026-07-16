# Assignment 08 - Clothing Product Semantic Search Engine in Python

import os
import sys

# Helper function to read environment variables from a .env file if it exists
def load_env():
    # Check parent folder or current folder for .env
    paths = [".env", "../.env"]
    for path in paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    # Skip blank lines and comments
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
    from openai import OpenAI
    from scipy.spatial.distance import cosine
except ImportError as e:
    print(f"Error: Missing prerequisites. {e}")
    sys.exit(1)

# Step 1: Initialize OpenAI client directly using the parameters configured in .env
openai_key = os.getenv("OPENAI_API_KEY")
openai_base = os.getenv("OPENAI_API_BASEURL")

if not openai_key:
    print("[ERROR] OPENAI_API_KEY environment variable is not set. Please check your .env file.")
    sys.exit(1)

client = OpenAI(
    api_key=openai_key,
    base_url=openai_base
)

# Step 2: Sample product data (Clothing Catalog)
products = [
    {
        "title": "Classic Blue Jeans",
        "short_description": "Comfortable blue denim jeans with a relaxed fit.",
        "price": 49.99,
        "category": "Jeans"
    },
    {
        "title": "Red Hoodie",
        "short_description": "Cozy red hoodie made from organic cotton.",
        "price": 39.99,
        "category": "Hoodies"
    },
    {
        "title": "Black Leather Jacket",
        "short_description": "Stylish black leather jacket with a slim fit design.",
        "price": 120.00,
        "category": "Jackets"
    },
    {
        "title": "White Summer Dress",
        "short_description": "Lightweight white cotton summer dress with beautiful floral patterns.",
        "price": 59.99,
        "category": "Dresses"
    },
    {
        "title": "Grey Crewneck Sweatshirt",
        "short_description": "Warm grey crewneck pullover sweatshirt crafted from premium fleece cotton.",
        "price": 45.00,
        "category": "Sweatshirts"
    },
    {
        "title": "Khaki Cargo Shorts",
        "short_description": "Durable cargo pocket shorts for outdoor utility activities.",
        "price": 29.99,
        "category": "Shorts"
    }
]

# Step 3: Function to get embeddings from OpenAI API
# Hardcoded to use the model "text-embedding-3-small" directly as instructed
# Returns a list of embeddings to support batch requests
def get_embedding(text):
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        print(f"[ERROR] Failed to query embeddings API: {e}")
        sys.exit(1)

# Reusable semantic search function
def find_n_closest(text_query, embeddings, n=3):
    # get_embedding(text_query)[0] is taken in case of a single text phrase
    query_embedding = get_embedding(text_query)[0]

    # Compute cosine distance directly between query and items
    scores = []
    for item in embeddings:
        distance = cosine(query_embedding, item["embedding"])
        scores.append((distance, item))

    # Sort ascending based on cosine distance (smaller distance = closer match)
    scores.sort(key=lambda x: x[0])
    return scores[:n]

def main():
    print("STARTING SEMANTIC SEARCH ENGINE RUN\n")
    
    # Step 4: Generate embeddings for all clothing descriptions (Batched Request)
    print("[INFO] Encoding clothing catalog product descriptions in a single batched call...")
    descriptions = [product["short_description"] for product in products]
    embeddings_list = get_embedding(descriptions)
    
    for idx, (product, embedding) in enumerate(zip(products, embeddings_list), start=1):
        product["embedding"] = embedding
        print(f"  [{idx}/{len(products)}] Baked embedding for: {product['title']}")
    print("[INFO] Product catalog embedding generation complete.\n")

    # Step 5: Accept user query (auto input)
    query = "warm cotton sweatshirt"
    print(f"User Search Query: '{query}'")

    # Execute find_n_closest query search
    print("[INFO] Finding top matches using raw cosine distance...")
    top_matches = find_n_closest(query, products, n=3)

    # Step 9: Display Top Matches (Top 3 results)
    print("\n" + "=" * 60)
    print(f"TOP 3 MATCHING PRODUCTS FOR: '{query}' (Ranked by Cosine Distance)")
    print("=" * 60)
    
    for rank, (distance, product) in enumerate(top_matches, start=1):
        print(f"Rank #{rank} [Cosine Distance: {distance:.4f}]")
        print(f"  Title      : {product['title']}")
        print(f"  Description: {product['short_description']}")
        print(f"  Price      : ${product['price']:.2f}")
        print(f"  Category   : {product['category']}")
        print("-" * 60)

if __name__ == "__main__":
    main()
