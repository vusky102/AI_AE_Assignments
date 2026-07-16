# Assignment 01 - Efficient OpenAI API Usage in Python

import os
import time
from openai import OpenAI, RateLimitError, APIError
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type

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

# Load the keys
load_env()

openai_key = os.getenv("OPENAI_API_KEY")
openai_base = os.getenv("OPENAI_API_BASEURL")
openai_model = os.getenv("OPENAI_API_MODEL")

# Set up the OpenAI client
client = OpenAI(
    api_key=openai_key,
    base_url=openai_base
)

# Function schema for travel itinerary planning
functions = [
    {
        "name": "generate_itinerary",
        "description": "Generate a travel itinerary for a given destination and duration.",
        "parameters": {
            "type": "object",
            "properties": {
                "destination": {
                    "type": "string",
                    "description": "Travel destination city or country"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to plan for"
                },
                "activities_by_day": {
                    "type": "string",
                    "description": "The detailed day-by-day itinerary of matching sights and activities"
                }
            },
            "required": ["destination", "days", "activities_by_day"]
        }
    }
]

# Set up retry logic with exponential backoff on exceptions (max 5 attempts)
@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)),
    wait=wait_random_exponential(min=1, max=10),
    stop=stop_after_attempt(5),
    reraise=True
)
def call_openai_function(prompt, destination, days):
    # Call OpenAI Chat Completion with functions defined
    response = client.chat.completions.create(
        model=openai_model,
        messages=[
            {"role": "user", "content": f"{prompt} Destination: {destination}, Duration: {days} days."}
        ],
        functions=functions,
        function_call={"name": "generate_itinerary"},
        temperature=0.3
    )
    return response

# Process inputs as a batch
def batch_process(inputs):
    results = []
    for input_data in inputs:
        prompt = input_data["prompt"]
        destination = input_data["destination"]
        days = input_data["days"]
        
        print(f"Processing itinerary request for {destination} ({days} days)...")
        
        try:
            res = call_openai_function(prompt, destination, days)
            results.append(res)
            time.sleep(1)  # Optional pause to avoid reaching rate limits aggressively
        except Exception as e:
            print(f"Error processing {destination}: {e}")
            results.append(None)
            
    return results

# Sample inputs as required (3 samples)
batch_inputs = [
    {"prompt": "Plan a relaxed vacation travel itinerary.", "destination": "Paris", "days": 3},
    {"prompt": "Plan an active exploring travel itinerary.", "destination": "Tokyo", "days": 5},
    {"prompt": "Plan a sightseeing city travel itinerary.", "destination": "New York", "days": 4}
]

if __name__ == "__main__":
    print("STARTING BATCH PROCESSING WORKFLOW\n")
    outputs = batch_process(batch_inputs)
    
    print("\nBATCH PROCESSING RESULTS\n")
    print("=" * 60)
    for idx, output in enumerate(outputs):
        destination = batch_inputs[idx]["destination"]
        print(f"Result for {destination}:")
        if output:
            func_call = output.choices[0].message.function_call
            if func_call:
                print(f"Function Name: {func_call.name}")
                print(f"Arguments: {func_call.arguments}")
            else:
                print(output.choices[0].message.content)
        else:
            print("No result due to error or retry failure.")
        print("=" * 60)
