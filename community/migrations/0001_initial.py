# Generated by Django 2.2.4 on 2019-12-23 21:03

import community.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityComments',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('discussion_id', models.IntegerField()),
                ('comment_author_id', models.CharField(max_length=64)),
                ('comment_publish_date', models.DateTimeField(auto_now_add=True)),
                ('comment_description', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='CommunityDiscussions',
            fields=[
                ('discussion_id', models.AutoField(primary_key=True, serialize=False)),
                ('discussion_author_id', models.CharField(max_length=64)),
                ('discussion_publish_date', models.DateTimeField(auto_now_add=True)),
                ('discussion_title', models.CharField(max_length=32)),
                ('discussion_description', models.TextField(max_length=500)),
                ('discussion_maximum_comments', models.IntegerField(default=100)),
                ('discussion_type', models.CharField(max_length=8)),
                ('discussion_tags', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='ConversationMessages',
            fields=[
                ('conversation_id', models.IntegerField()),
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('message_text', models.TextField(max_length=500)),
                ('user_id', models.IntegerField()),
                ('message_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Conversations',
            fields=[
                ('conversation_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_ids', models.TextField(default='')),
                ('conversation_title', models.CharField(default='', max_length=32)),
                ('conversation_history', models.TextField(default='')),
                ('admin_id', models.CharField(max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfiles',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=24)),
                ('user_description', models.TextField(max_length=256, null=True)),
                ('user_following', models.TextField(default='')),
                ('user_threads', models.TextField(default='')),
                ('user_profile_image', models.ImageField(default='profile/profile.jfif', upload_to=community.models.get_image_path)),
                ('user_date_joined', models.DateTimeField(auto_now_add=True)),
                ('user_saved_threads', models.TextField(default='')),
            ],
        ),
    ]
