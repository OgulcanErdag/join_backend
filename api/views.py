from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, viewsets
from rest_framework.response import Response
from api.models import Task, Subtask, Contact
from .serializers import TaskSerializer, SubtaskSerializer, ContactSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsAuthenticatedOrGuest


class TaskViewSet(ModelViewSet):
    queryset, serializer_class, permission_classes, authentication_classes, http_method_names = Task.objects.all(), TaskSerializer, [AllowAny],[TokenAuthentication], ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        board_category = self.request.query_params.get("board_category", None)
        if board_category:
            return Task.objects.filter(board_category=board_category)
        return Task.objects.all() 

    def perform_create(self, serializer):
        serializer.save().contacts.set(self._get_contact_ids())
        task = serializer.save()

        subtasks_data = self.request.data.get("subtasks", [])
        for subtask in subtasks_data:
            Subtask.objects.create(task=task, **subtask)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        contact_ids = request.data.get("contact_ids", None)
        subtasks_data = request.data.get("subtasks", [])
        priority = request.data.get("priority", instance.priority)
        
        if contact_ids is not None:
            if isinstance(contact_ids, list) and len(contact_ids) > 0:
                instance.contacts.set(contact_ids)

        if isinstance(subtasks_data, list) and subtasks_data:
            instance.subtasks.all().delete()

            for subtask in subtasks_data:
                if "title" in subtask and "completed" in subtask:
                    Subtask.objects.create(task=instance, title=subtask["title"], completed=subtask["completed"])
        return super().partial_update(request, *args, **kwargs)

    def _get_contact_ids(self):
        ids = self.request.data.get("contact_ids", [])
        return list(ids) if isinstance(ids, (list, tuple, set)) else [int(i) for i in ids if str(i).isdigit()]
    
class SubtaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrGuest]
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

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
            "completed-percentage": round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0,}
        return Response(task_counts)  
    
class BoardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request): 
        tasks = Task.objects.all().values()
        return Response({"board": list(tasks)})