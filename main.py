from reminders import ReminderDictionary



def main():
    reminder_dict = ReminderDictionary()
    reminder_dict.addReminder("Test reminder", "2023-12-19 15:52:00", "2023-12-19 21:00:00", "Incomplete")

    print(reminder_dict.getReminder(1))

    print(reminder_dict.getAllReminders())

    reminder_dict.deleteReminder(1)

    print(reminder_dict.getAllReminders())



if __name__ == "__main__":
    main()
