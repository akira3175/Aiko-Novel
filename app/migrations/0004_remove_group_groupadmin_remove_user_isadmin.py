# Generated by Django 5.0.2 on 2024-03-15 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_group_is_group_admin_group_groupadmin_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='groupAdmin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='isAdmin',
        ),
    ]
