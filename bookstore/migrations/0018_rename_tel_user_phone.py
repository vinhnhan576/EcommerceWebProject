# Generated by Django 4.1.7 on 2023-05-16 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0017_rename_phone_user_tel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='tel',
            new_name='phone',
        ),
    ]
