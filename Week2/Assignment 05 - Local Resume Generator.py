# Assignment 05 - Local Resume Generator in Python

import os

try:
    from llama_cpp import Llama
    HAS_LLAMA = True
except ImportError:
    HAS_LLAMA = False

class LlamaModel:
    def __init__(self, model_path, n_ctx=2048):
        """
        Initializes the local LLaMA model.
        Args:
            model_path (str): The filename/path to the local GGUF model file.
            n_ctx (int): The context window size.
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}. Please download/place a local GGUF model here.")
        
        try:
            # Load model locally
            self.llm = Llama(model_path=model_path, n_ctx=n_ctx)
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to load LLaMA model: {e}")

    def generate_text(self, prompt, max_tokens=1024, temperature=0.7):
        """
        Generates text using the loaded local model.
        Args:
            prompt (str): Prompt to query the model.
            max_tokens (int): Max completion tokens to generate.
            temperature (float): Context sampling randomness.
        """
        try:
            output = self.llm(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["User:", "Assistant:"] # Standard stop tokens
            )
            return output["choices"][0]["text"].strip()
        except Exception as e:
            raise RuntimeError(f"Failed to generate text: {e}")


class ResumeGenerator:
    def __init__(self, llama_model):
        """
        Creates a Resume Generator using a loaded LlamaModel.
        """
        self.llama = llama_model

    def build_resume(self, profile):
        """
        Formats user profile credentials and prompts the local LLM to generate the resume.
        """
        name = profile.get("name", "")
        role = profile.get("target_role", "")
        experience = profile.get("experience", "")
        skills = profile.get("skills", "")
        education = profile.get("education", "")

        # Format input details as an instruction prompt
        prompt = (
            f"Write a professional resume. Rely on these details:\n"
            f"Name: {name}\n"
            f"Target Position: {role}\n"
            f"Work Experience: {experience}\n"
            f"Professional Skills: {skills}\n"
            f"Education: {education}\n\n"
            f"Instructions:\n"
            f"- Organize clearly with sections: Profile, Work Experience, Skills, Education.\n"
            f"- Keep it concise and professional.\n"
            f"Resume Output:\n"
        )
        return self.llama.generate_text(prompt)


def main():
    # Check if llama_cpp is installed
    if not HAS_LLAMA:
        print("Error: The 'llama-cpp-python' library is not installed on this system.")
        print("Troubleshooting: Please run 'pip install llama-cpp-python' to set it up.")
        return

    # 3 dummy profile inputs as required for auto execution
    profiles = [
        {
            "name": "John Doe",
            "target_role": "Senior Software Engineer",
            "experience": "5 years at TechCorp leading API development, 2 years at CodeCo writing Django backends",
            "skills": "Python, Django, AWS, SQL, REST APIs",
            "education": "B.S. in Computer Science"
        },
        {
            "name": "Alice Smith",
            "target_role": "Data Analyst",
            "experience": "3 years at DataBiz creating dashboard reports and statistics pipelines",
            "skills": "R, Python, Tableau, Excel, PowerBI, SQL",
            "education": "M.S. in Statistics"
        },
        {
            "name": "Bob Johnson",
            "target_role": "Product Manager",
            "experience": "4 years Product Manager at RetailApp directing roadmaps and sprint workflows",
            "skills": "Agile, Scrum, Product Roadmapping, JIRA, SQL",
            "education": "B.A. in Business Administration"
        }
    ]

    # Local GGUF model path (can be changed to match local name/location on user's system)
    model_path = "./llama-3.2-1b-instruct-q4_k_m.gguf"

    print("INITIALIZING LOCAL RESUME GENERATOR TASK\n")
    try:
        # Load local model
        llama_model = LlamaModel(model_path)
        generator = ResumeGenerator(llama_model)
        
        # Loop and generate resume for each profile (3 samples)
        for i, profile in enumerate(profiles, start=1):
            print(f"=== Sample Profle #{i}: {profile['name']} - {profile['target_role']} ===")
            resume = generator.build_resume(profile)
            print(resume)
            print("=" * 60 + "\n")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Note: Before executing this script, please download a LLaMA/Qwen model in .gguf file format,")
        print(f"place it at '{model_path}', and install llama-cpp-python via 'pip install llama-cpp-python'.")
    except Exception as e:
        print(f"Failed to execute resume generator: {e}")

if __name__ == "__main__":
    main()
