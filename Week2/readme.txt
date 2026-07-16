Week 2 Assignment - Efficient OpenAI API Usage

This directory contains resources for implementing function calling, batching, and rate limit retry backoffs with the OpenAI API.

Project Structure
- Assignment 04 - Efficient OpenAI API Usage.py: Main script executing the batch requests.
- readme.txt: Simplified description of the approach, design, and challenges.

Design Choices

1. Function Calling
We specified a travel itinerary schema containing the fields: destination, days, and activities_by_day. We use this schema to enforce structured itinerary output directly from the model using the function_call parameter.

2. Batching
Requests are processed sequentially through a loop. A safety time delay (time.sleep) is included between calls to limit the likelihood of hitting concurrency/TPM rate limits on the endpoint.

3. Retries and Rate Limits
We integrated the tenacity library using the retry decorator. The system catches RateLimitError and APIError, applies exponential random backoffs starting at 1 second up to 10 seconds, and retries up to 5 times. It re-raises the error if all attempts fail, facilitating clean logs.

Challenges Faced

1. Connection and Rate Limits
Interacting with remote API endpoints can lead to sudden rate limits. Introducing the tenacity decorator ensures the script waits and automatically retries rather than crashing immediately.

2. Environment Config
The script dynamically retrieves API keys from the .env file in the root workspace. This allows the CLI to execute correctly using customized endpoints.

How to Run
Run the script using Python:
python "Assignment 04 - Efficient OpenAI API Usage.py"
