# Generated by Django 3.2.11 on 2022-03-15 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_newstable_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newstable',
            name='news_time',
            field=models.DateTimeField(),
        ),
    ]
