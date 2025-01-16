# Generated by Django 5.1.3 on 2024-12-23 15:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_book_rating_book_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publication_year',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
    ]
