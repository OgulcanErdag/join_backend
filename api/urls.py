from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, SubtaskViewSet, ContactViewSet, SummaryView, BoardView

# Da ich die EndPunkte brauche, benutze ich DefaultRouter.
# DefaultRouter() erzeugt automatisch die API-Endpoints für ModelViewSet.
# Jetzt sind folgende Endpunkte verfügbar:
    # GET /api/tasks/ → Alle Tasks abrufen.
    # POST /api/tasks/ → Neuen Task erstellen.
    # GET /api/tasks/{id}/ → Task abrufen.
    # PUT /api/tasks/{id}/ → Task aktualisieren.
    # DELETE /api/tasks/{id}/ → Task löschen.


router = DefaultRouter()
router.register(r'tasks', TaskViewSet)  # Task-Endpunkte automatisch registrieren.
router.register(r'contacts', ContactViewSet)  # Kontakte hinzufügen.
router.register(r'subtasks', SubtaskViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Alle Endpunkte unter `/api/` , Diese Zeile macht, dass die API-Root (`/api/`) ViewSets anzeigt.
    path('summary/', SummaryView.as_view(), name="summary"),  # summary/ ist erreichbar unter /api/summary/, aber es taucht nicht in /api/ auf.(manuell).
    path('board/', BoardView.as_view(), name="board"),
]