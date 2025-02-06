from django.contrib import admin
from .models import Task, Subtask, Contact

# Registriere deine Modelle im Admin-Bereich
admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(Contact)