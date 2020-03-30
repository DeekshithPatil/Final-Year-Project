def dialogflowinit():
    global DIALOGFLOW_PROJECT_ID
    global SESSION_ID 
    global DIALOGFLOW_LANGUAGE_CODE 
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "testbot-kwvnui-5236f6e1b6d6.json"
    DIALOGFLOW_PROJECT_ID = 'testbot-kwvnui'
    SESSION_ID = "a19316dbac5045a699b19c59589ef248"
    DIALOGFLOW_LANGUAGE_CODE = 'en-US'

def dialogflowinteract():
    global response
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    return response
def stt():
        r=sr.Recognizer()
        with sr.Microphone() as source:
                print("speak anything: ")
                audio=r.record(source,duration=4)
                try:
                        text=r.recognize_google(audio)
                        print("You said: {}".format(text))
                except:
                        print("Sorry, could not recognize your voice.")
        return text
def stt():
        r=sr.Recognizer()
        with sr.Microphone() as source:
                print("speak anything: ")
                audio=r.record(source,duration=4)
                try:
                        text=r.recognize_google(audio)
                        print("You said: {}".format(text))
                except:
                        print("Sorry, could not recognize your voice.")
        return text

def tts(text):
        os.system("espeak ' " +text+ " ' ")

def conv():
    global text_to_be_analyzed
    global response
    text_to_be_analyzed=str(stt())
    if (text_to_be_analyzed=="can you repeat"):
        tts(repeat)
    else:
        response=dialogflowinteract()
        printresponse(response)


def sql_search(name):
    print(name)
    global directions
    conn = sqlite3.connect(r'/home/pi/Desktop/FYP-2019/test.db')
    cur = conn.cursor()
    cur.execute("""select * from lib where Title=(?);""",(name,))
    results = cur.fetchall()
    #print(results)
    directions=results[0][-1]
    return directions

def printresponse(response):
    global intent
    print("Query text:", response.query_result.query_text)
    print("Detected intent:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    intent=response.query_result.intent.display_name
    if (intent=='BookSearch'):
        book_name=(response.query_result.parameters.values())
        #print(x[0])
        sql_search(str(book_name[0]))
        tts(directions)
    else:
        tts(response.query_result.fulfillment_text)

import os, time
import speech_recognition as sr
import dialogflow_v2 as dialogflow
import dialogflow
from google.api_core.exceptions import InvalidArgument
import speech_recognition as sr
import sqlite3


dialogflowinit()
conv()
if (intent=="BookSearch"):
    repeat=directions
else:
    repeat=response.query_result.fulfillment_text
while intent!='Endofconversation':
    conv()
    if (intent=="BookSearch"):
    	repeat=directions
    else:
    	repeat=response.query_result.fulfillment_text

