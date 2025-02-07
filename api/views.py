from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Task, Subtask, Contact
from api.serializers import TaskSerializer, SubtaskSerializer, ContactSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
# Create your views here.

# ModelViewSet gibt automatisch = 'GET', 'POST', 'PUT', 'DELETE'.
# GET /tasks/ → Alle Tasks abrufen.
# POST /tasks/ → Neuen Task erstellen.
# GET /tasks/{id}/ → Einen bestimmten Task abrufen.
# PUT /tasks/{id}/ → Einen Task aktualisieren.
# DELETE /tasks/{id}/ → Einen Task löschen.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        category = self.request.query_params.get('board_category')
        if category:
            return self.queryset.filter(board_category=category)
        return self.queryset

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        contact_ids = request.data.pop('contact_ids', [])
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            task = serializer.save()
            task.contacts.set(contact_ids)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        task = self.get_object()
        print("🔥 PUT Request erhalten:", json.loads(request.body)) 
        print(f"🔄 Update Request für Task {task.id}: {request.data}") # Debugging
        return super().update(request, *args, **kwargs)

class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    # def get_queryset(self):
    #     return Contact.objects.filter(user=self.request.user) 

class SummaryView(APIView):
    def get(self, request):
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(status="done").count()
        pending_tasks = total_tasks - completed_tasks

        task_counts = {
            "to-do": Task.objects.filter(status="to-do").count(),
            "in-progress": Task.objects.filter(status="in-progress").count(),
            "await-feedback": Task.objects.filter(status="await-feedback").count(),
            "done": completed_tasks,
            "total-tasks": total_tasks,
            "urgent": Task.objects.filter(priority="urgent").count(),
            "completed-percentage": round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0,
        }
        return Response(task_counts)
    
class BoardView(APIView):
    def get(self, request): 
        tasks = Task.objects.all().values()
        return Response({"board": list(tasks)})