import speech_recognition as sr


r=sr.Recognizer()

with sr.Microphone() as source:
	r.adjust_for_ambient_noise(source, duration=2)
	print("speak anything")
	audio=r.record(source,duration=5)
	try:
		text=r.recognize_google(audio)
		print("you said: {}".format(text))
	except:
		print("sorry could not recognize your voice")
