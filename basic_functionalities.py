import cohere_nlp
import gemini
import requests
import json
# API Key
with open("config.json") as f:
    config = json.load(f)

WEATHER_API_KEY = config.get("WEATHER_API_KEY")

def get_weather(SYSTEM_PROMPT, LOCATION="Toronto"):
    API_URL = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={LOCATION}&aqi=no"
    # Make the API request
    response = requests.get(API_URL)
    SYSTEM_PROMPT = "You are a personal assistant that goes by the name Wingman. You are helpful and friendly, and have the voice of Voice.MALE_UKBUTLER. You are tasked with helping the user with their daily tasks. You can play music, stop music, and have conversations with the user. You can also provide jokes, facts, and other information. Output your response in plaintext (without any formatting like bold or underline), and limit your response to at most 2 short sentences at most while sounding as human as possible. Here are your past messages: deque([], maxlen=5)"
    if response.status_code == 200:
        json_response = response.json()  # Store the JSON response
        location = json_response["location"]
        current_weather = json_response["current"]
        
        # Extracting relevant details
        city = location["name"]
        country = location["country"]
        temp_c = current_weather["temp_c"]
        
        weather_report = f"The weather in {city}, {country} is {int(temp_c)} degrees."
        bot_response = gemini.get_response(f"Provide the user with the current weather and a general description of the weather (you could use the windchill values, humidity, etc.. anything else you may think helpful). {SYSTEM_PROMPT}. Your rsponse should start with {weather_report}")
        print(bot_response)
        return bot_response
    else:
        return "I couldn't get the weather for you."

def personal_assistant(text, system_prompt):
    return gemini.get_response(f"{system_prompt}. Here is the user prompt: {text}")