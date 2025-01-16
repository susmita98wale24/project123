# Generated by Django 5.1.3 on 2024-12-11 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_book_created_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='Category',
        ),
        migrations.RemoveField(
            model_name='book',
            name='ISBN',
        ),
        migrations.RemoveField(
            model_name='book',
            name='Language',
        ),
        migrations.RemoveField(
            model_name='book',
            name='book_title',
        ),
        migrations.RemoveField(
            model_name='book',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='book',
            name='file',
        ),
        migrations.RemoveField(
            model_name='book',
            name='image',
        ),
        migrations.RemoveField(
            model_name='book',
            name='publication_country',
        ),
        migrations.AlterField(
            model_name='book',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publication_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
