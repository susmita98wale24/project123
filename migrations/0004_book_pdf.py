# Generated by Django 5.1.3 on 2024-12-11 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_book_category_remove_book_isbn_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='books/pdfs/'),
        ),
    ]
