from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
import time
from groq import RateLimitError

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    doc = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(doc)
    return chunks

def answer_question(question, filename):
    chunks = process_pdf(os.path.join('uploads', filename))
    
    llm = ChatGroq(
        model="llama3-70b-8192",
        temperature=0.7,
        api_key=GROQ_API_KEY
    )

    system = "You are a helpful AI assistant. Answer the user's query based on the given context"
    human = """Answer the following question based on the given context
    {question}

    Context: {context}"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", human)
    ])
    chain = prompt | llm

    context = "\n".join([chunk.page_content for chunk in chunks])
    response = chain.invoke({"question": question, "context": context})
    return response.content



def answer_question(question, filename):
    chunks = process_pdf(os.path.join('uploads', filename))
    
    max_retries = 3
    retry_delay = 120  # 2 minutes

    for attempt in range(max_retries):
        try:
            llm = ChatGroq(
                model="llama3-70b-8192",
                temperature=0.7,
                groq_api_key=GROQ_API_KEY
            )

            system = "You are a helpful AI assistant. Answer the user's query based on the given context"
            human = """Answer the following question based on the given context
            {question}

            Context: {context}"""

            prompt = ChatPromptTemplate.from_messages([
                ("system", system),
                ("human", human)
            ])
            chain = prompt | llm

            # Limit the context size
            max_context_tokens = 4000  # Adjust this value as needed
            context = "\n".join([chunk.page_content for chunk in chunks])
            context = context[:max_context_tokens]  # Simple truncation, you might want to use a more sophisticated method

            response = chain.invoke({"question": question, "context": context})
            return response.content

        except RateLimitError as e:
            if attempt < max_retries - 1:
                print(f"Rate limit reached. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Please try again later.")
                raise e

    return "Unable to process the request due to rate limiting."