# Assignment 02 - Prompt-Driven Work Instructions Generator in Python

import os
from openai import OpenAI

# Mock Input Data - 5 task descriptions
task_descriptions = [
    "Install the battery module in the rear compartment, connect to the high-voltage harness, and verify torque on fasteners.",
    "Calibrate the ADAS (Advanced Driver Assistance Systems) radar sensors on the front bumper using factory alignment targets.",
    "Apply anti-corrosion sealant to all exposed welds on the door panels before painting.",
    "Perform leak test on coolant system after radiator installation. Record pressure readings and verify against specifications.",
    "Program the infotainment ECU with the latest software package and validate connectivity with dashboard display."
]

# Helper function to read environment variables from a .env file if it exists
def load_env():
    # Check parent folder (since .env is in root and script runs in Week1) or current folder
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

def generate_instruction(task):
    client = OpenAI(
        api_key=openai_key,
        base_url=openai_base
    )
    
    prompt = f"""You are an expert automotive manufacturing supervisor. Generate step-by-step 
work instructions for the following new model task. Include safety 
precautions, required tools (if any), and acceptance checks. Write in clear, 
numbered steps suitable for production workers.

Task:
\"\"\"{task}\"\"\"

Work Instructions:"""

    response = client.chat.completions.create(
        model=openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def main():
    for i, task in enumerate(task_descriptions, start=1):
        instructions = generate_instruction(task)
        print(f"Task Description #{i}: {task}")
        print("Generated Work Instruction:")
        print(instructions)
        print("-" * 50)

if __name__ == "__main__":
    main()
