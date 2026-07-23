import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("MONGO_DB_NAME", "LegalMind")
 
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
 
db = client[DB_NAME]
 
users_collection = db["users"]
lawyers_profiles_collection = db["lawyers_profiles"]
documents_collection = db["documents"]
chat_history_collection = db["chat_history"]
appointments_collection = db["appointments"]
quizzes_collection = db["quizzes"]
achievements_collection = db["achievements"]
 
try:
    client.admin.command("ping")
    logger.info(f"Connected to MongoDB at {MONGO_URI}, database '{DB_NAME}'")
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    logger.error(f"Could not connect to MongoDB at {MONGO_URI}: {e}")