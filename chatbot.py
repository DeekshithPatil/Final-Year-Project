#########WORKING########
def dialogflowinit():
    global DIALOGFLOW_PROJECT_ID
    global SESSION_ID 
    global DIALOGFLOW_LANGUAGE_CODE 
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "testbot-kwvnui-5236f6e1b6d6.json"
    DIALOGFLOW_PROJECT_ID = 'testbot-kwvnui'
    SESSION_ID = "a19316dbac5045a699b19c59589ef248"
    DIALOGFLOW_LANGUAGE_CODE = 'en-US'

def dialogflowinteract():
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    return response

def printresponse(response):
    print("Query text:", response.query_result.query_text)
    print("Detected intent:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    #print("Response: ", response)
    x=(response.query_result.parameters.values())
    print(x[0])
    print("Fulfillment text:", response.query_result.fulfillment_text)

def repeat():
    x=response.query_result.fulfillment_text
    robot(x)
    
def stt():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("speak anything:")
        audio=r.record(source,duration=3)
        try:
            text=r.recognize_google(audio)
            print("you said:{}".format(text))
        except:
            print("sorry could not recognise your voice")
    return text
def robot(text):
	os.system("espeak ' " +text+ " ' ")

import os ,time
import os
import dialogflow_v2 as dialogflow
import dialogflow
from google.api_core.exceptions import InvalidArgument
import speech_recognition as sr
dialogflowinit()
text_to_be_analyzed=str(stt())
response=dialogflowinteract()
printresponse(response)
fulfillment_text=response.query_result.fulfillment_text
robot(fulfillment_text)
comp="What is the BookName?"



if (fulfillment_text==comp):
    text_to_be_analyzed=str(input("Enter"))
    response=dialogflowinteract()
    printresponse(response)
text_to_be_analyzed=str(input("Enter"))
rep="can u repeat"
if (text_to_be_analyzed==rep):
    repeat()
