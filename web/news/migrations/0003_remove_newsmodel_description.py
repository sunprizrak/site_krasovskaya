# Generated by Django 5.0.5 on 2024-09-16 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_remove_newsmodel_image_newsmodel_file_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsmodel',
            name='description',
        ),
    ]
