# Generated by Django 4.1.7 on 2023-05-16 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0019_alter_book_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(default=None, upload_to='static/images/book/covers'),
        ),
    ]
