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
        GPIO.output(11,GPIO.HIGH)
        audio=r.record(source,duration=4)
        GPIO.output(11,GPIO.LOW)
        try:
                
                text=r.recognize_google(audio)
                print("You said: {}".format(text))
        except:
                print("Sorry, could not recognize your voice.")
    return text
    
def conv():
    global text_to_be_analyzed
    global response
    text_to_be_analyzed=str(stt())
    response=dialogflowinteract()
    printresponse(response)

def tts(text):
    os.system("espeak ' " +text+ " ' ")

   
def sql_search(name):
    global directions
    global results
    print(name)
    temp=['%'+name+'%']
    print(temp[0])
    conn = sqlite3.connect(r'/home/pi/Desktop/FYP-20/test.db')
    cur = conn.cursor()
    if (intent=='BookSearch_no'):
        cur.execute("""select distinct * from lib where Title like (?)""",(temp[0],))
        results = cur.fetchall()
        
    elif (intent=='AuthorSearch'):
        cur.execute("""select distinct * from lib where Authors like (?)""",(temp[0],))
        results = cur.fetchall()
    #print(results[0][-1])
    #print(results[0][-1])
    print(results)
    row_no=results[0][-1]
    route={"1":"Go to the row 1","2":"Go to the row 2","3":"Go to the row 3","4":"Go to the row 4","5":"Go to the row 5","6":"Go to the row 6","7":"Go to the row 7","8":"Go to the row 8","9":"Go to the row 9","10":"Go to the row 10","11":"Go to the row 11","12":"Go to the row 12","13":"Go to the row 13","14":"Go to the row 14","15":"Go to the row 15","16":"Go to the row 16","99":"Go to the row 99"}
    directions=route[row_no]
    return directions

def auth_search(name):
    new_name=name[1:]
    print(new_name)
    global final_result
    for x in range(len(results)):
        #print(results[x][2])
        if (new_name in results[x][2]):
            res=[]
            res=results[x]
            x=list(res)
            final_result=x[-1]
    #print(Authors)
    return final_result


def sql_search2(name):
    global results,row_no
    global directions
    x=name[1:]
    print(x)
    temp=['%'+name[1:]+'%']
    
    print(temp[0])
    conn = sqlite3.connect(r'/home/pi/Desktop/FYP-20/test.db')
    cur = conn.cursor()
    #cur.execute("""select distinct * from lib where Title like (?) AND Authors like (?)""",(temp[0],temp1[0],))
    cur.execute("""select distinct * from lib where Title like (?)""",(temp[0],))
   # cur.execute("""select distinct * from lib where Title= ?""",[bname])
    results = cur.fetchall()
    #print(results[0][-1])
    #print(results)
    
    row_no=auth_search(aname)
    
    route={"1":"Go to the row 1","2":"Go to the row 2","3":"Go to the row 3","4":"Go to the row 4","5":"Go to the row 5","6":"Go to the row 6","7":"Go to the row 7","8":"Go to the row 8","9":"Go to the row 9","10":"Go to the row 10","11":"Go to the row 11","12":"Go to the row 12","13":"Go to the row 13","14":"Go to the row 14","15":"Go to the row 15","16":"Go to the row 16","99":"Go to the row 99"}
    directions=route[row_no]
    #return directions


def extract_name(response):
    global aname, bname
    bn=str(response.query_result.parameters.fields["Book"])
    an=str(response.query_result.parameters.fields["Author"])
    bname=bn.split(":")
    bname=str(bname[1])
    bname=bname.replace('"','')
    bname=bname.replace('\n','')
    print(bname)
    aname=an.split(":")
    aname=str(aname[1])
    aname=aname.replace('"','')
    aname=aname.replace('\n','')
    
    print(aname)

    
def printresponse(response):
    global intent
    global auth_name
    global rep
    print("Query text:", response.query_result.query_text)
    print("Detected intent:", response.query_result.intent.display_name)
    intent=response.query_result.intent.display_name
    
    #**********BookSearch Intent*****************************
    
    if (intent=='BookSearch'):
        tts(response.query_result.fulfillment_text)
        rep=response.query_result.fulfillment_text
	
    elif(intent=='BookSearch_yes'):
        tts(response.query_result.fulfillment_text)
        rep=response.query_result.fulfillment_text
	
    elif(intent=='BookSearch_yes_custom'):
        print(response)
        extract_name(response)
        sql_search2(bname)
        tts(directions)
        rep=directions
                
    elif(intent=='BookSearch_no'):
        x=response.query_result.parameters.values()
        book_name=str(x[0])
        sql_search(book_name)
        tts(directions)
        rep=directions
                
    #************AuthorAndBookSearch Intent************************************
    elif (intent=='AuthorAndBookSearch'):
        print(response)
        extract_name(response)
        sql_search2(bname)
        tts(directions)
        rep=directions
            
    #****************AuthorSearch Intent************        
    elif (intent=='AuthorSearch'):
        x=response.query_result.parameters.values()
        auth_name=str(x[0])
        sql_search(auth_name)
        tts(directions)
        rep=directions
        
    elif (intent=='Repeat'):
        tts(rep)
                
    #***********other intents*************************
    else:
        tts(response.query_result.fulfillment_text)
        rep=response.query_result.fulfillment_text
        
    
import os
import dialogflow_v2 as dialogflow
import dialogflow
from google.api_core.exceptions import InvalidArgument
import speech_recognition as sr
import sqlite3
#import pandas as pd
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

# red led should be ON
GPIO.output(23,GPIO.HIGH)
GPIO.output(18,GPIO.LOW)
while 1:    
    dialogflowinit()
#intent="Default_Welcome_Intent"
    text_to_be_analyzed=str(stt())
    if (text_to_be_analyzed=='hello item'):
        #green led should be ON
        tts("welcome. How may i assist you?")
        GPIO.output(23,GPIO.LOW)
        GPIO.output(18,GPIO.HIGH)
        conv()
        GPIO.output(18,GPIO.LOW)
        
    else:
        #red led should be ON
        GPIO.output(23,GPIO.HIGH)
        GPIO.output(18,GPIO.LOW)
        continue
        
    while intent!='Endofconversation':
        conv()
# in the stt function the led should be on while it is listening
