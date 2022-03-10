# Generated by Django 3.2.11 on 2022-03-09 13:30

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockTable',
            fields=[
                ('stock_ts', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('stock_symbol', models.CharField(max_length=6)),
                ('stock_name', models.CharField(max_length=45)),
                ('stock_industry', models.CharField(max_length=45)),
                ('stock_market', models.CharField(max_length=45)),
                ('stock_list_date', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'stock_table',
            },
        ),
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_no', models.CharField(max_length=18, unique=True)),
                ('user_name', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=45)),
                ('phone_number', models.CharField(max_length=45, unique=True)),
                ('user_email', models.EmailField(max_length=254, unique=True)),
                ('photo_url', imagekit.models.fields.ProcessedImageField(default='avatar/default.png', upload_to='avatar', verbose_name='头像')),
                ('account_num', models.CharField(max_length=45, null=True)),
                ('account_type', models.CharField(max_length=45, null=True)),
                ('account_balance', models.FloatField(null=True)),
                ('freeze', models.BooleanField(default=False)),
                ('account_opened', models.BooleanField(default=True)),
                ('last_login', models.CharField(max_length=45, null=True)),
            ],
            options={
                'db_table': 'user_table',
            },
        ),
    ]