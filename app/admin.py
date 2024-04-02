from django.contrib import admin
from app.models import Book, Category, UserInfo, Role

# Register your models here.
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(UserInfo)
admin.site.register(Role)