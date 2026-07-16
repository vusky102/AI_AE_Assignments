Week 1 Assignments

This directory contains three python projects for Week 1.

Project Structure
- Assignment 01 - Command-Line Task Manager.py: A command-line program to add, view, complete, and delete tasks.
- Assignment 02 - Prompt-Driven Work Instructions.py: An AI assistant that generates manufacturing instructions for new car models using an LLM.
- Assignment 03 - AI-Powered Meeting Summarizer.py: An AI assistant that summarizes meeting transcripts.
- readme.txt: Short report detailing the approach, folder info, and sample outputs.


Assignment 01: Command-Line Task Manager

Approach
- Data Structure: The application uses a list filled with dictionaries. Each task dictionary stores the task ID, description, and status.
- Functions: The program is broken down into separate modular functions: add_task, view_tasks, mark_completed, and delete_task.
- Automated Input: We used a loop to run dummy commands automatically so the program runs without needing manual user inputs.

Challenges Faced: None

How to Run
Run the script using Python:
python "Assignment 01 - Command-Line Task Manager.py"


Assignment 02: Prompt-Driven Work Instructions Generator

Approach
- LLM Connection: Uses OpenAI client and prompt engineering to draft detailed, sequential assembly instructions.
- Environment variables: Loads OPENAI_API_KEY, OPENAI_API_BASEURL, and OPENAI_API_MODEL from the env file to make the api calls.
- Output: Prints the generated shop-floor instructions directly to the console.

Challenges Faced: None

How to Run
Run the script using Python:
python "Assignment 02 - Prompt-Driven Work Instructions.py"


Assignment 03: AI-Powered Meeting Summarizer

Approach
- Summarization: Ingests meeting transcipts and generates a breakdown of key points, decisions, and action items.
- Environment variables: Loads OPENAI_API_KEY, OPENAI_API_BASEURL, and OPENAI_API_MODEL from the env file to make the api calls.
- Output: Logs outputs directly to the console.

Challenges Faced: None

How to Run
Run the script using Python:
python "Assignment 03 - AI-Powered Meeting Summarizer.py"


Assignment 03 Sample Transcripts and Outputs (5 Samples)

Sample 1: Project Sync Meeting
Transcript:
[10:02 AM - Project Sync Meeting]
Anna: Chào mọi người, hôm nay mình sẽ cập nhật tiến độ dự án AI chatbot.
Minh: Backend đã xong phần xử lý intent, còn API thì đang test.
Trang: Bên frontend mình gặp chút lỗi khi hiển thị gợi ý từ chatbot, sẽ fix hôm nay.
Anna: Tốt rồi. Nhớ cập nhật trên Jira trước chiều nhé. Có gì blocker không?
Minh: Không có gì lớn.
Trang: Mình cần thêm access từ devops.
Anna: Ok, mình sẽ nhờ Huy cấp cho.

Output Summary:
Key Points:
- Intent processing is completed at backend. API is currently under testing phase.
- Frontend has a bug with chatbot suggestions that will be fixed today.
Decisions:
- Team needs to updates progress on Jira before this afternoon.
Action Items:
- Anna to contact Huy to grant devops access for Trang.

---

Sample 2: Marketing Launch Brainstorm
Transcript:
[02:15 PM - Marketing Launch Brainstorm]
James: Let's brainstorm ideas for launching the new app version.
Sarah: I suggest running an influencer campaign on TikTok and Instagram.
Leo: I can design new ad banners and post visual updates on LinkedIn.
James: Great. Sarah, can you draft a budget proposal by Friday?
Sarah: Yes, I will share it in our Slack channel.
Leo: I will finish the LinkedIn banner mockups by tomorrow morning.
James: Perfect. We'll review both deliverables next Monday.

Output Summary:
Key Points:
- Brainstorming campaign strategies for app launch including social media influencer collaborations.
Decisions:
- Review budget and LinkedIn banner deliverables next Monday.
Action Items:
- Sarah to draft a budget proposal by Friday and upload to Slack.
- Leo to finish LinkedIn banner mockups by tomorrow morning.

---

Sample 3: Development Standup
Transcript:
[09:30 AM - Development Standup]
Kevin: I finished debugging the database connection pool leak yesterday.
Alice: Awesome! I will review your pull request this morning.
Bob: I am still working on integrating Stripe checkout, needing some clarifications on webhooks.
Kevin: We can discuss the webhook details right after this standup.
Alice: Great, let's merge the database fix first so we can deploy to staging today.

Output Summary:
Key Points:
- Database pool leak fix completes. Checkout integration is ongoing.
Decisions:
- Merge pool leak fix first and code deploy to staging today.
Action Items:
- Alice to review Kevin's pull request this morning.
- Kevin and Bob to sync and clarify Stripe webhook integration details.

---

Sample 4: Customer Support Weekly Sync
Transcript:
[01:00 PM - Customer Support Weekly Sync]
Rachel: We had a 15% increase in response times due to high ticket volumes this week.
David: Most inquiries were about resetting passwords after the recent database update.
Rachel: Can we write a quick FAQ section or setup an automation flow to guide them?
David: Yes, I will write the FAQ draft today so we can publish it.
Rachel: I'll also configure the automated email responder to link to the new FAQ.

Output Summary:
Key Points:
- Password reset inquiries increased response times by 15% following database updates.
Decisions:
- Formulate a password troubleshooting FAQ and setup autoreply redirects.
Action Items:
- David to write the FAQ draft today.
- Rachel to configure mail responders to point to the new FAQ.

---

Sample 5: HR Onboarding Sync
Transcript:
[11:00 AM - HR Onboarding Sync]
Emily: We have three new software engineers joining next Monday.
Marcus: I prepared the onboarding documents and sent them to their personal emails.
Emily: Excellent. Did we check if IT set up their work laptops yet?
Marcus: Not yet. I'll ping IT today to make sure the laptops are shipped and ready.
Emily: Great. I will schedule the welcome sync for Monday morning at 9:30 AM.

Output Summary:
Key Points:
- Three new hires starting on Monday. Paperwork is complete and delivered.
Decisions:
- Welcome sync scheduled for Monday at 9:30 AM.
Action Items:
- Marcus to contact IT today checking status of setup and shipping for work notebooks.
