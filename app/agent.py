from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from app.rag import get_retriever
from app.router import route_query
from app.handoff import handoff_to_human
from app.config import GEMINI_API_KEY, MODEL_NAME
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Using model: {MODEL_NAME}")
logger.info(f"API Key loaded from config")

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,
)

response_prompt = PromptTemplate(
    input_variables=["query", "context"],
    template="Answer empathetically based on the context: {context}\n Query: {query}"
)

# Create chain using LCEL
chain = response_prompt | llm | StrOutputParser()

def process_query(query):
    try:
        logger.info(f"Processing query: {query}")
        
        # Route the query
        category, confidence = route_query(query)
        logger.info(f"Query routed to category: {category}, confidence: {confidence}")

        if confidence < 0.8 or category == "Unknown":
            logger.info("Low confidence or unknown category, handing off to human")
            return handoff_to_human(query)

        # Get relevant documents
        retriever = get_retriever()
        docs = retriever.invoke(query)
        logger.info(f"Retrieved {len(docs)} documents")
        
        context = "\n".join([doc.page_content for doc in docs[:3]])
        logger.info(f"Context length: {len(context)} characters")

        # Invoke the chain with the input variables
        response = chain.invoke({"query": query, "context": context})
        logger.info(f"Generated response length: {len(response)} characters")

        if len(response) < 10:
            logger.info("Response too short, handing off to human")
            return handoff_to_human(query, response)

        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise