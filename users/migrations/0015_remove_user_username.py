# Generated by Django 4.0.5 on 2022-08-05 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
