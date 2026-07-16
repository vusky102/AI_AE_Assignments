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
    
    # Prompt optimized to generate exactly 4-5 concise steps as shown in the user's instructions
    prompt = f"""You are an expert automotive manufacturing supervisor. 
Generate exactly 4 to 5 short, concise, single-sentence step-by-step work instructions for the new model task.
Keep it simple and numbered as:
1. [First instruction]
2. [Second instruction]
3. [Third instruction]
4. [Fourth instruction]
5. [Fifth instruction]

Task:
\"{task}\"

Work Instructions:"""

    response = client.chat.completions.create(
        model=openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def print_table(results):
    # Print the table header
    print("=" * 110)
    print(f"{'Task Description'.ljust(45)} | {'Generated Work Instruction'}")
    print("=" * 110)
    
    for task_desc, instruction_text in results:
        # Wrap task description to line lengths of 42 characters
        desc_lines = []
        words = task_desc.split()
        current_line = []
        for word in words:
            if len(" ".join(current_line + [word])) <= 42:
                current_line.append(word)
            else:
                desc_lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            desc_lines.append(" ".join(current_line))
            
        # Split instructions by newline
        instruction_lines = [line.strip() for line in instruction_text.split("\n") if line.strip()]
        
        # Print side-by-side
        max_lines = max(len(desc_lines), len(instruction_lines))
        for i in range(max_lines):
            left = desc_lines[i] if i < len(desc_lines) else ""
            right = instruction_lines[i] if i < len(instruction_lines) else ""
            print(f"{left.ljust(45)} | {right}")
        
        print("-" * 110)

def main():
    results = []
    for task in task_descriptions:
        instructions = generate_instruction(task)
        results.append((task, instructions))
        
    print_table(results)

if __name__ == "__main__":
    main()
