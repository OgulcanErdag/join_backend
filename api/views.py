from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, viewsets
from rest_framework.response import Response
from api.models import Task, Subtask, Contact
from .serializers import TaskSerializer, SubtaskSerializer, ContactSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
import traceback

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset, serializer_class, permission_classes, http_method_names = Task.objects.all(), TaskSerializer, [IsAuthenticated], ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        board_category = self.request.query_params.get("board_category", None)
        if board_category:
            return Task.objects.filter(board_category=board_category)
        return Task.objects.all() 

    def perform_create(self, serializer):
        serializer.save().contacts.set(self._get_contact_ids())

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        contact_ids = request.data.get("contact_ids", None)

        print(f"🔥 Backend: Eingehende contact_ids = {contact_ids}")  # Debugging

        if contact_ids is not None:
            instance.contacts.add(*contact_ids)  
            print(f"✅ Kontakte nach Update: {list(instance.contacts.values_list('id', flat=True))}")  

        return super().partial_update(request, *args, **kwargs)





    def _get_contact_ids(self):
        ids = self.request.data.get("contact_ids", [])
        print(f"🔥 contact_ids aus Request: {ids}")  # Debug-Print
        return list(ids) if isinstance(ids, (list, tuple, set)) else [int(i) for i in ids if str(i).isdigit()]

class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer

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
            "completed-percentage": round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0,
        }
        return Response(task_counts)
    
class BoardView(APIView):
    permission_classes = [AllowAny]
    def get(self, request): 
        tasks = Task.objects.all().values()
        return Response({"board": list(tasks)})