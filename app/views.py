from audioop import reverse
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
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

def forOfTransTeam(group_member_counts, groups, join):
    for group in groups:
        member = Member.objects.filter(group=group, teamrole__in = ['owner', 'admin', 'member'])
        group_member_info = {
            'groupname': group.groupname,
            'groupid': group.id,
            'member_count': member.count(),
            'join' : join,
            'is_member': (join == 'Đã tham gia')
        }
        group_member_counts.append(group_member_info)
    
def transTeam(request):
    user = request.user
    user_groups = Member.objects.filter(auth_user=user).values_list('group', flat=True)
    groups = Group.objects.filter(id__in=user_groups)
    other_groups = Group.objects.exclude(id__in=user_groups)
    
    group_member_counts = []
    forOfTransTeam(group_member_counts, groups, 'Đã tham gia')
    forOfTransTeam(group_member_counts, other_groups, 'Chưa tham gia')
    
    context = {
        'group_member_counts': group_member_counts,
    }
    return render(request, 'app/transteam.html', context)

def novelOfTransTeam(request):
    return render(request, 'app/novel-of-trans.html')

def memberOfTransTeam(request, group_id):
    group = Group.objects.get(pk=group_id)
    members = Member.objects.filter(group=group, teamrole__in = ['owner', 'admin', 'member'])
    waiters = Member.objects.filter(group=group, teamrole='waiter')
    return render(request, 'app/member-of-trans.html', {'Members' : members, 'Group':group, 'Waiters': waiters})

def novelWorks(request):
    return render(request, 'app/novelworks.html')

def addGroup(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            groupname = request.POST.get('groupname')
            if Group.objects.filter(groupname=groupname).exists():
                messages.error(request, "Group name already exists")
            else: 
                group = form.save()
                current_user = request.user # Lấy thông tin user hiện tại từ request
                member = Member(auth_user_id=current_user.id, group_id=group.id, teamrole='owner')
                member.save()
                messages.success(request, "Group created successfully")
        else:   
            messages.error(request, "Error add group. Please check the addGroup.")
    return redirect('transteam')

    
def wantToJoin(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if Member.objects.filter(auth_user=request.user, group=group, teamrole='waiter').exists():
        messages.success(request, 'Please waiting for the admin acceptance')
    elif Member.objects.exclude(auth_user=request.user, group=group).exists():
        member = Member(auth_user_id=request.user.id, group_id=group.id, teamrole='waiter')
        member.save()
        messages.success(request, 'Join successfully')
    return redirect('transteam')

def approveMember(request, group_id, member_id):
    group = get_object_or_404(Group, pk=group_id)
    member = get_object_or_404(Member, pk=member_id)
    
    if Member.objects.filter(auth_user=request.user, group=group, teamrole__in=['admin', 'owner', 'member']).exists():
        if request.method == 'POST':
            member.teamrole = "member"
            member.save()
            messages.success(request, "Approve successfully")
    else:
        messages.error(request, "You must have admin/owner/member role in the group to approve members")
    return redirect('member-of-trans-team', group_id=group_id)

def changeRoleToAdmin(request, group_id, member_id):
    # Đổi vai trò thành viên
    group = get_object_or_404(Group, pk=group_id)
    member = get_object_or_404(Member, pk=member_id)
    if Member.objects.filter(auth_user=request.user, group=group, teamrole__in=['admin', 'owner']).exists():
        member.teamrole = "admin"
        member.save()
        messages.success(request, "Change member's role successfully")
    else:
        messages.error(request, "You must have admin/owner role in the group to change member's role")
    return redirect('member-of-trans-team', group_id=group_id)
    
def deleteGroup(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    # Kiểm tra xem người dùng hiện tại có trong nhóm và có vai trò owner trong nhóm đó không
    if Member.objects.filter(auth_user=request.user, group=group, teamrole='owner').exists():
        if request.method == 'POST':
            group.delete()
            messages.success(request, 'Delete group successfully')
    else:
        messages.error(request, "You must have owner role in the group to delete this group")
    return redirect('transteam')

def deleteMember(request, group_id, member_id):
    # Lấy nhóm và thành viên từ cơ sở dữ liệu
    group = get_object_or_404(Group, id=group_id)
    member = get_object_or_404(Member, id=member_id)
    
    if Member.objects.filter(auth_user=request.user, group=group).exists():
        # Kiểm tra xem người dùng hiện tại có vai trò "owner" trong nhóm đó không
        if Member.objects.filter(auth_user=request.user, group=group, teamrole='owner').exists():
            if member.teamrole == "owner" and member.auth_user == request.user:
                messages.error(request, "You can't delete yourself as the owner.")
            else:
                member.delete()
                messages.success(request, "Delete member successfully")
        elif Member.objects.filter(auth_user=request.user, group=group, teamrole='admin').exists():
            if member.teamrole in ["owner", "admin"]:
                messages.error(request, "Can't delete an admin/owner member.")
            else:
                member.delete()
                messages.success(request, "Delete member successfully")
        else:
            messages.error(request, "You must have admin/owner role in the group to delete this member")
    else:
        messages.error(request, "You must be a member of the group to delete this member")
    
    return redirect('member-of-trans-team', group_id=group_id)