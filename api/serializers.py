from rest_framework import serializers
from api.models import Task, Subtask, Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'  # Alle Felder von Contact in die API aufnehmen

class TaskSerializer(serializers.ModelSerializer):
    contacts = contacts = ContactSerializer(many=True, read_only=True)
    contact_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=Contact.objects.all(), write_only=True) # Sorgt dafür, dass Django IDs akzeptiert, statt komplette JSON-Objekte zu erwarten.
    icon = serializers.CharField(source="get_icon", read_only=True)
    
    id = serializers.ReadOnlyField()
    board_category = serializers.CharField(required=False)
    priority = serializers.CharField()
    
    class Meta:
        model = Task
        fields = '__all__'  # Alle Felder des Task-Modells in JSON umwandeln
        extra_kwargs = {"board_category": {"required": False}}

    def create(self, validated_data):
        contact_ids = validated_data.pop('contact_ids', [])  # Holt Kontakt-IDs aus dem Request
        task = Task.objects.create(**validated_data)
        task.contacts.set(contact_ids)  # Fügt Kontakte zur Task hinzu
        return task

    def update(self, instance, validated_data):
        contact_ids = validated_data.pop('contact_ids', None)
        board_category = validated_data.get('board_category', instance.board_category)  # Falls leer, nimm alten Wert

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.board_category = board_category  # Manuell setzen
            instance.save()

        if contact_ids is not None:
            instance.contacts.set(contact_ids)
        return instance
    
    def get_icon(self, obj):
        return obj.icon if obj.icon else "/static/default.svg" 
class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = '__all__'

    