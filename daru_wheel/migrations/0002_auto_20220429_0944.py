# Generated by Django 3.1.13 on 2022-04-29 06:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('daru_wheel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stake',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_wp_istakes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='outcome',
            name='cashstore',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cashstores', to='daru_wheel.cashstore'),
        ),
        migrations.AddField(
            model_name='outcome',
            name='stake',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='istakes', to='daru_wheel.stake'),
        ),
    ]
