# Assignment 14 - Retail RAG Chatbot in Python

import os
import sys
from typing import TypedDict, Optional, List

# --- Step 0: Environment Loading ---
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

# --- Step 1: Defensive Imports ---
try:
    from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type
    from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI, OpenAIEmbeddings, ChatOpenAI
    from langchain_community.docstore.in_memory import InMemoryDocstore
    from langchain_community.vectorstores import FAISS
    from langchain_core.documents import Document
    from langchain_core.prompts import ChatPromptTemplate
    from langgraph.graph import StateGraph, END
    from openai import APIError, RateLimitError
except ImportError as e:
    print(f"Error: Missing prerequisites. {e}")
    print("Troubleshooting: Please ensure you are running inside the configured virtual environment with required packages installed:")
    print("  pip install langchain langchain-openai langchain-community langgraph faiss-cpu tenacity openai")
    sys.exit(1)


# --- Step 2: Helper Functions for LLM & Embedding Initialization ---
def get_llm():
    """Initializes AzureChatOpenAI with automatic fallback to proxy ChatOpenAI."""
    endpoint = os.getenv("AZURE_OPENAI_LLM_ENDPOINT", os.getenv("OPENAI_API_BASEURL", "https://aiportalapi.stu-platform.live/jpe"))
    api_key = os.getenv("AZURE_OPENAI_LLM_API_KEY", os.getenv("OPENAI_API_KEY"))
    model = os.getenv("AZURE_OPENAI_LLM_MODEL", os.getenv("OPENAI_API_MODEL", "GPT-4o-mini"))
    
    try:
        azure_llm = AzureChatOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            deployment_name=model,
            api_version="2024-07-01-preview",
            temperature=0
        )
        azure_llm.invoke("ping")
        return azure_llm
    except Exception:
        return ChatOpenAI(
            api_key=api_key,
            base_url=endpoint,
            model=model,
            temperature=0
        )

def get_embeddings():
    """Initializes AzureOpenAIEmbeddings with automatic fallback to proxy OpenAIEmbeddings."""
    endpoint = os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT", os.getenv("OPENAI_API_BASEURL", "https://aiportalapi.stu-platform.live/jpe"))
    api_key = os.getenv("AZURE_OPENAI_EMBEDDING_API_KEY", os.getenv("OPENAI_API_KEY"))
    model = os.getenv("AZURE_OPENAI_EMBED_MODEL", "text-embedding-3-small")
    
    try:
        azure_emb = AzureOpenAIEmbeddings(
            azure_endpoint=endpoint,
            api_key=api_key,
            model=model,
            api_version="2024-07-01-preview"
        )
        azure_emb.embed_query("ping")
        return azure_emb
    except Exception:
        return OpenAIEmbeddings(
            api_key=api_key,
            base_url=endpoint,
            model=model
        )


# --- Step 3: Mock Dataset of 15 Walmart Policy & Product Documents ---
WALMART_DOCS = [
    Document(
        page_content="Walmart customers may return electronics within 30 days with a receipt and original packaging.",
        metadata={"id": 1, "category": "Electronics"}
    ),
    Document(
        page_content="Grocery items at Walmart can be returned within 90 days with proof of purchase, except perishable products.",
        metadata={"id": 2, "category": "Grocery"}
    ),
    Document(
        page_content="Walmart offers a 1-year warranty on most electronics and appliances. See product details for exceptions.",
        metadata={"id": 3, "category": "Warranty"}
    ),
    Document(
        page_content="Walmart Plus members get free shipping with no minimum order amount.",
        metadata={"id": 4, "category": "Membership"}
    ),
    Document(
        page_content="Prescription medications purchased at Walmart are not eligible for return or exchange.",
        metadata={"id": 5, "category": "Pharmacy"}
    ),
    Document(
        page_content="Open-box items are eligible for return at Walmart within the standard return period, but must include all original accessories.",
        metadata={"id": 6, "category": "Open Box"}
    ),
    Document(
        page_content="If a Walmart customer does not have a receipt, most returns are eligible for store credit with valid photo identification.",
        metadata={"id": 7, "category": "No Receipt"}
    ),
    Document(
        page_content="Walmart allows price matching for identical items found on Walmart.com and local competitor ads.",
        metadata={"id": 8, "category": "Price Match"}
    ),
    Document(
        page_content="Walmart Vision Center purchases may be returned or exchanged within 60 days with a receipt.",
        metadata={"id": 9, "category": "Vision Center"}
    ),
    Document(
        page_content="Returns on cell phones at Walmart require the device to be unlocked and all personal data erased.",
        metadata={"id": 10, "category": "Cell Phones"}
    ),
    Document(
        page_content="Walmart gift cards cannot be redeemed for cash except where required by law.",
        metadata={"id": 11, "category": "Gift Cards"}
    ),
    Document(
        page_content="Seasonal merchandise at Walmart (e.g., holiday decorations) may have modified return windows, see in-store signage.",
        metadata={"id": 12, "category": "Seasonal"}
    ),
    Document(
        page_content="Bicycles purchased at Walmart can be returned within 90 days if not used outdoors and with all accessories present.",
        metadata={"id": 13, "category": "Sports & Outdoors"}
    ),
    Document(
        page_content="For online Walmart orders, customers can return items in store or by mail using the prepaid label.",
        metadata={"id": 14, "category": "Online Orders"}
    ),
    Document(
        page_content="Walmart reserves the right to deny returns suspected of fraud or abuse.",
        metadata={"id": 15, "category": "Fraud Policy"}
    ),
]


# --- Step 4: Typed State for LangGraph ---
class RAGState(TypedDict):
    question: str
    context: Optional[str]
    retrieved_docs: Optional[List[Document]]
    answer: Optional[str]


# --- Step 5: System Prompt Template ---
PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful, precise Walmart retail support assistant. "
            "Use ONLY the provided policy and product context to answer the user question accurately. "
            "Cite and reference the specific policy rules from the context in your answer. "
            "If the information is clear, provide a concise, direct, human-friendly recommendation.",
        ),
        ("human", "Retrieved Policy Context:\n{context}\n\nUser Question: {question}"),
    ]
)


# --- Step 6: Define LangGraph Nodes with Tenacity Exponential Retries ---
@retry(
    retry=retry_if_exception_type((APIError, RateLimitError, Exception)),
    wait=wait_random_exponential(min=1, max=10),
    stop=stop_after_attempt(5),
    reraise=True
)
def retrieve_node(state: RAGState, retriever) -> RAGState:
    docs = retriever.invoke(state["question"])
    context_str = "\n".join([f"[Doc {doc.metadata.get('id', '?')}]: {doc.page_content}" for doc in docs])
    return {**state, "context": context_str, "retrieved_docs": docs}


@retry(
    retry=retry_if_exception_type((APIError, RateLimitError, Exception)),
    wait=wait_random_exponential(min=1, max=10),
    stop=stop_after_attempt(5),
    reraise=True
)
def generate_node(state: RAGState, llm) -> RAGState:
    formatted_prompt = PROMPT_TEMPLATE.format(
        context=state.get("context", ""), question=state["question"]
    )
    answer_msg = llm.invoke(formatted_prompt)
    return {**state, "answer": answer_msg.content}


# --- Step 7: Build LangGraph Workflow ---
def build_rag_graph(retriever, llm):
    builder = StateGraph(RAGState)
    builder.add_node("retrieve", lambda s: retrieve_node(s, retriever))
    builder.add_node("generate", lambda s: generate_node(s, llm))
    builder.set_entry_point("retrieve")
    builder.add_edge("retrieve", "generate")
    builder.set_finish_point("generate")
    return builder.compile()


# --- Step 8: Main Automated Headless Execution ---
if __name__ == "__main__":
    print("=" * 80)
    print("  WALMART RAG CHATBOT FOR PRODUCT AND POLICY SUPPORT")
    print("  LangGraph + FAISS + Azure OpenAI / OpenAI API")
    print("=" * 80)

    # Initialize Embeddings & Vector Store
    print("\n[1/3] Initializing Embeddings & Vector Store with 15 Walmart Documents...")
    embeddings = get_embeddings()
    docstore = InMemoryDocstore({str(i): doc for i, doc in enumerate(WALMART_DOCS)})
    vectorstore = FAISS.from_documents(WALMART_DOCS, embeddings, docstore=docstore)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    print(" -> Vector store initialized successfully.")

    # Initialize LLM & Build LangGraph
    print("\n[2/3] Initializing LLM & Constructing LangGraph Workflow...")
    llm = get_llm()
    rag_graph = build_rag_graph(retriever, llm)
    print(" -> LangGraph compiled successfully.")

    # Automated Mock Query Execution
    test_queries = [
        "Can I return a Walmart bicycle if I've ridden it outdoors?",
        "What is the return policy for electronics if I don't have a receipt?",
        "Are prescription medications purchased at Walmart eligible for return or exchange?",
        "How does free shipping work for Walmart Plus members?",
        "What requirements must be met to return an open-box item or a cell phone?",
    ]

    print(f"\n[3/3] Executing Automated Evaluation on {len(test_queries)} Mock User Scenarios:\n")

    for idx, query in enumerate(test_queries, 1):
        print("=" * 80)
        print(f"  SCENARIO {idx}: \"{query}\"")
        print("=" * 80)
        
        result = rag_graph.invoke({"question": query})
        
        print("\n--- RETRIEVED CONTEXT ---")
        print(result.get("context", "No context retrieved."))
        
        print("\n--- GENERATED ANSWER ---")
        print(result.get("answer", "No answer generated."))
        print("-" * 80 + "\n")

    print("=" * 80)
    print("  AUTOMATED EVALUATION COMPLETED SUCCESSFULLY")
    print("=" * 80)
