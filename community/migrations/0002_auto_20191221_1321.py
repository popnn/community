# Generated by Django 2.2.7 on 2019-12-21 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofiles',
            name='user_following',
            field=models.TextField(default=''),
        ),
    ]
