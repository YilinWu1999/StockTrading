# Generated by Django 3.2.11 on 2022-03-15 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newstable',
            old_name='news_source',
            new_name='news_src',
        ),
    ]
