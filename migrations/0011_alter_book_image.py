# Generated by Django 5.1.3 on 2024-12-25 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_book_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, default='books/images/default.jpg', null=True, upload_to='books/images/'),
        ),
    ]