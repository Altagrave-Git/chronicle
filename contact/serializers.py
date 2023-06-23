from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.Serializer):
    sender = serializers.CharField(max_length=100)
    contact = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=2000)
    timestamp = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Message.objects.create(**validated_data)

    class Meta:
        model = Message
        fields = ['sender', 'contact', 'content', 'timestamp']