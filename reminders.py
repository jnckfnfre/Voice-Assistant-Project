#will be used to do all reminder related processing
#
#we will use a dictionary to emulate our database right now

"""
reminders = {
    reminderID: int (unique) - PK
    message/description: String
    reminderTime: datetime
    createdTime: datetime
    status: String or ENUM or int (can map number to status code)
}
"""

class ReminderDictionary:
    def __init__(self):
        self.data = {}
        self.next_id = 1

    def addReminder(self, message, reminderTime, createdTime, status):
        reminder_id = self.next_id
        self.next_id += 1
        reminder = {
            "reminderID": reminder_id,
            "message": message,
            "reminderTime": reminderTime,
            "createdTime": createdTime,
            "status": status
        }

        self.data[reminder_id] = reminder

    def deleteReminder(self, reminder_id):
        if reminder_id in self.data:
            del self.data[reminder_id]

    def getReminder(self, reminder_id):
        if reminder_id in self.data:
            return self.data[reminder_id]


    def getAllReminders(self):
        return self.data

    def deleteAllReminders(self):
        self.data = {}
        self.next_id = 1