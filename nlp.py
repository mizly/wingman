import cohere
import os
from dotenv import load_dotenv
load_dotenv()

cohere_api_key = os.getenv("COHERE_API_KEY")

co = cohere.ClientV2(cohere_api_key)
response = co.chat(
    model="command-a-03-2025", 
    messages=[{"role": "user", "content": "hello world!"}]
)

def get_response(text):
    response = co.chat(
        model="command-a-03-2025", 
        messages=[{"role": "user", "content": text}]
    )
    return response.message.content[0].text

if __name__ == "__main__":
    print(get_response("tell me a joke!"))
