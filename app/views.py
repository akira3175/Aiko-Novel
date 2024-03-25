from audioop import reverse
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth import authenticate, login, logout # thu vien xac thuc
from django.contrib.auth.models import User
from django.contrib import messages # thu vien thong bao
from .models import Book, Member, Group, GroupForm
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
    groups = Group.objects.all()
    group_member_counts = []
    for group in groups:
        member_count = Member.objects.filter(group=group).count()
        group_member_info = {
            'groupname': group.groupname,
            'member_count': member_count
        }
        group_member_counts.append(group_member_info)
    context = {
        'group_member_counts': group_member_counts,
    }
    return render(request, 'app/transteam.html', context)

def novelOfTransTeam(request):
    return render(request, 'app/novel-of-trans.html')

def memberOfTransTeam(request):
    members = Member.objects.all()
    return render(request, 'app/member-of-trans.html', {'Members' : members})

def novelWorks(request):
    return render(request, 'app/novelworks.html')

def addGroup(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            # Lấy thông tin user hiện tại từ request
            current_user = request.user
            # Thêm user tạo group vào nhóm với vai trò admin
            member = Member(auth_user_id=current_user.id, group_id=group.id, teamrole='admin')
            member.save()
            messages.success(request, "Group created successfully")
        else:   messages.error(request, "Error add group. Please check the addGroup.")
    return redirect('transteam')

    
# def addMember(request):
#     form = MemberForm()
#     if request.method == 'POST':
#         form = MemberForm(request.POST)
#         if form.is_valid():
#             form.save()
#     return redirect('transteam')

def deleteGroup(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    group.delete()
    messages.success(request, "Group deleted successfully")
    return redirect('transteam')

def deleteMember(request, group_id, member_id):
    group = get_object_or_404(Group, pk=group_id)
    member = get_object_or_404(Member, pk=member_id)
    member.delete()
    messages.success(request, "Member deleted successfully")
    return redirect('group_detail', group_id=group.id)
