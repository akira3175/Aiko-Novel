# Generated by Django 5.0.1 on 2024-03-19 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_book_date_alter_book_quantityvol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
