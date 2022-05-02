# Generated by Django 3.1.13 on 2022-05-02 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cmail', models.CharField(blank=True, max_length=100, null=True)),
                ('message', models.TextField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Contact Us Messages',
                'db_table': 'd_contact_us',
            },
        ),
        migrations.CreateModel(
            name='UserStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homepage_hits_login', models.IntegerField(blank=True, default=0, null=True)),
                ('homepage_hits_anonymous', models.IntegerField(blank=True, default=0, null=True)),
                ('spinx_hits', models.IntegerField(blank=True, default=0, null=True)),
                ('spinx_hits_anonymous', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'd_user_stat',
                'get_latest_by': 'id',
            },
        ),
    ]
