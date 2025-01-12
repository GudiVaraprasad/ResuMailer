from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Please try again after 5 minutes.")

llm = ChatGroq(
    api_key=api_key,
    model_name="gemma2-9b-it", 
    temperature=0.8,
    max_tokens=1000
)

# Create a simple prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

# Create a response generation function
def generate_response(prompt_text: str) -> str:
    # Create the input for the LLM
    chain = prompt | llm
    response = chain.invoke({"input": prompt_text})
    
    # Extract the text content from the AIMessage object
    return response.content 