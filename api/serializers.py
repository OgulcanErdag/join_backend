from rest_framework import serializers
from api.models import Task, Subtask, Contact, Board
from rest_framework import serializers

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__' 
class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__' 
class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = '__all__'
class TaskSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)  
    contact_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Contact.objects.all(),
        source="contacts",  
        write_only=True 
    )
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'board_category', 'task_category', 'subtasks', 'contacts', 'contact_ids']







    