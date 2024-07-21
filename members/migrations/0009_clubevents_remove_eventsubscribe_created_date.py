# Generated by Django 5.0.7 on 2024-07-21 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_rename_subscribedusers_eventsubscribe'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=255, null=True)),
                ('event_date', models.DateField(null=True)),
                ('event_members', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='eventsubscribe',
            name='created_date',
        ),
    ]
