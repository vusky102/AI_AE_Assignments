# Assignment 03 - AI-Powered Meeting Summarizer in Python

import os
from openai import OpenAI

# Mock Input Data - 5 different meeting transcripts
transcripts = [
    # Transcript 1
    (
        "[10:02 AM - Project Sync Meeting]\n"
        "Anna: Chào mọi người, hôm nay mình sẽ cập nhật tiến độ dự án AI chatbot.\n"
        "Minh: Backend đã xong phần xử lý intent, còn API thì đang test.\n"
        "Trang: Bên frontend mình gặp chút lỗi khi hiển thị gợi ý từ chatbot, sẽ fix hôm nay.\n"
        "Anna: Tốt rồi. Nhớ cập nhật trên Jira trước chiều nhé. Có gì blocker không?\n"
        "Minh: Không có gì lớn.\n"
        "Trang: Mình cần thêm access từ devops.\n"
        "Anna: Ok, mình sẽ nhờ Huy cấp cho."
    ),
    # Transcript 2
    (
        "[02:15 PM - Marketing Launch Brainstorm]\n"
        "James: Let's brainstorm ideas for launching the new app version.\n"
        "Sarah: I suggest running an influencer campaign on TikTok and Instagram.\n"
        "Leo: I can design new ad banners and post visual updates on LinkedIn.\n"
        "James: Great. Sarah, can you draft a budget proposal by Friday?\n"
        "Sarah: Yes, I will share it in our Slack channel.\n"
        "Leo: I will finish the LinkedIn banner mockups by tomorrow morning.\n"
        "James: Perfect. We'll review both deliverables next Monday."
    ),
    # Transcript 3
    (
        "[09:30 AM - Development Standup]\n"
        "Kevin: I finished debugging the database connection pool leak yesterday.\n"
        "Alice: Awesome! I will review your pull request this morning.\n"
        "Bob: I am still working on integrating Stripe checkout, needing some clarifications on webhooks.\n"
        "Kevin: We can discuss the webhook details right after this standup.\n"
        "Alice: Great, let's merge the database fix first so we can deploy to staging today."
    ),
    # Transcript 4
    (
        "[01:00 PM - Customer Support Weekly Sync]\n"
        "Rachel: We had a 15% increase in response times due to high ticket volumes this week.\n"
        "David: Most inquiries were about resetting passwords after the recent database update.\n"
        "Rachel: Can we write a quick FAQ section or setup an automation flow to guide them?\n"
        "David: Yes, I will write the FAQ draft today so we can publish it.\n"
        "Rachel: I'll also configure the automated email responder to link to the new FAQ."
    ),
    # Transcript 5
    (
        "[11:00 AM - HR Onboarding Sync]\n"
        "Emily: We have three new software engineers joining next Monday.\n"
        "Marcus: I prepared the onboarding documents and sent them to their personal emails.\n"
        "Emily: Excellent. Did we check if IT set up their work laptops yet?\n"
        "Marcus: Not yet. I'll ping IT today to make sure the laptops are shipped and ready.\n"
        "Emily: Great. I will schedule the welcome sync for Monday morning at 9:30 AM."
    )
]

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

# Load environment keys
load_env()

openai_key = os.getenv("OPENAI_API_KEY")
openai_base = os.getenv("OPENAI_API_BASEURL")
openai_model = os.getenv("OPENAI_API_MODEL")

def summarize_transcript(transcript):
    client = OpenAI(
        api_key=openai_key,
        base_url=openai_base
    )
    
    prompt = f"Summarize the following meeting transcript with key points, decisions, and action items:\n\n{transcript}"
    
    response = client.chat.completions.create(
        model=openai_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant specialized in summarizing meeting notes."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

def main():
    print("AI-POWERED MEETING SUMMARIZER INITIATING\n")
    
    for i, transcript in enumerate(transcripts, start=1):
        print(f"=== Transcript #{i} ===")
        print(transcript)
        print("\n=== Summary ===")
        summary = summarize_transcript(transcript)
        print(summary)
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main()
