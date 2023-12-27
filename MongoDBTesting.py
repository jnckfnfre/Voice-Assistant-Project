from datetime import datetime
import pytz
from pymongo import MongoClient

# Assuming you have a datetime in CST
cst_time = datetime.strptime('2023-12-28 05:00:00', '%Y-%m-%d %H:%M:%S')
cst_zone = pytz.timezone('America/Chicago')  # CST/CDT timezone

# Localize the datetime to CST
localized_cst_time = cst_zone.localize(cst_time)

# Convert to UTC
utc_time = localized_cst_time.astimezone(pytz.utc)

print("Original CST Time:", localized_cst_time)
print("Converted UTC Time:", utc_time)


# Create a MongoClient to the running mongod instance
client = MongoClient('localhost', 27017)

# Specify the database to use
db = client['Reminders']  # Replace 'example_database' with your database name

# Specify the collection to use
collection = db['reminder']  # Replace 'example_collection' with your collection name

# Perform operations (for example, listing all documents in the collection)
reminder_document = {
    "reminder_time": utc_time,
    "description": "go running"  # Add more fields as needed
}

# Insert the document into the collection
insert_result = collection.insert_one(reminder_document)
print("Inserted document ID:", insert_result.inserted_id)

# List all documents in the collection (optional)
for document in collection.find():
    print(document)
