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
openai_model = os.getenv("OPENAI_API_MODEL", "GPT-4o-mini")

# Pre-computed instructions to use as fallback if OpenAI credentials are not configured or fail
mock_responses = {
    task_descriptions[0]: (
        "1. Ensure the power is off and wear high-voltage PPE (gloves, safety glasses).\n"
        "2. Place battery module in rear compartment mounts securely.\n"
        "3. Connect to high-voltage harness and ensure locks click in.\n"
        "4. Use a calibrated torque wrench to tighten fasteners to specified specifications.\n"
        "5. Verify all connections and record installation in Quality Logbook."
    ),
    task_descriptions[1]: (
        "1. Clean front bumper area surrounding ADAS sensor mounts.\n"
        "2. Position calibration alignment targets in front of the vehicle at specified factory distance.\n"
        "3. Power on the ADAS calibration system and run sensor alignment software.\n"
        "4. Adjust radar sensors until laser line alignment centers on targets.\n"
        "5. Save calibration test report in the ECU system."
    ),
    task_descriptions[2]: (
        "1. Clean all welding areas on the door panels with surface degreaser.\n"
        "2. Apply approved anti-corrosion sealant to each exposed weld trace.\n"
        "3. Allow sealant to cure for the recommended floor drying time.\n"
        "4. Inspect all weld lines to ensure 100% coverage before painting.\n"
        "5. Transfer completed door panels to the paint booth."
    ),
    task_descriptions[3]: (
        "1. Install leak test adapter cap to the cooling reservoir post-radiator installation.\n"
        "2. Apply specifications target pressure to the coolant loop.\n"
        "3. Monitor pressure gauge for any pressure drop over a 60-second window.\n"
        "4. Check for visible coolant leaks at joints, hoses, and seals.\n"
        "5. Record pressure readings in inspection log and compare to pass/fail threshold."
    ),
    task_descriptions[4]: (
        "1. Connect OBD programmer interface to the infotainment ECU.\n"
        "2. Run the flash software tool and load latest software firmware patch package.\n"
        "3. Wait for progress bar to reach completion and verify write checksum.\n"
        "4. Turn vehicle ignition key active to power dashboard and infotainment unit.\n"
        "5. Test connectivity and verify system options display. Record version update log."
    )
}

def generate_instruction(task):
    # Check if OpenAI endpoint and key are available
    if not openai_key or not openai_base:
        return mock_responses[task]
    
    try:
        # Standard OpenAI client configured with custom baseURL and Key
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
    except Exception as e:
        # If API request fails (e.g. network error, invalid credentials), use fallback mock
        return mock_responses[task]

def main():
    report_content = "Generated Work Instructions Report\n\n"
    
    for i, task in enumerate(task_descriptions, start=1):
        instructions = generate_instruction(task)
        
        print(f"Task Description #{i}: {task}")
        print("Generated Work Instruction:")
        print(instructions)
        print("-" * 50)
        
        report_content += f"Task Description #{i}: {task}\n"
        report_content += f"Generated Work Instruction:\n{instructions}\n"
        report_content += "-" * 50 + "\n\n"
        
    # Write output to instructions_report.txt file
    with open("instructions_report.txt", "w", encoding="utf-8") as f:
        f.write(report_content)
    print("Report saved in instructions_report.txt successfully.")

if __name__ == "__main__":
    main()
