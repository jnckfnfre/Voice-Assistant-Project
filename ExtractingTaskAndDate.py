import sys
import nlp
import spacy
import dateparser
from spacy.matcher import Matcher
from datetime import datetime, timedelta


# Test sentences
# text = [
#     "Remind me to go running at 5:00 a.m. tomorrow.",
#     "Set a reminder to throw the trash at 8:00 p.m. today.",
#     "Remind me to get everyone's number at 8:00 p.m. on Tuesday.",
#     "Set a reminder to wash my dad's car at 10:00 a.m. tomorrow.",
#     "Remind me to not fall asleep in class at 1:15 p.m. today.",
#     "Remind me to take a nap before class on Thursday at 2:00 p.m.",
#     "Remind me to work out tomorrow at 10:00 a.m.",
#     "Remind me to get two eggs tomorrow at 8:00 a.m.",
#     "Set a reminder to go to sleep at 10:00 p.m.",
#     "Remind me to go home after class at 3:00 p.m. tomorrow.",
#     "Remind me to get a job in 45 minutes.",
#     "Remind me to grab eggs in 3 hours."
# ]

# Time-related words for filtering tasks
time_words = ["at", "on"]

# Phrases to stop including in the task
stop_phrases = ["tomorrow at", "on Monday at", "on Tuesday at", "on Wednesday at", "on Thursday at", "on Friday at", "on Saturday at", "on Sunday at"]

# Settings for dateparser
dateparser_settings = {
    "PREFER_DATES_FROM": "future"
}

def pattern1_approach(doc, matches):
    tasks = []
    time_strings = []
    for match_id, start, end in matches:
        # Existing logic for extracting the task
        task_start = [tok.i for tok in doc[start:end] if tok.text.lower() == "to"][0] + 1
        task_end = start
        for i in range(start, end):
            if doc[i].lower_ in time_words or (doc[i].ent_type_ in ["TIME", "DATE"]):
                task_end = i
                break

        task = doc[task_start:task_end].text
        tasks.append(task)

        # Extracting the time part
        time_start = end
        time_string = doc[time_start:].text
        time_strings.append(time_string)

    # Filter for the longest unique task
    if tasks:
        longest_task = max(tasks, key=len)
        reminder_time = dateparser.parse(time_strings[tasks.index(longest_task)], settings=dateparser_settings)
        print(f"Reminder Task: {longest_task}, Reminder Time: {reminder_time}")
        print((longest_task, reminder_time))
        print("pattern1")


def handle_duration_approach(doc, matches):
    tasks = []
    durations = []

    for match_id, start, end in matches:
        if nlp.vocab.strings[match_id] == "REMINDER_DURATION":
            # Extracting the duration part
            duration_string = doc[start:end].text
            durations.append(duration_string)

            # Extracting the task
            # Task is assumed to be between "remind me to" / "set a reminder to" and the duration
            task_start = None
            for i, token in enumerate(doc):
                if token.lower_ in ["remind", "set"] and i + 2 < len(doc) and doc[i + 2].lower_ == "to":
                    task_start = i + 3
                    break
            if task_start is not None:
                task_end = start
                task = doc[task_start:task_end].text.strip()
                tasks.append(task)

    # Filter for the longest unique task and corresponding duration
    if tasks:
        longest_task = max(tasks, key=len)
        # Assuming the duration corresponding to the longest task is at the same index
        corresponding_duration = durations[tasks.index(longest_task)]

        # Parsing the duration to get the future time
        reminder_time = dateparser.parse(corresponding_duration, settings={'PREFER_DATES_FROM': 'future'})
        print(f"Reminder Task: {longest_task}, Duration: {corresponding_duration}, Reminder Time: {reminder_time}")
        print((longest_task,reminder_time))
        print("duration approach")

def extract_task_and_date(text):

    nlp = spacy.load("en_core_web_sm")
    print(nlp)
    matcher = Matcher(nlp.vocab)
    print(matcher)

    # Updated Pattern for "Remind me to" and "Set a reminder to"
    pattern1 = [
        {"TEXT": {"IN": ["Remind", "Set"]}},
        {"TEXT": "me", "OP": "?"},
        {"TEXT": "a", "OP": "?"},
        {"TEXT": "reminder", "OP": "?"},
        {"TEXT": "to"},
        {"IS_ALPHA": True, "OP": "+"},
        {"TEXT": "'s", "OP": "?"},
        {"IS_ALPHA": True, "OP": "*"},
    ]
    pattern2 = [
        {"LOWER": "in"},
        {"IS_DIGIT": True},
        {"LOWER": {"IN": ["minute", "minutes", "hour", "hours", "day", "days", "week", "weeks"]}},
    ]

    matcher.add("REMINDER_DURATION", [pattern2])

    # Add pattern1 to the matcher
    matcher.add("REMINDER_TASK", [pattern1])
    doc = nlp(text)
    matches = matcher(doc)
    print(matcher)

    has_pattern1 = False
    has_pattern2 = False
    for match_id, start, end in matches:
        if nlp.vocab.strings[match_id] == "REMINDER_TASK":
            has_pattern1 = True
        elif nlp.vocab.strings[match_id] == "REMINDER_DURATION":
            has_pattern2 = True
    print(has_pattern2)
    print(has_pattern1)
    if has_pattern2:
        return handle_duration_approach(doc, matches)
    elif has_pattern1:
        return pattern1_approach(doc, matches)

if __name__ == "__main__":

    extract_task_and_date("Remind me to go running at 5:00 a.m. tomorrow.")