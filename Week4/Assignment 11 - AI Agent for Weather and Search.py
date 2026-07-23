# Assignment 11 - AI Agent for Weather and Search in Python
import os
import sys

# Define environment loader
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

# Defensive import handling
try:
    from tenacity import retry, stop_after_attempt, wait_random_exponential
    from langchain.tools import tool
    from langchain_community.utilities import OpenWeatherMapAPIWrapper
    from langchain_openai import ChatOpenAI, AzureChatOpenAI
    from langgraph.prebuilt import create_react_agent
except ImportError as e:
    print(f"Error: Missing prerequisites. {e}")
    print("Troubleshooting: Please ensure you are running inside the configured virtual environment (.venv) with required packages installed:")
    print("  .\\.venv\\Scripts\\pip.exe install langchain langchain-openai langchain-community langgraph pyowm tavily-python tenacity requests openai")
    sys.exit(1)

# Step 1: Define OpenWeather Tool with defensive error handling
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city.
    Args:
        city (str): The name of the city to get the weather for.
    Returns:
        str: A string describing the current weather in the specified city.
    """
    print(f"  [Tool Call] get_weather tool calling: Getting weather for '{city}'")
    owm_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not owm_key or owm_key.startswith("your_"):
        raise ValueError("OpenWeatherMap API key is missing. Please configure OPENWEATHERMAP_API_KEY.")
    
    try:
        weather_wrapper = OpenWeatherMapAPIWrapper()
        return weather_wrapper.run(city)
    except Exception as err:
        raise err


# Step 2: Define Tavily Search Tool with defensive error handling
@tool
def tavily_search_tool(query: str) -> str:
    """Search the web for real-time news, current events, and information.
    Args:
        query (str): Search topic or query string.
    Returns:
        str: Summarized search results or snippets from web search.
    """
    print(f"  [Tool Call] tavily_search tool calling: Searching for '{query}'")
    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key or tavily_key.startswith("your_"):
        raise ValueError("Tavily API key is missing. Please configure TAVILY_API_KEY.")
    
    try:
        from langchain_community.tools.tavily_search import TavilySearchResults
        search = TavilySearchResults(max_results=2)
        results = search.invoke({"query": query})
        return str(results)
    except Exception as err:
        raise err

# Step 3: LLM Initialization
def get_llm():
    """Initializes LLM using Azure OpenAI or OpenAI proxy configuration."""
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_deployment = os.getenv("AZURE_DEPLOYMENT_NAME", os.getenv("OPENAI_API_MODEL", "GPT-4o-mini"))
    
    if azure_endpoint and azure_key:
        return AzureChatOpenAI(
            azure_deployment=azure_deployment,
            azure_endpoint=azure_endpoint,
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-07-01-preview"),
            api_key=azure_key,
            temperature=0.0,
        )
    
    openai_key = os.getenv("OPENAI_API_KEY")
    openai_base = os.getenv("OPENAI_API_BASEURL")
    openai_model = os.getenv("OPENAI_API_MODEL", "GPT-4o-mini")
    
    if openai_key:
        kwargs = {
            "model": openai_model,
            "api_key": openai_key,
            "temperature": 0.0,
        }
        if openai_base:
            kwargs["base_url"] = openai_base
        return ChatOpenAI(**kwargs)
    
    raise ValueError("No API key found. Please configure OPENAI_API_KEY or AZURE_OPENAI_API_KEY in .env")

# Step 4: Resilient Agent Turn Invocation
@retry(
    wait=wait_random_exponential(min=1, max=10),
    stop=stop_after_attempt(3),
    reraise=True,
)
def execute_agent_turn(agent, messages):
    """Executes agent turn with exponential backoff retries."""
    return agent.invoke({"messages": messages})

# Main execution loop
if __name__ == "__main__":
    print("=" * 70)
    print("      AI AGENT FOR WEATHER & SEARCH QUERIES (LANGCHAIN / RE-ACT)")
    print("=" * 70)
    
    llm = get_llm()
    tools = [get_weather, tavily_search_tool]
    
    print("[System] Initializing LangGraph ReAct Agent with Weather & Tavily Tools...")
    agent = create_react_agent(model=llm, tools=tools)
    print("[System] Agent initialized successfully.\n")
    
    mock_questions = [
        "What's the weather in Hanoi?",
        "Tell me about the latest news in AI.",
        "Who won the last World Cup?",
        "What's the weather in Paris today?",
        "Search for the latest news on AI in healthcare.",
        "exit",
    ]
    
    messages = []
    
    for user_input in mock_questions:
        print("-" * 70)
        print(f"User: {user_input}")
        
        if user_input.lower() == "exit":
            print("AI: Goodbye! Agent session ended.")
            print("-" * 70)
            break
            
        messages.append({"role": "user", "content": user_input})
        try:
            response = execute_agent_turn(agent, messages)
            assistant_msg = response["messages"][-1].content
            messages.append({"role": "assistant", "content": assistant_msg})
            print(f"AI: {assistant_msg}\n")
        except Exception as e:
            print(f"Error during agent turn: {e}\n")
    
    print("=" * 70)
    print("Execution completed successfully.")
    print("=" * 70)
