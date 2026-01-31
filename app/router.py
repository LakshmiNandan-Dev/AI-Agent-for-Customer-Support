from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import MODEL_NAME, GEMINI_API_KEY
import logging
import re

logger = logging.getLogger(__name__)

# Verify API key is loaded
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in config")

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,
)

router_prompt = PromptTemplate(
    input_variables=["query"],
    template="""Classify this customer query into exactly one of these categories: FAQ, Technical, Billing, or Unknown.

Query: {query}

Respond with ONLY the category name, nothing else."""
)

# Use StrOutputParser for cleaner output
chain = router_prompt | llm | StrOutputParser()

def route_query(query):
    """
    Route a query to the appropriate category
    Returns: (category, confidence)
    """
    try:
        logger.info(f"Routing query: {query}")
        response = chain.invoke({"query": query})
        
        # Clean up the response - remove common prefixes and extra text
        category = response.strip()
        category = re.sub(r'^(Category:\s*|Answer:\s*|Response:\s*)', '', category, flags=re.IGNORECASE)
        category = category.strip().split('\n')[0].strip()  # Take first line only
        
        # Normalize category names
        category_lower = category.lower()
        if 'faq' in category_lower:
            category = 'FAQ'
        elif 'technical' in category_lower or 'tech' in category_lower:
            category = 'Technical'
        elif 'billing' in category_lower or 'payment' in category_lower:
            category = 'Billing'
        elif 'unknown' in category_lower:
            category = 'Unknown'
        
        # Set confidence based on category
        confidence = 0.9 if category in ["FAQ", "Technical", "Billing"] else 0.5
        
        logger.info(f"Routed to category: {category}, confidence: {confidence}")
        return category, confidence
        
    except Exception as e:
        logger.error(f"Error in route_query: {str(e)}")
        return "Unknown", 0.5