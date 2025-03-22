from google import genai
import json
with open("config.json") as f:
    config = json.load(f)

gemini_api_key = config.get("GEMINI_API_KEY")
client = genai.Client(api_key="AIzaSyAF6PzwnX4j-qMphSlcTX226Tuti0dADZs")

def get_response(text):
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=text,
    )
    return response.text