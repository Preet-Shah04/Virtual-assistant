import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
import openai
import os
from dotenv import load_dotenv

r = sr.Recognizer() # It helps to convert speech to text
engine = pyttsx3.init() # initialize pytsx3
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
newsapi = os.getenv("NEWS_API_KEY")

def speak(text):
    engine.say(text)         #this is copied
    engine.runAndWait()      #this is copied

def processcommand(c):
    if "open google" in c.lower():
        try:
            webbrowser.open("https://www.google.com")
        except Exception as e:
            speak("Couldn't open google")
            print(f"Error : {e}")
    elif "open youtube" in c.lower():
        try:
            webbrowser.open("https://www.youtube.com/")
        except Exception as e:
            speak("Couldn't open youtube")
            print(f"Error : {e}")
    elif "open linkedin" in c.lower():
        try:
            webbrowser.open("https://www.linkedin.com/feed/?trk=guest_homepage-basic_google-one-tap-submit")
        except Exception as e:
            speak("Couldn't Linkedin")
            print(f"Error : {e}")
    elif "open facebook" in c.lower():
        try:
            webbrowser.open("https://www.facebook.com/")
        except Exception as e:
            speak("Couldn't open facebook")
            print(f"Error : {e}")

    elif c.lower().startswith("play"):
        try:
            song = c.lower().replace("play", "").strip()
            for title in musiclibrary.music:
                if title.lower() in song:
                    link = musiclibrary.music[title]
                    webbrowser.open(link)
                    speak(f"Playing {title}")
                    break
            else:
                speak("I couldn't find that song in your library.")
        except Exception as e:
            speak("Something went wrong while trying to play the song.")
            print(f"Error: {e}")
            
    elif "news" in c.lower():
        speak("Here are the top news headlines.")
        try:
            req = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            data = req.json()

            print("Fetched articles:", len(data["articles"]))  

            for article in data["articles"][0:]:
                print(article["title"])
                speak(article["title"])
        except Exception as e:
            speak("Sorry, I could not fetch the news.")
            print(f"Error fetching news: {e}")
    
    elif "help" in c.lower():
        speak("You can ask me to open websites, play songs, fetch news, or answer your questions.")

    elif "exit" in c.lower() or "stop" in c.lower():
        speak("Goodbye!")
        exit()

        
    else:
        try:
                response = client.chat.completions.create(
                    model="gpt-4.1",
                    messages=[
                        {"role": "system", "content": "You are a virtual assistant named Jarvis capable of answering questions like Google or Alexa. Respond naturally."},
                        {"role": "user", "content": c}
                    ]
                )
                reply = response.choices[0].message.content
                speak("Let me look that up for you...")
                speak(reply)
        except Exception as e:
                speak("Sorry, I couldn't process your question.")
                print(f"OpenAI error: {e}")

    
    
    

if __name__=="__main__":
    speak("Initializing Jarvis...")
    while True:
        #Listen for the wake word Jarvis

        # obtain audio from the microphone
      
        # recognize speech using Sphinx
        try:
                # obtain audio from the microphone
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=5,phrase_time_limit=5)

            word = r.recognize_google(audio)

            if word.lower()=="jarvis":
                speak("Ya")
                print(word)
                #Listen for command
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processcommand(command)
                    print(command)

                
            

        except sr.UnknownValueError:
            
            print("Jarvis could not understand audio please Say jarvis again and continue")
        except sr.RequestError as e:
            print("Jarvis error; {0}".format(e))
        except Exception as e:
            print(f"Unexpected error occurerd {e}")