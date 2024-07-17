# Generated by Django 5.0.7 on 2024-07-17 16:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_member_zipcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(null=True)),
                ('event_name', models.CharField(max_length=255, null=True)),
                ('purpose', models.CharField(max_length=255, null=True)),
                ('amount', models.IntegerField(null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.member')),
            ],
        ),
    ]