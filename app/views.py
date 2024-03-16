from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout # thu vien xac thuc
from django.contrib.auth.models import User
from django.contrib import messages # thu vien thong bao
from .models import Book, Member, User, Group
from django import forms

# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        if password == repassword:
            myuser = User.objects.create_user(username=username, email=email, password=password)
            myuser.save()
            messages.success(request, "Your account has been registered")
            return redirect('home')
        else:
            messages.error(request, "Passwords do not match")

    return redirect('home')

def loginPage(request):
    if request.user.is_authenticated:
        return render(request, 'app/home.html', {'name': request.user.username})
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return render(request, 'app/home.html', {'name': user.username})
        else:
            messages.error(request, "Username or password is incorrect!")

    return render(request, 'app/home.html')

def logoutPage(request):
    logout(request)
    return redirect('home')
    
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

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['groupname']
        
        
def addGroup(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            # Thêm người tạo nhóm vào bảng Member với vai trò là "admin"
            Member.objects.create(user=request.user, group=group, teamrole='admin')
            messages.success(request, "Group created successfully")
    context = {'form': form}
    return render(request, 'addgroup.html', context)

# def addGroup(request):
#     form = GroupForm()
#     # member_form = MemberForm()  # Tạo một instance của MemberForm

#     if request.method == 'POST':
#         form = GroupForm(request.POST)
#         # member_form = MemberForm(request.POST)
        
#         if form.is_valid(): # and member_form.is_valid():
#             group = form.save()

#             # # Lấy dữ liệu từ member_form và tạo một thành viên mới
#             # username = member_form.cleaned_data['username']
#             # email = member_form.cleaned_data['email']
#             # new_member = User.objects.create_user(username=username, email=email)

#             # # Thêm người tạo nhóm vào bảng Member với vai trò là "admin"
#             # Member.objects.create(user=new_member, group=group, teamrole='admin')

#             messages.success(request, "Group created successfully")
#             return redirect('home')
    
#     context = {'form': form}
#     return render(request, 'addgroup.html', context)

def deleteGroup(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    group.delete()
    messages.success(request, "Group deleted successfully")
    return redirect('home')

def deleteMember(request, group_id, member_id):
    group = get_object_or_404(Group, pk=group_id)
    member = get_object_or_404(Member, pk=member_id)
    member.delete()
    messages.success(request, "Member deleted successfully")
    return redirect('group_detail', group_id=group.id)
