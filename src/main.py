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
    string = input("Please enter target language(s) for translation (comma-separated): ")
    return [lang.strip().lower() for lang in string.split(',')]

# 1B: Match the input into a language code
def match_string_to_json_entry(string, json_file):
    with open(json_file, 'r') as f:
        dictionary = json.load(f)

    matches = []     
    for key, value in dictionary:
        if string in key.lower() or string in str(value.lower()):
            matches.append((key, value))
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
def translate_text(key, endpoint, text, target_language_codes):
    """This function detects the language of a text string."""
    constructed_url = endpoint + '/translate'
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text': text
    }]
    translations = {}
    for code in target_language_codes:
        params = {
            'api-version': '3.0',
            'to': [code]
        }
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()
        translations[code] = response[0]['translations'][0]['text']
    return translations

if __name__ == "__main__":   
    # Pull in Cog Services language codes
    print("First, let's get our Cognitive Services language code. \n")

    langcode_file_path = "./CogServices-LanguageCodeDictionary.json"
    input_language_codes = []
    
    # Loop until you get a match
    while not input_language_codes:
        lowercase_langs = get_input_and_convert_to_lowercase()
        for lang in lowercase_langs:
            matches = match_string_to_json_entry(lang, langcode_file_path)
            if matches:
                input_language_codes.extend(matches)
            else:
                print(f"Sorry, no language matches found for '{lang}'. Please try again.\nIf you're unsure of spelling, try a shorter input (e.g. 'Afri' to get a match for 'Afrikaans').")
    
    print(format_matches(input_language_codes))

    # Read text from file
    text_to_translate = read_text_file(text_file_path)
    trans_langs = [input("Enter target language code: ") for _ in input_language_codes]
    
    # Translate the text
    translations = translate_text(key, endpoint, text_to_translate, trans_langs)
    
    for lang, translated_text in translations.items():
        print(f"translated into: {lang}")
        # NOTE: comment out the following line if you don't want to see the translated text
        print(f"translated text: {translated_text}")
        
        # save the translated text to a file
        # 1. Create a new file path:
        translated_text_file_path = text_file_path + "_translated_to_" + lang + ".txt"
        # 2. Write to disk
        write_to_file(translated_text, translated_text_file_path)
