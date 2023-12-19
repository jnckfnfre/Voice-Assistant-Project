# Functionality and Tools

**what it is and what it does:**

**Voice Assistant that can be used to set reminders and search the internet.**

When you run the script, you can tell the program using your voice “At 5:00 remind me to throw the trash” and it send you an SMS notification at 5:00 to throw the trash, storing all reminders with mongoDB

When you ask the voice assistant any other question, it will search the internet and repeat back to you a summarized version of its findings using web scraping and machine learning library, as well as print a Google link to view more

**Software, Tools, Libraries, etc.**

- PyCharm
- MongoDB
    - database to store reminders
- Python
- Flask
    - Not necessary for right now, but will need it if I ever want this to be able to run non-locally
- Git Control
- speech_recognition and/or sounddevice, PyAudio libraries
    - for speech recognition
- Twilio API
    - to send SMS reminders
- BeautifulSoup
    - for web scraping
- SpaCy
    - to extract key phrases and information from the results of the web scraping
- Hugging Face Transformers
    - Machine Learning library to create a summary of the extracted information
- subprocess
    - texttospeech import to easily repeat results and prompts out loud
