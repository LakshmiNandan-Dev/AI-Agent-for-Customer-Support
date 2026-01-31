from langchain_community.embeddings import HuggingFaceEmbeddings
import logging
import os

logger = logging.getLogger(__name__)

def get_embeddings():
    """
    Returns HuggingFace embeddings using langchain-community
    """
    cache_dir = os.getenv("HF_HOME", "/app/.cache/huggingface")
    os.makedirs(cache_dir, exist_ok=True)
    
    logger.info("Initializing embeddings model...")
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True},
        cache_folder=cache_dir,
    )
    
    logger.info("Embeddings model loaded successfully")
    return embeddings