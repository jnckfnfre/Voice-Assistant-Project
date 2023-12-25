#this file will be used to process the speech and parse information to create a reminder
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import dateparser
import spacy

FILENAME_FROM_MIC = "REMINDER_INPUT.WAV"
VOICE_TEXT_FILENAME = "REMINDER_TO_TEXT.txt"

# initialize the recognizer
r = sr.Recognizer()


def recognize_from_file(audioFile, reminderTextFile):
    # open the file
    with sr.AudioFile(audioFile) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data) 

    with open(reminderTextFile, "w") as outputFile:
        outputFile.write(text)


def recognize_from_microphone(file_to_write):
    SAMPLE_RATE=44100
    duration = 7  # seconds
    audio_recording = sd.rec(duration * SAMPLE_RATE, samplerate=SAMPLE_RATE, channels=1, dtype='int32')
    print("Recording Audio")
    sd.wait()
    print("Audio recording complete")
    wav.write(file_to_write, SAMPLE_RATE, audio_recording) #write to wav file

def parseReminderDate(reminderTextFile):
    nlp = spacy.load("en_core_web_lg")

    with open(reminderTextFile, "r") as inputFile:
        reminder = inputFile.read()

    doc = nlp(reminder)


    task = " ".join([token.text for token in doc if token.pos_ in ["VERB", "NOUN", "PROPN", "PRON"]])
    date = " ".join([token.text for token in doc if token.pos_ in ["NUM"]])
    time = " ".join([token.text for token in doc if token.pos_ in ["TIME"]])


    reminder_datetime = dateparser.parse(reminder)
    print("Task: " + task)
    print("Date: " + str(reminder_datetime))
    print("Time: " + str(time))


if __name__ == "__main__":
    #recognize_from_microphone(FILENAME_FROM_MIC)
    #recognize_from_file(FILENAME_FROM_MIC, "reminderoutput.txt")
    parseReminderDate("reminderoutput.txt")