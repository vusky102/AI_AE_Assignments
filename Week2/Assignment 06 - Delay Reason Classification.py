# Assignment 06 - Delay Reason Classification in Python

import os

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

# Loadenvironment variables
load_env()

# Step 1: Input Data  
log_entries = [  
    "Driver reported heavy traffic on highway due to construction",  
    "Package not accepted, customer unavailable at given time",  
    "Vehicle engine failed during route, replacement dispatched",  
    "Unexpected rainstorm delayed loading at warehouse",  
    "Sorting label missing, required manual barcode scan",  
    "Driver took a wrong turn and had to reroute",  
    "No issue reported, arrived on time",  
    "Address was incorrect, customer unreachable",  
    "System glitch during check-in at loading dock",  
    "Road accident caused a long halt near delivery point"  
]  

# Step 2: Heuristic Pre-classifier  
def initial_classify(text):  
    keywords = {  
        "traffic": "Traffic",  
        "road accident": "Traffic",  
        "customer": "Customer Issue",  
        "unavailable": "Customer Issue",  
        "engine": "Vehicle Issue",  
        "vehicle": "Vehicle Issue",  
        "rain": "Weather",  
        "storm": "Weather",  
        "label": "Sorting/Labeling Error",  
        "barcode": "Sorting/Labeling Error",  
        "wrong turn": "Human Error",  
        "reroute": "Human Error",  
        "system": "Technical System Failure",  
        "glitch": "Technical System Failure"  
    }  
  
    for k, v in keywords.items():  
        if k in text.lower():  
            return v  
    return "Other"  

# Step 3: API Setup
from openai import OpenAI

openai_key = os.getenv("OPENAI_API_KEY")
openai_base = os.getenv("OPENAI_API_BASEURL")
deployment_name = os.getenv("OPENAI_API_MODEL", "GPT-4o-mini")

client = OpenAI(
    api_key=openai_key,
    base_url=openai_base
)

# Refinement layer using LLM
def refine_classification(text, initial_label):  
    prompt = f"""  
You are a logistics assistant. A log entry has been auto-categorized as 
"{initial_label}". Please confirm or correct it by choosing one of the following 
categories:  
  - Traffic
  - Customer Issue
  - Vehicle Issue
  - Weather
  - Sorting/Labeling Error
  - Human Error
  - Technical System Failure
  - Other

Log Entry:  
\"\"\"{text}\"\"\"  

Return only the most appropriate category from the list. Do not output anything else.
"""  
    try:
        response = client.chat.completions.create(  
            model=deployment_name,  
            messages=[{"role": "user", "content": prompt}],  
            temperature=0,  
        )  
        return response.choices[0].message.content.strip()  
    except Exception as e:
        print(f"[ERROR] LLM refinement failed: {e}")
        return initial_label

# Step 4: Final Classification Pipeline  
def classify_log(text):  
    initial = initial_classify(text)  
    final = refine_classification(text, initial)  
    return {"log": text, "initial": initial, "final": final}  

# Step 5: Execution  
if __name__ == "__main__":  
    print("STARTING CLASSFICATION PIPELINE\n")
    print(f"{'No.':<4} | {'Log Entry':<60} | {'Initial':<25} | {'Final':<25}")
    print("-" * 125)
    
    for idx, entry in enumerate(log_entries, start=1):  
        result = classify_log(entry)  
        print(f"{idx:<4} | {result['log']:<60} | {result['initial']:<25} | {result['final']:<25}")

    print("\nProcess finished.")
