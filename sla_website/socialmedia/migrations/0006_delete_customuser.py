# Generated by Django 2.2a1 on 2019-02-08 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedia', '0005_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]