# Generated by Django 4.1.2 on 2023-06-04 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_room_from_user_room_to_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='image',
        ),
        migrations.RemoveField(
            model_name='room',
            name='name',
        ),
    ]