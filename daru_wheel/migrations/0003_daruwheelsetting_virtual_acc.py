# Generated by Django 3.1.13 on 2022-04-05 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daru_wheel', '0002_auto_20220401_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='daruwheelsetting',
            name='virtual_acc',
            field=models.FloatField(blank=True, default=500000, null=True),
        ),
    ]
