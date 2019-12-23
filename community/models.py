from django.db import models
import json

# Create your models here.
def get_image_path(instance, filename):
    extension = filename.split('.')[-1]
    return 'profile/{}.{}'.format(str(instance.user_id), extension)

class UserProfiles(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=24)
    user_description = models.TextField(max_length=256, null=True)
    user_following = models.TextField(default="")
    user_threads = models.TextField(default="")
    user_profile_image = models.ImageField(upload_to=get_image_path, default="profile/profile.jfif")
    user_date_joined = models.DateTimeField(auto_now_add=True)
    user_saved_threads = models.TextField(default="")

class CommunityDiscussions(models.Model):
    discussion_id = models.AutoField(primary_key=True)
    discussion_author_id = models.CharField(max_length=64)
    discussion_publish_date = models.DateTimeField(auto_now_add=True)
    discussion_title = models.CharField(max_length=32)
    discussion_description = models.TextField(max_length=500)
    discussion_maximum_comments = models.IntegerField(default=100)
    discussion_type = models.CharField(max_length=8)
    discussion_tags = models.TextField(default="")
    
class CommunityComments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    discussion_id = models.IntegerField()
    comment_author_id = models.CharField(max_length=64)
    comment_publish_date = models.DateTimeField(auto_now_add=True)
    comment_description = models.TextField(max_length=500)

class Conversations(models.Model):
    conversation_id = models.AutoField(primary_key=True)
    user_ids = models.TextField(default='')
    conversation_title = models.CharField(max_length=32, default='')
    conversation_history = models.TextField(default='')
    admin_id = models.CharField(max_length=24)

class ConversationMessages(models.Model):
    conversation_id = models.IntegerField()
    message_id = models.AutoField(primary_key=True)
    message_text = models.TextField(max_length=500)
    user_id = models.IntegerField()
    message_time = models.DateTimeField(auto_now_add=True) 
