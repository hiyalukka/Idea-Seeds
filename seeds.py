import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["idea_seeds"]
seeds = db["seeds"]

client.admin.command("ping")
print("Connected to Atlas!")