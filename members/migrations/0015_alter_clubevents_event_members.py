# Generated by Django 5.0.7 on 2024-07-30 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0014_rename_product_clubpicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubevents',
            name='event_members',
            field=models.CharField(db_column='event_members', max_length=255, null=True),
        ),
    ]
