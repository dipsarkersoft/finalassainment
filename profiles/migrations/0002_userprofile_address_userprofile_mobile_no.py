# Generated by Django 5.1.4 on 2025-01-14 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mobile_no',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
