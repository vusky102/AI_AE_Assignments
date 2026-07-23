# Assignment 12 - Satellite Image Cloud Detection via AzureOpenAI Inference in Python

"""
Assignment 12: Satellite Image Cloud Detection via AzureOpenAI Inference
Objective: Build a lightweight, non-interactive visual scene analysis system using
Azure OpenAI (GPT-4o-mini) to classify satellite images as 'Cloudy' or 'Clear' with confidence/accuracy.
"""

import base64
import io
import os
import sys

# --- Defensive Import Handling ---
try:
    import requests
    from PIL import Image
    from pydantic import BaseModel, Field
    from langchain_openai import AzureChatOpenAI, ChatOpenAI
    from tenacity import (
        retry,
        stop_after_attempt,
        wait_random_exponential,
        retry_if_exception_type,
    )
except ImportError as e:
    print(f"Error: Missing prerequisites. {e}")
    print("Troubleshooting: Please run `.venv\\Scripts\\pip.exe install langchain-openai pillow requests pydantic tenacity`")
    sys.exit(1)


# --- Lightweight Environment Loading ---
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


# --- Configure Azure / OpenAI Environment Variables ---
raw_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", os.getenv("OPENAI_API_BASEURL", "https://aiportalapi.stu-platform.live/jpe"))
AZURE_ENDPOINT = raw_endpoint.replace("stuplatform.live", "stu-platform.live")

AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))
AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT_NAME", os.getenv("OPENAI_API_MODEL", "GPT-4o-mini"))
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")


# --- Output Pydantic Schema ---
class WeatherResponse(BaseModel):
    accuracy: float = Field(description="The accuracy or confidence percentage of the classification (e.g. 95.0)")
    result: str = Field(description="The classification result, strictly either 'Cloudy' or 'Clear'")


# --- Resilient Image Fetcher ---
@retry(
    stop=stop_after_attempt(3),
    wait=wait_random_exponential(min=1, max=5),
    reraise=True
)
def fetch_image_as_base64(image_url: str) -> str:
    """
    Downloads an image from a URL, validates format via PIL, and returns base64 string.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(image_url, headers=headers, timeout=15)
    response.raise_for_status()
    
    # Validate image bytes using Pillow
    image_bytes = response.content
    img = Image.open(io.BytesIO(image_bytes))
    
    # Convert image format if needed or re-encode as JPEG
    output_buffer = io.BytesIO()
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(output_buffer, format="JPEG")
    encoded_b64 = base64.b64encode(output_buffer.getvalue()).decode("utf-8")
    return encoded_b64


# --- Resilient LLM Initialization Helper ---
def get_llm():
    """
    Initializes AzureChatOpenAI model instance with fallback to ChatOpenAI
    for API proxy routing compatibility.
    """
    try:
        return AzureChatOpenAI(
            azure_endpoint=AZURE_ENDPOINT,
            azure_deployment=AZURE_DEPLOYMENT,
            api_key=AZURE_API_KEY,
            api_version=AZURE_API_VERSION,
            temperature=0.0
        )
    except Exception:
        return ChatOpenAI(
            base_url=AZURE_ENDPOINT,
            model=AZURE_DEPLOYMENT,
            api_key=AZURE_API_KEY,
            temperature=0.0
        )


# --- Resilient LLM Inference Function ---
@retry(
    stop=stop_after_attempt(3),
    wait=wait_random_exponential(min=1, max=10),
    retry=retry_if_exception_type(Exception),
    reraise=True
)
def classify_satellite_image(image_url: str, llm_structured) -> WeatherResponse:
    """
    Fetches image, encodes it to base64, constructs multimodal prompt,
    and invokes Azure OpenAI / ChatOpenAI LLM for cloud detection classification.
    """
    # Step 1: Fetch image & encode base64
    base64_data = fetch_image_as_base64(image_url)
    
    # Step 2: Construct multimodal prompt payload
    messages = [
        {
            "role": "system",
            "content": (
                "Based on the satellite image provided, classify the scene as either: "
                "'Clear' (no clouds present in satellite view) or 'Cloudy' (with clouds). "
                "Respond with structured output containing accuracy (float percentage 0-100) and result ('Clear' or 'Cloudy'). "
                "Do not provide explanations."
            ),
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Classify the scene as either: 'Clear' or 'Cloudy' and Accuracy.",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_data}"},
                },
            ],
        },
    ]
    
    # Step 3: Invoke LLM with resilient fallback
    try:
        return llm_structured.invoke(messages)
    except Exception:
        fallback_llm = ChatOpenAI(
            base_url=AZURE_ENDPOINT,
            model=AZURE_DEPLOYMENT,
            api_key=AZURE_API_KEY,
            temperature=0.0
        ).with_structured_output(WeatherResponse)
        return fallback_llm.invoke(messages)


# --- Main Non-Interactive Mock Execution ---
def main():
    print("=" * 70)
    print("      ASSIGNMENT 12 - SATELLITE IMAGE CLOUD DETECTION VIA AZURE OPENAI")
    print("=" * 70)
    print(f"Endpoint:   {AZURE_ENDPOINT}")
    print(f"Deployment: {AZURE_DEPLOYMENT}")
    print(f"API Version:{AZURE_API_VERSION}")
    print("-" * 70)
    
    # Initialize model with structured output
    try:
        llm = get_llm()
        llm_structured = llm.with_structured_output(WeatherResponse)
    except Exception as e:
        print(f"Initialization Error: Unable to configure LLM client. {e}")
        return

    # Mock dataset containing 3 sample satellite/sky image URLs
    mock_dataset = [
        {
            "id": 1,
            "title": "Dense Fluffy Cloud Cover",
            "url": "https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=600",
            "expected": "Cloudy"
        },
        {
            "id": 2,
            "title": "Clear Blue Ocean Surface",
            "url": "https://images.unsplash.com/photo-1505118380757-91f5f5632de0?w=600",
            "expected": "Clear"
        },
        {
            "id": 3,
            "title": "Overcast Cumulus Scene",
            "url": "https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?w=600",
            "expected": "Cloudy"
        }
    ]

    results_table = []

    for idx, item in enumerate(mock_dataset, 1):
        print(f"\n[Test {idx}/{len(mock_dataset)}] Processing Scene: '{item['title']}'")
        print(f"  Image URL: {item['url']}")
        
        try:
            prediction: WeatherResponse = classify_satellite_image(item['url'], llm_structured)
            print(f"  >> Prediction: {prediction.result}")
            print(f"  >> Accuracy:   {prediction.accuracy:.1f}%")
            
            results_table.append({
                "Test": idx,
                "Title": item['title'],
                "Prediction": prediction.result,
                "Accuracy": f"{prediction.accuracy:.1f}%"
            })
        except Exception as e:
            print(f"  [ERROR] Classification failed for Test {idx}: {e}")
            results_table.append({
                "Test": idx,
                "Title": item['title'],
                "Prediction": "ERROR",
                "Accuracy": "N/A"
            })

    print("\n" + "=" * 70)
    print("                     CLASSIFICATION SUMMARY REPORT")
    print("=" * 70)
    print(f"{'Test':<6} | {'Scene Description':<28} | {'Prediction':<12} | {'Accuracy':<10}")
    print("-" * 70)
    for row in results_table:
        print(f"{row['Test']:<6} | {row['Title']:<28} | {row['Prediction']:<12} | {row['Accuracy']:<10}")
    print("=" * 70)
    print("Automated execution completed successfully.")

if __name__ == "__main__":
    main()
