from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        User,
        related_name="sent_requests",
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User,
        related_name="received_requests",
        on_delete=models.CASCADE
    )
    note = models.TextField(blank=True, null=True)
    accepted = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.sender} -> {self.receiver}"