# Generated by Django 5.0.7 on 2024-07-15 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_alter_member_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='zipcode',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
