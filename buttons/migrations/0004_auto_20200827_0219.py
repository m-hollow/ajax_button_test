# Generated by Django 3.1 on 2020-08-27 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buttons', '0003_auto_20200827_0157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='users_proxies',
            new_name='users',
        ),
    ]
