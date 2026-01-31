from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from app.utils import get_embeddings
import os
import logging

logger = logging.getLogger(__name__)

def load_documents(directory="data/"):
    """Load text and PDF documents from directory"""
    logger.info(f"Loading documents from {directory}")
    
    # Load text files
    loader = DirectoryLoader(
        directory, 
        glob="**/*.txt", 
        loader_cls=TextLoader, 
        silent_errors=True
    )
    
    # Load PDF files
    pdf_loader = DirectoryLoader(
        directory, 
        glob="**/*.pdf", 
        loader_cls=PyPDFLoader,
        silent_errors=True
    )

    docs = loader.load() + pdf_loader.load()
    logger.info(f"Loaded {len(docs)} documents")
    
    if not docs:
        logger.warning(f"No documents found in {directory}")
        logger.warning("Creating placeholder documents for testing")
        from langchain.schema import Document
        docs = [
            Document(
                page_content="FAQ: How do I contact support? You can email us at support@example.com",
                metadata={"source": "placeholder"}
            ),
            Document(
                page_content="Technical documentation: Our system is built with Python and LangChain.",
                metadata={"source": "placeholder"}
            )
        ]
    
    return docs

def build_rag_index():
    """Build FAISS index from documents"""
    logger.info("Building RAG index...")
    docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    logger.info(f"Split into {len(chunks)} chunks")
    
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Ensure directory exists
    os.makedirs("faiss_index", exist_ok=True)
    vectorstore.save_local("faiss_index")
    logger.info("FAISS index saved to faiss_index/")
    
    return vectorstore

def get_retriever():
    """Get retriever, building index if necessary"""
    embeddings = get_embeddings()
    
    # Check if the actual index file exists, not just the directory
    index_file = os.path.join("faiss_index", "index.faiss")
    
    if os.path.exists(index_file):
        logger.info("Loading existing FAISS index")
        try:
            vectorstore = FAISS.load_local(
                "faiss_index", 
                embeddings, 
                allow_dangerous_deserialization=True
            )
            return vectorstore.as_retriever(search_kwargs={"k": 3})
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            logger.info("Rebuilding index...")
            return build_rag_index().as_retriever(search_kwargs={"k": 3})
    else:
        logger.info("No FAISS index found, building new one...")
        return build_rag_index().as_retriever(search_kwargs={"k": 3})