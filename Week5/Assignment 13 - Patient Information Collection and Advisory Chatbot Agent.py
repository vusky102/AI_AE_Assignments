# Assignment 13 - Patient Information Collection and Advisory Chatbot Agent in Python
import os
import sys

# Step 1: Environment Loader
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

# Step 2: Defensive Import Handling
try:
    from tenacity import retry, stop_after_attempt, wait_random_exponential
    from langchain_core.documents import Document
    from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
    from langchain_core.tools import tool
    from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings, ChatOpenAI, OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS
    from langgraph.graph import StateGraph, MessagesState, START, END
    from langgraph.prebuilt import ToolNode
except ImportError as e:
    print(f"Error: Missing prerequisites. {e}")
    print("Troubleshooting: Please ensure you are running inside the configured virtual environment (.venv) with required packages installed:")
    print("  .\\.venv\\Scripts\\pip.exe install langchain langchain-openai langchain-community langgraph faiss-cpu tavily-python tenacity openai")
    sys.exit(1)

# Step 3: Setup Mock Knowledge Base & Vector Retriever
mock_chunks = [
    Document(
        page_content="Patients with a sore throat should drink warm fluids, gargle with salt water, and avoid cold beverages."
    ),
    Document(
        page_content="Mild fevers under 38.5°C can often be managed with rest, hydration, and paracetamol or acetaminophen if needed."
    ),
    Document(
        page_content="If a patient reports dizziness, advise checking their blood pressure, hydration level, and avoiding sudden position changes."
    ),
    Document(
        page_content="Persistent coughs lasting more than 2 weeks should be evaluated by a healthcare provider for infections, asthma, or allergies."
    ),
    Document(
        page_content="Patients experiencing fatigue should consider iron deficiency, thyroid issues, or poor sleep quality as potential causes."
    ),
    Document(
        page_content="Red Flag Warning: Severe chest pain, shortness of breath, sudden confusion, or high fever over 39°C require urgent medical attention."
    ),
]

def init_retriever():
    """Initializes FAISS retriever with fallback to mock keyword search if embeddings fail."""
    embed_model_name = os.getenv("AZURE_OPENAI_EMBED_MODEL", "text-embedding-3-small")
    embed_key = os.getenv("AZURE_OPENAI_EMBEDDING_API_KEY", os.getenv("OPENAI_API_KEY"))
    embed_endpoint = os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT")

    embedding_model = None
    if embed_endpoint and embed_key:
        try:
            embedding_model = AzureOpenAIEmbeddings(
                model=embed_model_name,
                api_key=embed_key,
                azure_endpoint=embed_endpoint,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            )
        except Exception as err:
            print(f"[Embedding Setup Warning] Azure embeddings fallback: {err}")

    if not embedding_model and os.getenv("OPENAI_API_KEY"):
        try:
            kwargs = {"model": "text-embedding-3-small", "api_key": os.getenv("OPENAI_API_KEY")}
            if os.getenv("OPENAI_API_BASEURL"):
                kwargs["base_url"] = os.getenv("OPENAI_API_BASEURL")
            embedding_model = OpenAIEmbeddings(**kwargs)
        except Exception as err:
            print(f"[Embedding Setup Warning] OpenAI embeddings fallback: {err}")

    if embedding_model:
        try:
            db = FAISS.from_documents(mock_chunks, embedding_model)
            return db.as_retriever(search_kwargs={"k": 2})
        except Exception as err:
            print(f"[FAISS Setup Warning] Failed to construct FAISS index: {err}")

    return None

retriever = init_retriever()

# Step 4: Define Tools
@tool
def retrieve_advice(user_input: str) -> str:
    """Searches internal medical documents and health guidelines for relevant advice based on symptoms."""
    print(f"  [Tool Call] retrieve_advice tool calling for: '{user_input}'")
    if retriever:
        try:
            docs = retriever.invoke(user_input)
            if docs:
                return "\n".join(doc.page_content for doc in docs)
        except Exception as err:
            print(f"  [Retriever Invocation Note] {err}")

    # Keyword matching fallback over mock chunks
    query_words = [w.lower() for w in user_input.split() if len(w) > 3]
    matches = [
        doc.page_content for doc in mock_chunks
        if any(w in doc.page_content.lower() for w in query_words)
    ]
    if matches:
        return "\n".join(matches)
    return "\n".join(doc.page_content for doc in mock_chunks[:3])

@tool
def tavily_search_tool(query: str) -> str:
    """Searches the web via Tavily for real-time medical news, clinical updates, and supplementary health information."""
    print(f"  [Tool Call] tavily_search_tool tool calling for: '{query}'")
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

# Step 5: LLM Initialization
def get_llm():
    """Initializes LLM using Azure OpenAI or OpenAI proxy configuration."""
    azure_endpoint = os.getenv("AZURE_OPENAI_LLM_ENDPOINT") or os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_key = os.getenv("AZURE_OPENAI_LLM_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
    azure_deployment = os.getenv("AZURE_OPENAI_LLM_MODEL") or os.getenv("AZURE_DEPLOYMENT_NAME", "GPT-4o-mini")

    if azure_endpoint and azure_key:
        return AzureChatOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=azure_key,
            azure_deployment=azure_deployment,
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            temperature=0.2,
        )

    openai_key = os.getenv("OPENAI_API_KEY")
    openai_base = os.getenv("OPENAI_API_BASEURL")
    openai_model = os.getenv("OPENAI_API_MODEL", "GPT-4o-mini")

    if openai_key:
        kwargs = {
            "model": openai_model,
            "api_key": openai_key,
            "temperature": 0.2,
        }
        if openai_base:
            kwargs["base_url"] = openai_base
        return ChatOpenAI(**kwargs)

    raise ValueError("No API key found. Please configure OPENAI_API_KEY or AZURE_OPENAI_LLM_API_KEY in .env")

llm = get_llm()
tools = [retrieve_advice, tavily_search_tool]
llm_with_tools = llm.bind_tools(tools)

# Step 6: System Prompt & LangGraph Workflow Setup
SYSTEM_PROMPT = SystemMessage(
    content=(
        "You are an empathetic, professional AI Medical Information Assistant.\n"
        "Your goal is to interactively collect essential patient information and provide preliminary health advice.\n"
        "Follow these steps:\n"
        "1. Patient Details: Ensure you gather the patient's Name, Age, Main Symptoms, and Symptom Duration. "
        "If any of these key details are missing, kindly ask the patient for them.\n"
        "2. Retrieve Advice: Use the `retrieve_advice` tool to look up internal clinical guidance for the patient's symptoms.\n"
        "3. Supplemental Search: Use `tavily_search_tool` if additional up-to-date web information or specific treatment context is needed.\n"
        "4. Health Advice: Provide structured preliminary guidance including self-care steps, potential causes, and red flag warnings.\n"
        "5. Disclaimer: ALWAYS explicitly state that your advice is preliminary and not a replacement for evaluation by a qualified medical professional."
    )
)

@retry(
    wait=wait_random_exponential(min=1, max=10),
    stop=stop_after_attempt(3),
    reraise=True,
)
def call_model(state: MessagesState):
    """Executes model turn with exponential retries."""
    messages = state["messages"]
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SYSTEM_PROMPT] + messages
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: MessagesState):
    """Determines whether to invoke tools or end graph execution."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

tool_node = ToolNode(tools)

graph_builder = StateGraph(MessagesState)
graph_builder.add_node("call_model", call_model)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "call_model")
graph_builder.add_conditional_edges("call_model", should_continue, ["tools", END])
graph_builder.add_edge("tools", "call_model")

graph = graph_builder.compile()

# Step 7: Automated Non-Interactive Interactive Simulation
def run_patient_simulation(scenario_title: str, user_dialogue_turns: list):
    """Runs a multi-turn patient intake and advisory conversation through the LangGraph agent."""
    print("=" * 80)
    print(f"      PATIENT CASE SIMULATION: {scenario_title.upper()}")
    print("=" * 80)

    messages = [SYSTEM_PROMPT]

    for turn_idx, user_text in enumerate(user_dialogue_turns, 1):
        print(f"\n--- Turn {turn_idx} ---")
        print(f"Patient: {user_text}")
        messages.append(HumanMessage(content=user_text))

        try:
            result = graph.invoke({"messages": messages})
            # Update history with graph messages
            messages = result["messages"]
            final_msg = messages[-1].content
            print(f"\nAI Chatbot:\n{final_msg}")
        except Exception as e:
            print(f"\nAI Chatbot Error: {e}")
            break

    print("\n" + "=" * 80)

if __name__ == "__main__":
    print("=" * 80)
    print("      WEEK 5 ASSIGNMENT 13: PATIENT INFORMATION & ADVISORY CHATBOT AGENT")
    print("=" * 80)

    # Scenario 1: Gradual Intake (Missing details first, then provided)
    patient_1_turns = [
        "Hello doctor bot, I feel really unwell. I've had a sore throat and fever.",
        "My name is John Doe, I am 34 years old, and these symptoms started 3 days ago.",
    ]

    # Scenario 2: Comprehensive Intake with Dizziness and Fatigue
    patient_2_turns = [
        "Hi, I'm Sarah Connor, age 28. For the past week, I've been feeling extremely dizzy and tired whenever I stand up.",
        "No other pre-existing health conditions or symptoms, just dizziness when standing up and fatigue.",
    ]

    run_patient_simulation("Scenario 1: Sore Throat & Fever (2-Turn Interactive Intake)", patient_1_turns)
    run_patient_simulation("Scenario 2: Dizziness & Fatigue (1-Turn Full Intake)", patient_2_turns)

    print("\nExecution completed successfully.")
    print("=" * 80)
