from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.Serializer):
    sender = serializers.CharField(max_length=100)
    contact = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=2000)
    timestamp = serializers.DateTimeField(read_only=True)
    date = serializers.SerializerMethodField(allow_null=True, read_only=True)
    time = serializers.SerializerMethodField(allow_null=True, read_only=True)

    def get_date(self, obj):
        date = obj.timestamp.strftime("%d/%m/%Y")
        return date
    
    def get_time(self, obj):
        time = obj.timestamp.strftime("%H:%M:%S")
        return time

    def create(self, validated_data):
        return Message.objects.create(**validated_data)

    class Meta:
        model = Message
        fields = ['sender', 'contact', 'content', 'timestamp']