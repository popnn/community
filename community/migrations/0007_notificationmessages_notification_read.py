# Generated by Django 2.2.4 on 2020-01-05 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0006_notificationmessages'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationmessages',
            name='notification_read',
            field=models.IntegerField(default=1, max_length=1),
            preserve_default=False,
        ),
    ]
