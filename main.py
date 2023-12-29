from VoiceReader import get_text
from ExtractingTaskAndDate import extract_task_and_date

def main():
    # text_from_voice = get_text()
    # print(text_from_voice)
    taskAndTime = extract_task_and_date("remind me to go running at 5:00 p.m.")

if __name__ == "__main__":
    main()