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

# Updated Pattern for sentences starting with a time or date
pattern2 = [
    {"POS": {"IN": ["ADP", "NOUN", "NUM", "DET"]}, "OP": "*"},
    {"TEXT": {"IN": ["remind", "set"]}, "OP": "?"},
    {"TEXT": "me", "OP": "?"},
    {"TEXT": "to"},
    {"IS_ALPHA": True, "OP": "+"},
    {"TEXT": "'s", "OP": "?"},
    {"IS_ALPHA": True, "OP": "*"},
]

# Add patterns to the matcher
matcher.add("REMINDER_TASK", [pattern1, pattern2])

# Test sentences
texts = [
    "Remind me to go running at 5:00 a.m. tomorrow.",
    "Set a reminder to throw the trash at 8:00 p.m. today.",
    "On Thursday at 10:00 a.m., remind me to go to school.",
    "At 10:00 a.m. on Thursday, remind me to pick up my sister.",
    "Remind me to get everyone's number at 8:00 p.m. on Tuesday.",
    "Set a reminder to wash my dad's car at 10:00 tomorrow.",
    "Remind me to not fall asleep in class at 1:15 p.m. today.",
    "Remind me to take a nap before class at 2:25 p.m tomorrow."
]
# Time-related words for filtering tasks
time_words = ["at", "on", "in", "by", "before", "after"]

# Apply the matcher to each text and process tasks
for text in texts:
    doc = nlp(text)
    matches = matcher(doc)

    tasks = []
    time_strings = []

    for match_id, start, end in matches:
        # Extracting the task
        task_start = [tok.i for tok in doc[start:end] if tok.text.lower() == "to"][0] + 1
        task = doc[task_start:end].text
        tasks.append(task)

        # Extracting the time part
        time_start = end
        time_string = doc[time_start:].text
        time_strings.append(time_string)

    # Filter for the longest unique task and remove trailing time word if present
    if tasks:
        longest_task = max(tasks, key=len)
        task_words = longest_task.split()
        if task_words[-1].lower() in time_words:
            longest_task = " ".join(task_words[:-1])

        # Parsing the time string
        reminder_time = dateparser.parse(time_strings[tasks.index(longest_task)])
        print(f"Reminder Task: {longest_task}, Reminder Time: {reminder_time}")
