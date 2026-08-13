from database.connections import (
    users_collection,
    lawyers_profiles_collection,
    documents_collection,
    chat_history_collection,
    appointments_collection,
    quizzes_collection,
    achievements_collection
)


users_collection.insert_one({
    "name": "Raya",
    "email": "raya@gmail.com",
    "role": "public_user"
})
print("Users done")


lawyers_profiles_collection.insert_one({
    "name": "Arun Kumar",
    "specialization": "Criminal Law",
    "experience": 5
})
print("Lawyers done")


documents_collection.insert_one({
    "document_name": "Rental Agreement",
    "type": "legal"
})
print("Documents done")


chat_history_collection.insert_one({
    "question": "What is IPC?",
    "answer": "Legal information"
})
print("Chat done")


appointments_collection.insert_one({
    "lawyer": "Arun Kumar",
    "status": "pending"
})
print("Appointments done")


quizzes_collection.insert_one({
    "title": "Law Basics"
})
print("Quizzes done")


achievements_collection.insert_one({
    "badge": "First Quiz"
})
print("Achievements done")


print("All test data inserted")