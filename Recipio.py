#this is gonna be the start of the file for wednesday
import pathlib
import textwrap
import google.generativeai as genai
import allrecipesdatabase as ardb
#"set the environment variable, Replace /path/to/your/credentials.json with the actual path to your Google Cloud credentials file."
import os
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '%APPDATA%\gcloud\application_default_credentials.json'
#"authenticate with google cloud"
'''
from google.oauth2 import service_account
credentials = service_account.Credentials.from_service_account_file(
    'test'
)
'''
#"create a storage client"
#from google.cloud import storage
#client = storage.Client(credentials=credentials)
import configparser
from google.colab import userdata
from IPython.display import display
from IPython.display import Markdown

#api key
GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

from PIL import Image
import numbers
#i just copied this off of the link, it's a helper method used to clean up response objects and return them
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
#this is the function that we're gonna use to run the image recognition thing
def imager(image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(["Generate a list of the ingredients provided in the following image using * as bulletpoints", image], stream=False)
    to_markdown(response.text)
    print(response.text)
    userinput(response)
#this is the function that represents response generation
def userinput(contents):
    userResponse=input("Is this what you are looking for? [Yes or No]")
    if(userResponse=="No"):
        #if sensitive topic or first candidate not sufficient
        print("Here are alternatives or why you might not see something: ")
        print(contents.candidates)
        contents.prompt_feedback
    elif(userResponse=="Yes"):
        #the output should be an array of all the ingredients
        hold=[]
        ret=[]
        for token in contents.text:
            if((token.isalpha or token.isspace()) and not token=="*"):
                hold.append(token)
            #if the current token is a newline or the last element
            if(token=="\n"):
                ret.append(''.join(hold[:-1]))
                hold=[]
            #if(token is contents.text[-1]):
                #ret.append(''.join(hold))
        print(ret)
        for i,x in enumerate(ret):
            if(x=='' or len(x)==1 or len(x)==2):
                ret.pop(i);
        return ret
    else:
      #potential solution: gen_recipe(image)?
        print("Please enter either Yes or No")
        userinput(contents)
#This is the function where you interact with the backend (aka the allrecipesdatabase)        
def store(arr):
    #hold holds the resulting array with parsed ingredients
    hold=imager(image)
    ardb.getIngredientList(hold)
def process_image(image):
    image.show()  # Display the processed image
'''
client = storage.Client()
bucket = client.get_bucket('Downloads')
blob = bucket.get_blob('spices.jpeg')
blob.download_to_filename('spices.jpeg')
'''
image_path = "spices.jpeg"
input_image = Image.open(image_path)
process_image(input_image)
imager(input_image)
print("imager passed?")
