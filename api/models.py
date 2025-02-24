from django.db import models

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
    icon = models.CharField(max_length=255, blank=True, null=True, default="/static/default.svg")
    contacts = models.ManyToManyField("Contact", related_name="tasks")

    def __str__(self):
        return self.title
    
class Subtask(models.Model): 
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="subtasks")  
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)  

    def __str__(self):
        return self.title 


class Contact(models.Model):
    name = models.CharField(max_length=255)    
    email = models.EmailField(unique=True)    
    phone = models.CharField(max_length=20)     
    color = models.CharField(max_length=7, default='#000000') 

    def __str__(self):
        return self.name
    
class Board(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name