# Generated by Django 3.1 on 2022-04-04 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_comments'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comments',
        ),
    ]
