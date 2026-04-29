import json

with open("data/health-data.json", "r") as file:
    data = json.load(file)

chatbot_data = {}

for disease in data["diseases"]:
    disease_name = disease["name"].lower()
    chatbot_data[disease_name] = disease["description"]

    for symptom in disease["symptoms"]:
        symptom = symptom.lower()
        chatbot_data[symptom] = f"Possible disease: {disease['name']}"

with open("data/healthcare_chatbot_data.json", "w") as file:
    json.dump(chatbot_data, file, indent=4)

print("Dataset converted successfully!")