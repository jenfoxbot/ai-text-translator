# ai-text-translator

![Cover Image](/images/Cover2.jpg)

## Intro
This project makes text translation easier, faster, and more accessible! It uses Azure AI Translate to translate text or documents. You can translate between any of the 100+ languages supported by AI Language (full list here). In other words, you can upload a document in any (supported) language and get that document translated to any (supported) language of your choosing!

**More details:**

The program prompts the user (you!) for a desired target language. It outputs a list of supported languages that match your target language(s) along with its corresponding language code. Use the language code for the next input, which will translate the text file of your choosing!
The program prints and saves the translated file with an updated file name! Yay!

**Read time:** 5 min

**Build time:** <5 min

## Set up Azure AI Translator
Let's sign up for Azure AI Translator and get our API keys!

1. Sign up for a [free Azure account here](https://aka.ms/azure/live-captions). Your free trial lasts 30 days and includes $200 Azure credits.

2. Once you're logged in to your Azure dashboard, select 'Create a Resource'.
3. Select (or search for) Translator. (Or [click this link](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation) to create directly.)
4. When deployment is done, navigate to the resource you created.
6. In the 'Overview' page, click on your resource.
7. From here, grab the key, endpoint, and region for your Language resource. Under Resource Management, select 'Keys and Endpoint'.
    ![Cover Image](/images/AzurePortal-GetKeyandEndpt.jpg)
    * Copy one of the keys (either one is fine), the Location/Region, and the Endpoint URL. Save these for later!

Onward to the code!

**Need more help?** Check out the [full quickstart here](https://learn.microsoft.com/en-us/azure/ai-services/translator/quickstart-text-rest-api?tabs=csharp).

## Code Setup
1. Clone the GitHub repo:  https://github.com/jenfoxbot/ai-text-translator
2. In the project folder, navigate to the /src folder.
3. Create a .env file to store your Cognitive Services secrets. Paste the following code:
    `TRANSLATOR_TEXT_SUBSCRIPTION_KEY=YOURKEYHERE
    TRANSLATOR_TEXT_ENDPOINT=YOURENDPOINTHERE`

    Replace "YOURKEYHERE" with your Language Service key.
    Replace "YOURENDPOINTHERE" with your Language Service endpoint.
1. In main.py, update the location (or region) in Line 19 to match your selected region.
1. In main.py, update the  text_file_path variable in Line 22 to point to the file that you want to translate. The Translator service supports [a whole bunch of file types](https://learn.microsoft.com/en-us/azure/ai-services/translator/document-translation/reference/get-supported-document-formats) (although full disclosure I have not tested them all).
Note: I included a test text file (pomplemousse.txt) which you can use to test the program :)

## Install Libraries and Run the Code!
Install the libraries/dependencies you'll need with the following command:

`pip install -r requirements.txt`

When that's finished, run the program with the following command:

`python main.py`

This will take you through a prompt process where you specify your target language, grab the language code (e.g. for English you'd use 'en' or for Spanish you'd use 'es'), and then input that into the target language for translation.

If the program runs successfully, you'll see the translated text print to your screen (you can disable this by commenting out line 132). You'll also have a new file with the same name + the translation language (e.g. "pomplemousse.txt_translated_to_af.txt" -- okay yes it's a lil' messy but it does the job :P).

That's it! Go forth and translate all the things!! And of course, modify the program however you see fit.

## Going Further
1. Specify a target directory to save multiple files.
1. Add a 'choose file' option (would need an environment that supports a GUI).
1. Update the program to translate a single file to multiple languages or a bunch of files to the same language!
Have fun :)
