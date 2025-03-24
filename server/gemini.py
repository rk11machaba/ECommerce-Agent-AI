from dotenv import load_dotenv
import os

load_dotenv()

gemini_key = os.getenv("gemini_key")

# configure api key
import os
os.environ["GOOGLE_API_KEY"] = gemini_key

# use gemini for prompting
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

gemini = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# try simple prompt
prompt = "Explain the concept of blockchain in one line"

# call llm
response = gemini.invoke(prompt)

# print response
print(response.content)

PROMPT = "Explain {topic} in two points"
prompt = ChatPromptTemplate.from_template(PROMPT)

chain = (
    prompt
    |
    gemini
)

response = chain.invoke({"topic": "Gemini"})
print(response.content)

print("..." * 30)
response = chain.invoke({"topic": "Quantam Computing"})
print(response.content)