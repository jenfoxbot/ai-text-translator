"""This program takes a text file and translates it to a different language using Azure Cognitive Services API.
It also helps you get the corresponding language code for your target translation language!

Author: jenfoxbot
License: MIT
Date: 1/8/2024"""

import os, requests, uuid, json
from dotenv import load_dotenv

#Set up the subscription info for Azure Cog Services
# Load env vars from .env file
load_dotenv()
key = os.environ['TRANSLATOR_TEXT_SUBSCRIPTION_KEY']
endpoint = os.environ['TRANSLATOR_TEXT_ENDPOINT']

# location, also known as region.
# Note: this is required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
location = "eastus"

# ---------------------------- TO DO: Specify file path for the text file to translate -------------------------------
text_file_path = "./pomplemousse.txt"

## STEP 1: get language code for the language you want to translate to

# 1A: Get the input language
def get_input_and_convert_to_lowercase():
    string = input("Please enter target language for translation: ")
    return string.lower()

# 1B: Match the input into a language code
def match_string_to_json_entry(string, json_file):
    with open(json_file, 'r') as f:
        dictionary = json.load(f)

    matches = []     
    for key, value in dictionary:
        if string in key.lower() or string in str(value.lower()):
            matches.append((key, value))
        '''if entry[0].lower() == string:
            return entry[1]'''
    return matches


# 1C: Format the matches
def format_matches(matches):
    print("The table below shows potential matches for your target language. \nLanguage | Cognitive Services Code\n---------------------------------")
    for match in matches:
        print(f"{match[0]} | {match[1]}")

# STEP 2: functions to handle text file to translate
# 2A: read in the text file to translate        
def read_text_file(file_path):
    """This function opens and reads in a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 2B: function to write translated file to disk
def write_to_file(text, file_path):
    """This function writes a text file to local storage."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

# STEP 3: Run Cog Services on the text file to translate it
def detect_language(key, endpoint, text, target_language_code):
    """This function detects the language of a text string."""
    constructed_url = endpoint + '/translate'
    params = {
        'api-version': '3.0',
        'to': [target_language_code] # examples: 'es','sw', 'it']

    }
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text': text
    }]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    #return response[0]['detectedLanguage']['language']
    return response

def translate_text(key, endpoint, text, target_language):
    """This function translates a text string into a target language."""
    constructed_url = endpoint + '/translate'
    params = {
        'api-version': '3.0',
        'to': [target_language]
    }
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text': text
    }]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    return response[0]['translations'][0]['text']

if __name__ == "__main__":   
    # Pull in Cog Services language codes
    print("First, let's get our Cognitive Services language code. \n")

    langcode_file_path = "./CogServ_LanguageCodeDict.json"
    input_language_code = []
    
    # Loop until you get a match
    while input_language_code == []:
        lowercase_lang = get_input_and_convert_to_lowercase()
        input_language_code = match_string_to_json_entry(lowercase_lang, langcode_file_path)
        if input_language_code == []:
            print("Sorry, no language matches found. Please try again.\nIf you're unsure of spelling, try a shorter input (e.g. 'Afri' to get a match for 'Afrikaans').")
    
    print(format_matches(input_language_code))

    # Read text from file
    text_to_translate = read_text_file(text_file_path)
    trans_lang = input("Enter target language code: ")    
    
    # Detect the language of the text
    detected_language = detect_language(key, endpoint, text_to_translate, trans_lang)
    print("detected language: ", detected_language[0]['detectedLanguage']['language'])
    print("detected language score: ", detected_language[0]['detectedLanguage']['score'])
    print("translated into: ", detected_language[0]['translations'][0]['to'])
    print("translated text: ", detected_language[0]['translations'][0]['text'])
    
    # save the translated text to a file
    # 1. Create a new file path:
    translated_text_file_path = text_file_path + "_translated_to_" + trans_lang + ".txt"
    # 2. Write to disk
    write_to_file(detected_language[0]['translations'][0]['text'], translated_text_file_path)
    
