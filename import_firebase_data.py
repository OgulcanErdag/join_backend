import json
from api.models import Task, Contact, Subtask  
from datetime import datetime


with open('firebase_data.json', 'r', encoding='utf-8', errors='ignore') as file:
    data = json.load(file)


contact_mapping = {}  
if "contacts" in data:
    for key, contact in data["contacts"].items():
        obj, created = Contact.objects.get_or_create(
            email=contact["email"],
            defaults={
                "name": contact.get("name", ""),
                "phone": contact.get("phone", ""),
                "color": contact.get("color", "#000000"),
            }
        )
        contact_mapping[key] = obj  
    print("📌 Kontakte importiert!")


if "tasks" in data:
    for key, task in data["tasks"].items():
        due_date = None
        if task.get("due_date"):
            try:
                due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            except ValueError:
                print(f"⚠️ Fehler beim Umwandeln des Datums für Task: {task['title']}")

        task_obj = Task.objects.create(
            title=task.get("title", ""),
            description=task.get("description", ""),
            due_date=due_date,
            priority=task.get("priority", "medium"),
            status=task.get("status", "to-do"),
            task_category=task.get("task_category", "Technical Task"),
            board_category=task.get("board_category", "to-do")
        )

        
        if "contacts" in task:
            for contact_key in task["contacts"]:
                if contact_key in contact_mapping:
                    task_obj.contacts.add(contact_mapping[contact_key])

        print(f"📌 Task importiert: {task_obj.title}")

print("✅ Alle Firebase-Daten wurden erfolgreich in Django gespeichert!")
