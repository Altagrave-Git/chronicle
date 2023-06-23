from django.db import models


class Message(models.Model):
    sender = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender
    
    class Meta:
        ordering = ['timestamp']