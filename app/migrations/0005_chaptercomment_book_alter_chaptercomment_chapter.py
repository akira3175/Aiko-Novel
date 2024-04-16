# Generated by Django 5.0.1 on 2024-04-15 18:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_userinfo_role_id_remove_userinfo_date_join_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chaptercomment',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='book_comments', to='app.book'),
        ),
        migrations.AlterField(
            model_name='chaptercomment',
            name='chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chapter_comments', to='app.chapter'),
        ),
    ]