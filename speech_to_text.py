import time

from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx3
import chatbot_functions_library as Chat_Bot

Frame_Rate = 16000
Channels = 1

Speech_Model = Model(r"C:\Users\HEZRON WEKESA\Desktop\AI group project\Speech Recognition\speech_to_text_model\vosk-model-small-en-us-0.15") #
recognizer = KaldiRecognizer(Speech_Model, Frame_Rate) # PASS MODEL AND FREQUENCY 16000


def chat(message):
    statistics = Chat_Bot.predict_class(message)
    bot_response = Chat_Bot.get_response(statistics)
    print(bot_response)
    speak(bot_response)


def speak(say = 'Yes, am listening'):
    engine.say(say)
    engine.runAndWait()


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
engine.say('Hello, My Name Is Purity. How May I help you. Any Time You Need Me just call My Name')
engine.runAndWait()



mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=Channels, rate=Frame_Rate, input=True, frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(4096, exception_on_overflow = False)
    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        if 'purity' in text[14:-3]:
            speak()
            time.sleep(1)
            while True:
                data = stream.read(4096, exception_on_overflow=False)
                if recognizer.AcceptWaveform(data):
                    text = recognizer.Result()
                    print(text[14:-3])
                    chat(text[14:-3])
                    time.sleep(4)







