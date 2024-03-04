from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import Book
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout # thu vien xac thuc
from django.contrib import messages # thu vien thong bao
from .models import CreateUserForm

# Create your views here.
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'app/register.html', context)

def loginPage(request):
    if request.user.is_authenticated: # kiem tra xac thuc chua
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
        else: messages.info(request, "Username hoặc password không đúng!")
    context = {}
    return render(request, 'app/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')
    
def home(request):
    return render(request, 'app/home.html') 
    
def search(request):
    keywords = request.GET.get('keywords')
    matched_books = []
    all_book = Book.objects.all()
    if all_book:
        for book in all_book:
            if keywords.lower() in book.title.lower():
                matched_books.append(book)
    return render(request, 'app/search.html', {'keywords': keywords,'matched_books': matched_books})

def transTeam(request):
    return render(request, 'app/transteam.html')

def novelOfTransTeam(request):
    return render(request, 'app/novel-of-trans.html')

def novelWorks(request):
    return render(request, 'app/novelworks.html')