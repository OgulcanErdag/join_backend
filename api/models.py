from django.db import models

# Create your models here.

# In Django möchten wir sicherstellen, dass eine Aufgabe nur einen dieser Werte haben kann.
# Dafür nutzen wir choices, damit keine falschen Werte gespeichert werden.
# Ohne choices könnten falsche Werte in die Datenbank gelangen.

class Task(models.Model):
    STATUS_CHOICES = [
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('await-feedback', 'Await Feedback'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('urgent', 'Urgent'),
    ]

    TASK_CATEGORY_CHOICES = [
        ('Technical Task', 'Technical Task'),
        ('User Story', 'User Story'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to-do')
    task_category = models.CharField(max_length=20, blank=True, null=True, choices=TASK_CATEGORY_CHOICES)
    board_category = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to-do')

    contacts = models.ManyToManyField("Contact", related_name="tasks")

    def __str__(self):
        return self.title
    
class Subtask(models.Model):  # task = models.ForeignKey("Task") → Jede Subtask gehört zu einer Task , related_name="subtasks" → So können wir von Task aus auf alle Subtasks zugreifen.
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="subtasks")  # Beziehung zur Haupt-Task
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)  # Standardwert: nicht erledigt

    def __str__(self):
        return f"{self.title} ({'Done' if self.completed else 'Pending'})"


class Contact(models.Model):
    name = models.CharField(max_length=255)     # Kontaktname, max. 255 Zeichen.
    email = models.EmailField(unique=True)      # EmailField(unique=True), weil jeder Kontakt eine eindeutige E-Mail haben sollte.
    phone = models.CharField(max_length=20)     # Telefonnummer, als CharField(max_length=20)
    color = models.CharField(max_length=7, default='#000000')  # Zufällig generierte Farbe für UI-Darstellung.

    def __str__(self):
        return self.name