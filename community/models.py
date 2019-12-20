from django.db import models

# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

class UserProfiles(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=24)
    user_description = models.TextField(max_length=256, null=True)
    user_following = models.TextField(null=True)
    user_profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    user_date_joined = models.DateTimeField(auto_now_add=True)

class CommunityDiscussions(models.Model):
    discussion_id = models.AutoField(primary_key=True)
    discussion_author_id = models.CharField(max_length=64)
    discussion_publish_date = models.DateTimeField(auto_now_add=True)
    discussion_title = models.CharField(max_length=32)
    discussion_description = models.TextField(max_length=500)
    discussion_maximum_comments = models.IntegerField(default=100)
    discussion_type = models.CharField(max_length=8)
    
class CommunityComments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    discussion_id = models.IntegerField()
    comment_author_id = models.CharField(max_length=64)
    comment_publish_date = models.DateTimeField(auto_now_add=True)
    comment_description = models.TextField(max_length=500)
