import spacy
import dateparser
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

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

# Add pattern1 to the matcher
matcher.add("REMINDER_TASK", [pattern1])

# Test sentences
texts = [
    "Remind me to go running at 5:00 a.m. tomorrow.",
    "Set a reminder to throw the trash at 8:00 p.m. today.",
    "Remind me to get everyone's number at 8:00 p.m. on Tuesday.",
    "Set a reminder to wash my dad's car at 10:00 a.m. tomorrow.",
    "Remind me to not fall asleep in class at 1:15 p.m. today.",
    "Remind me to take a nap before class on Thursday at 2:00 p.m.",
    "Remind me to work out tomorrow at 10:00 a.m.",
    "Remind me to get two eggs tomorrow at 8:00 a.m.",
    "Set a reminder to go to sleep at 10:00 p.m.",
    "Remind me to go home after class at 3:00 p.m. tomorrow"
]

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

for text in texts:
    doc = nlp(text)
    matches = matcher(doc)
    pattern1_approach(doc, matches)
