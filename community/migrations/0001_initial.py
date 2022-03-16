# Generated by Django 3.2.11 on 2022-03-16 02:13

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0001_initial'),
        ('tradingSystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_title', models.CharField(max_length=100)),
                ('comment_content', models.TextField()),
                ('comment_time', models.DateTimeField(auto_now=True)),
                ('comment_photo', imagekit.models.fields.ProcessedImageField(null=True, upload_to='comment', verbose_name='评论图片')),
                ('comment_stock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.stocktable')),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tradingSystem.usertable')),
            ],
            options={
                'db_table': 'comment_table',
                'ordering': ['comment_time'],
            },
        ),
        migrations.CreateModel(
            name='DiscussTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discuss_content', models.CharField(max_length=100)),
                ('discuss_time', models.DateTimeField(auto_now=True)),
                ('discuss_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.commenttable')),
                ('discuss_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tradingSystem.usertable')),
            ],
        ),
    ]
