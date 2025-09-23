from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import os
import logging

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env (especially openai api key)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Google Gemini LLM model
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.environ["GOOGLE_API_KEY"], temperature=0.1)
# # Initialize instructor embeddings using the Hugging Face model
instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
vectordb_file_path = "faiss_index"

def create_vector_db():
    try:
        logger.info("Starting vector database creation...")
        
        # Load data from FAQ sheet
        loader = CSVLoader(file_path='codebasics_faqs.csv', source_column="prompt")
        data = loader.load()
        logger.info(f"Loaded {len(data)} documents from CSV")

        # Create a FAISS instance for vector database from 'data'
        vectordb = FAISS.from_documents(documents=data,
                                        embedding=instructor_embeddings)
        logger.info("Created FAISS vector database")

        # Save vector database locally
        vectordb.save_local(vectordb_file_path)
        logger.info(f"Saved vector database to {vectordb_file_path}")
        
        return True
    except Exception as e:
        logger.error(f"Error creating vector database: {str(e)}")
        raise e


def get_qa_chain():
    try:
        # Load the vector database from the local folder
        vectordb = FAISS.load_local(vectordb_file_path, instructor_embeddings)
        logger.info("Loaded vector database successfully")

        # Create a retriever for querying the vector database
        retriever = vectordb.as_retriever(score_threshold=0.7)

        prompt_template = """Given the following context and a question, generate an answer based on this context only.
        In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
        If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

        CONTEXT: {context}

        QUESTION: {question}"""

        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        chain = RetrievalQA.from_chain_type(llm=llm,
                                            chain_type="stuff",
                                            retriever=retriever,
                                            input_key="query",
                                            return_source_documents=True,
                                            chain_type_kwargs={"prompt": PROMPT})

        return chain
    except Exception as e:
        logger.error(f"Error creating QA chain: {str(e)}")
        raise e

if __name__ == "__main__":
    create_vector_db()
    chain = get_qa_chain()
    print(chain("Do you have javascript course?"))