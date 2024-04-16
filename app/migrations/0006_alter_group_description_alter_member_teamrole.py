# Generated by Django 5.0.1 on 2024-04-16 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_chaptercomment_book_alter_chaptercomment_chapter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.TextField(blank=True, default='Chào mừng bạn xem group chúng tôi', null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='teamrole',
            field=models.CharField(db_index=True, default='Thành viên', max_length=40),
        ),
    ]
