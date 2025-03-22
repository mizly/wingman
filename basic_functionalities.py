import nlp

def personal_assistant(text, system_prompt):
    return nlp.get_response(f"{system_prompt}. Here is the user prompt: {text}")