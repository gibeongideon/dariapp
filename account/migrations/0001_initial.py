# Generated by Django 3.1.13 on 2022-04-30 08:31

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountAnalytic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 30, 11, 31, 47, 370535), null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('gain', models.FloatField(blank=True, default=0, null=True)),
                ('all_bets', models.IntegerField(blank=True, default=1, null=True)),
                ('t_bal', models.FloatField(blank=True, default=0, null=True)),
                ('t_wit', models.FloatField(blank=True, default=0, null=True)),
                ('t_in', models.FloatField(blank=True, default=0, null=True)),
                ('t_out', models.FloatField(blank=True, default=0, null=True)),
                ('r_cred', models.FloatField(blank=True, default=0, null=True)),
                ('diffe', models.FloatField(blank=True, default=0, null=True)),
                ('flag', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AccountSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 30, 11, 31, 47, 370535), null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('min_redeem_refer_credit', models.FloatField(blank=True, default=1000, null=True)),
                ('auto_approve', models.BooleanField(blank=True, default=False, null=True)),
                ('auto_approve_cash_trasfer', models.BooleanField(blank=True, default=False, null=True)),
                ('withraw_factor', models.FloatField(blank=True, default=1, null=True)),
            ],
            options={
                'db_table': 'd_accounts_setup',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 30, 11, 31, 47, 370535), null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('rate', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
            ],
            options={
                'verbose_name_plural': 'Currencies',
                'db_table': 'd_currency',
            },
        ),
        migrations.CreateModel(
            name='RegisterUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 30, 11, 31, 47, 370535), null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('success', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RefCreditTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 30, 11, 31, 47, 370535), null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='amount')),
                ('succided', models.BooleanField(blank=True, default=False, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_refer_credit_trans', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'd_refcredit_trans',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='RefCredit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 30, 11, 31, 47, 370535), null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('current_bal', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('credit_from', models.CharField(blank=True, max_length=200, null=True)),
                ('closed', models.BooleanField(blank=True, null=True)),
                ('has_record', models.BooleanField(blank=True, null=True)),
                ('approved', models.BooleanField(blank=True, default=False, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ref_accountcredit_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'd_refcredits',
            },
        ),
        migrations.CreateModel(
            name='CashWithrawal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 30, 11, 31, 47, 370535), null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('tokens', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('approved', models.BooleanField(blank=True, default=False, null=True)),
                ('cancelled', models.BooleanField(blank=True, default=False, null=True)),
                ('withrawned', models.BooleanField(blank=True, null=True)),
                ('confirmed', models.BooleanField(blank=True, null=True)),
                ('has_record', models.BooleanField(blank=True, null=True)),
                ('withr_type', models.CharField(blank=True, default='shop', max_length=100, null=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.currency')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_withrawals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'd_withrawals',
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='CashTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 30, 11, 31, 47, 370535), null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('approved', models.BooleanField(blank=True, default=False, null=True)),
                ('cancelled', models.BooleanField(blank=True, default=False, null=True)),
                ('success', models.BooleanField(blank=True, null=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('recipient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipientss', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='senderss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CashDeposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 30, 11, 31, 47, 370535), null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('tokens', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('confirmed', models.BooleanField(blank=True, default=False, null=True)),
                ('deposited', models.BooleanField(blank=True, null=True)),
                ('deposit_type', models.CharField(blank=True, default='Shop Deposit', max_length=100, null=True)),
                ('has_record', models.BooleanField(blank=True, null=True)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.currency')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_deposits', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'd_deposits',
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime(2022, 4, 30, 11, 31, 47, 370535), null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('token_count', models.IntegerField(blank=True, default=0, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('actual_balance', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('withraw_power', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('refer_balance', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('trial_balance', models.DecimalField(blank=True, decimal_places=2, default=50000, max_digits=12, null=True)),
                ('cum_deposit', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('cum_withraw', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('active', models.BooleanField(blank=True, default=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_accounts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'd_accounts',
                'ordering': ('-user_id',),
            },
        ),
    ]
