from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class ChatRoom(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    participants = models.ManyToManyField(CustomUser, related_name="chatRooms")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat Room: {self.name}"

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message from {self.sender.name} in {self.chat_room.name}"


