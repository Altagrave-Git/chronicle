from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    sender = serializers.CharField(max_length=100)
    contact = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=2000)
    timestamp = serializers.DateTimeField(read_only=True)
    is_new = serializers.BooleanField(allow_null=True, required=False)
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
    
    def update(self, instance, **validated_data):
        instance.sender = validated_data.get('sender', instance.sender)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.content = validated_data.get('content', instance.content)
        instance.is_new = validated_data.get('is_new', instance.is_new)
        instance.save()
        return instance

    class Meta:
        model = Message
        fields = ['sender', 'contact', 'content', 'is_new']