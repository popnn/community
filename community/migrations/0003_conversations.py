# Generated by Django 2.2.4 on 2019-12-23 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_delete_conversations'),
    ]

    operations = [
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
    ]