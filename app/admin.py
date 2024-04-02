from django.contrib import admin
from app.models import Book, Category, UserInfo, Role
from .models import Group, Member

# Register your models here.
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(UserInfo)
admin.site.register(Role)
admin.site.register(Group)
admin.site.register(Member)
