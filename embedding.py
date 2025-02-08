from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from scraper import scrape_brainlox_courses  # Import scraper function

# Define the persistent storage path for ChromaDB
CHROMA_PATH = r"C:\Users\hp\Desktop\chatbot\chroma_db"

# Load Hugging Face embeddings model
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Scrape the courses and get LangChain Document objects
documents = scrape_brainlox_courses()

# Initialize ChromaDB using LangChain's wrapper (persistence happens automatically)
vector_store = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_function
)

# Add scraped documents to ChromaDB
vector_store.add_documents(documents)

print(f"Stored {len(documents)} courses successfully in ChromaDB")






