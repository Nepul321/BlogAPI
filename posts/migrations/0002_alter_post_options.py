# Generated by Django 4.0.1 on 2022-02-05 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-datetime']},
        ),
    ]