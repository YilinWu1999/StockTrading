# Generated by Django 3.2.11 on 2022-03-03 14:34

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tradingSystem', '0003_auto_20220301_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertable',
            name='photo_url',
            field=imagekit.models.fields.ProcessedImageField(default='avatar/default.png', upload_to='avatar', verbose_name='头像'),
        ),
    ]
