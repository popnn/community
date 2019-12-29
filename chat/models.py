from django.db import models

# Create your models here.
class ChatMessage(models.Model):
    chatroom_name = models.CharField(max_length=50)
    message_id = models.AutoField(primary_key=True)
    message_text = models.TextField(max_length=500)
    user_id = models.IntegerField()
    message_time = models.DateTimeField(auto_now_add=True) 