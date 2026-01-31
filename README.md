# AI-Agent-for-Customer-Support
An intelligent customer support agent built with LangChain, Google Gemini AI, and RAG (Retrieval-Augmented Generation). 
This system automatically routes customer queries, provides context-aware responses, and escalates to human agents when needed.

## Features

Intelligent Query Routing: Automatically classifies queries into FAQ, Technical, Billing, or Unknown categories
RAG-Powered Responses: Uses document retrieval with FAISS vector store for context-aware answers
Smart Escalation: Hands off to human agents when confidence is low or query is complex
Keyword Optimization: Reduces API calls by 70-80% with keyword-based pre-routing
Production Ready: Dockerized setup with FastAPI backend and Streamlit frontend
Vector Search: FAISS-based semantic search for accurate document retrieval
Rate Limit Handling: Built-in retry logic and graceful degradation**

## Architecture

<img width="343" height="601" alt="image" src="https://github.com/user-attachments/assets/bf30f282-28bf-4f0c-b1f3-42ff81aa96d3" />

## Quick Start
Prerequisites

Python 3.11+

Docker & Docker Compose (optional)

Google Gemini API Key 



## Local Setup

Clone the repository

git clone https://github.com/yourusername/customer-support-agent.git
cd customer-support-agent

Create virtual environment

bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Configure environment variables

### Create .env file
cp .env.example .env

### Edit .env and add your API key
GOOGLE_API_KEY=your_gemini_api_key_here

Add your knowledge base documents

### Place your documents in the data/ directory
mkdir -p data
### Add .txt or .pdf files with your FAQs, technical docs, etc.

Build the FAISS index

python build_index.py

Run the application

Start FastAPI backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# In another terminal, start Streamlit frontend
streamlit run frontend/streamlit_app.py --server.port 8080

Access the application


Frontend: http://localhost:8080
API Docs: http://localhost:8000/docs

Docker Setup

Build and run with Docker Compose

bashdocker-compose up --build

Access the application


Frontend: http://localhost:8080
Backend API: http://localhost:8000


Environment Variables
Create a .env file with the following:
env# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional
MODEL_NAME=gemini-2.5-flash

HF_HOME=/app/.cache/huggingface

Customizing the Router

Edit app/router.py to add custom keywords for your domain:
python# Add your custom keywords
if any(word in query_lower for word in ['your', 'custom', 'keywords']):
    return 'YourCategory', 0.85
Adjusting Confidence Threshold
In app/agent.py, modify the confidence threshold:
if confidence < 0.8:  # Adjust this value
    return handoff_to_human(query)

    
📊 API Endpoints
POST /query
Process a customer query
Request:
json{
  "query": "What is your return policy?"
}
Response:
json{
  "response": "Our return policy allows...",
  "category": "FAQ",
  "confidence": 0.9,
  "handoff": false
}
    
