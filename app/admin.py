from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(Book)
admin.site.register(Volume)
admin.site.register(Chapter)
admin.site.register(ChapterComment)
admin.site.register(Category)
admin.site.register(UserInfo)
admin.site.register(Group)
admin.site.register(Member)
admin.site.register(BookFollowing)
