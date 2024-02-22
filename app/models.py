from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your models here.
# Change forms register django
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
