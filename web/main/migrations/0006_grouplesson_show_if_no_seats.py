# Generated by Django 5.0.5 on 2024-11-05 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_grouplesson_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouplesson',
            name='show_if_no_seats',
            field=models.BooleanField(default=False, verbose_name='отображать, если нет мест'),
        ),
    ]
