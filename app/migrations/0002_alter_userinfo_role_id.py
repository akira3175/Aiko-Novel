# Generated by Django 5.0.1 on 2024-04-02 03:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='role_id',
            field=models.ForeignKey(default=-999, on_delete=django.db.models.deletion.CASCADE, to='app.role'),
        ),
    ]
