# Generated by Django 2.2.5 on 2020-02-02 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0002_auto_20200202_1224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likerecord',
            old_name='like_time',
            new_name='liked_time',
        ),
    ]
