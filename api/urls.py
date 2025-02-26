from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, SubtaskViewSet, ContactViewSet, SummaryView, BoardView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)  
router.register(r'contacts', ContactViewSet) 
router.register(r'subtasks', SubtaskViewSet)

urlpatterns = [
    path('', include(router.urls)),  
    path('summary/', SummaryView.as_view(), name="summary"), 
    path('board/', BoardView.as_view(), name="board"),
]