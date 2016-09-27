import json
import pyaudio
import wave
from watson_developer_cloud import AlchemyLanguageV1
import speech_recognition as sr
from os import path
import subprocess
from tkinter import *

def check_valid_flight_number(string_numbers_said):
    numbers = {"zero": 0, "one": 1, "two": 2, "three": 3,
               "four": 4, "five": 5, "six": 6,
               "seven": 7, "eight": 8, "nine": 9}

    nums = string_numbers_said.split(" ")
    boolean_valid = False
    csv_num_and_name = []
    for num in nums:
        if num not in numbers:
            boolean_valid = False
        else:
            boolean_valid = True
    if boolean_valid:
        database_numbers = ""
        for anum in nums:
            try:
                database_numbers += str(numbers[anum])
            except:
                boolean_valid = False
        csv_num_and_name.append(database_numbers)
        print(database_numbers)
        say_name()
        record_flight_number("full_name.wav")
        name = speech_to_text("full_name.wav")
        csv_num_and_name.append(name)
        print(name)
        play_both_right()
        record()

    else:
        invalid_flight()
        return []
    return csv_num_and_name


def play_both_right():
    CHUNK = 1024

    wf = wave.open("both_right.wav", 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()

    p.terminate()


def invalid_flight():
    CHUNK = 1024

    wf = wave.open("invalid_flight_number.wav", 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()

    p.terminate()

def say_flight_number():
    CHUNK = 1024

    wf = wave.open("flight_number_ask.wav", 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()

    p.terminate()

def say_name():
    CHUNK = 1024

    wf = wave.open("full_name_ask.wav", 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()

    p.terminate()

def say_ok():
    CHUNK = 1024

    wf = wave.open("both_right.wav", 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()

    p.terminate()

def record_flight_number(string_file_name):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = string_file_name
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def flight_number():
    boolean_valid = False
    flight_number = "123"
    for num in flight_number:
        try:
            int(num)
        except:
            print("incorrect flight number")

def speech_to_text(string_file_name):
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), string_file_name)
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source) # read the entire audio file

    # recognize speech using Sphinx
    try:
        final_speech_to_text = r.recognize_sphinx(audio)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    finally:
        final_speech_to_text = r.recognize_sphinx(audio)
    return final_speech_to_text

def analyze():
    alchemy_language = AlchemyLanguageV1(api_key='a61d0c6e1cccf27052e986c5cc1dca21dacd9c2b')
    jsonStr = json.dumps(
        alchemy_language.combined(
        text = speech_to_text("output.wav"),
        extract='keywords',
        sentiment=1,
        max_items=10),
        indent=2)
    return jsonStr

#record audio clip
def record():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def make_csv():
    csv_str = ""
    speech = speech_to_text("passenger_flight_number.wav")
    num_and_name = check_valid_flight_number(speech)
    num_and_name.append(speech_to_text("output.wav"))
    jsonStr = analyze()
    jsonFile = json.loads(jsonStr)
    total_sentiment = 0.0
    count = 0
    keywords = []
    length = len(keywords)
    for item in jsonFile["keywords"][length]:
        if item == "text":
            keywords.append(jsonFile["keywords"][0]["text"])
        elif item == "sentiment":
            total_sentiment += (float(jsonFile["keywords"][count]["sentiment"]["score"])
                                * float(jsonFile["keywords"][count]["relevance"]))
        count += 1
    average_sentiment = total_sentiment/count * 100
    average_sentiment = (average_sentiment + 100) / 20
    average_sentiment = average_sentiment * 1.5 if average_sentiment > 5 else average_sentiment * 0.7
    average_sentiment_str = str(average_sentiment)

    num_and_name.append(keywords)
    num_and_name.append(average_sentiment_str)
    for item in num_and_name:
        if type(item) == list:
            csv_str += (item[0] + ";")
        else:
            csv_str += (item + ";")
    f = open("data.txt", "w")
    f.write("Flight Number: " + csv_str)
    return csv_str

def main():
    say_flight_number()
    record_flight_number("passenger_flight_number.wav")
    make_csv()
    print(analyze())
    subprocess.call("node firebase.js")


def gui():
    app = Tk()
    app.configure(background = "white")
    app.title("Customer Experience")
    photo = PhotoImage(file="deltalogo.png")
    label2 = Label(app, image=photo, bg = "white")
    label = Label(app, text="Customer Experience Improvement", font=("Corbel", 35), bg = "white")

    label3 = Label(app, text="IBM Watson Keyword & Sentiment Analyzer", font=("Corbel", 28), bg = "white")

    logo = PhotoImage(file="Aviato_Logo.png")

    logo_label = Label(app, image=logo)
    button = Button(text="Start", command=main, height = 1, width = 6, font = ("Corbel", 30), bg = "white")
    logo_label.pack()
    label2.pack()
    label.pack()
    label3.pack()
    button.pack(padx=5, pady=10)

    mainloop()
gui()
