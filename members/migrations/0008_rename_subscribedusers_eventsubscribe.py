# Generated by Django 5.0.7 on 2024-07-21 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_subscribedusers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SubscribedUsers',
            new_name='EventSubscribe',
        ),
    ]
