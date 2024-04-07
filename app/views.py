from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from app.models import Book, UserInfo, Category, Role, Member, Group
from app.models import GroupForm
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout # thu vien xac thuc
from django.contrib.auth.models import User
from django.contrib import messages # thu vien thong bao
from .models import UserForm
from forum.models import ForumPost
from django.views.decorators.csrf import csrf_exempt
from django import forms

# Create your views here.

"""Login and Register"""
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        date_join = timezone.now()

        if password == repassword:
            # Tạo một người dùng mới
            myuser = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
            )

            # Tạo một đối tượng UserInfo và liên kết với người dùng mới
            UserInfo.objects.create(username=myuser, full_name=myuser.username, date_join=date_join)

            messages.success(request, "Your account has been registered")
            return redirect('home')
        else:
            messages.error(request, "Passwords do not match")

    return redirect('home')

def checkUsername(request):
    if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        username = request.GET.get('username', '').strip()
        if username:
            try:
                if User.objects.filter(username__iexact=username).exists():
                    return JsonResponse({'is_taken': True})
                else:
                    return JsonResponse({'is_taken': False})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Yêu cầu không hợp lệ.'}, status=400)
    else:
        return JsonResponse({'error': 'Yêu cầu không hợp lệ hoặc không phải là AJAX.'}, status=400)

def checkEmail(request):
    if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        email = request.GET.get('email', '').strip()
        if email:
            try:
                if User.objects.filter(email__iexact=email).exists():
                    return JsonResponse({'is_taken': True})
                else:
                    return JsonResponse({'is_taken': False})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Yêu cầu không hợp lệ.'}, status=400)
    else:
        return JsonResponse({'error': 'Yêu cầu không hợp lệ hoặc không phải là AJAX.'}, status=400)


def loginPage(request):
    if request.user.is_authenticated:
        return render(request, 'app/home.html', {'name': request.user.username})
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password is incorrect!")

    return redirect('home')

def logoutPage(request):
    logout(request)
    return redirect('home')

"""Home page"""
    
def home(request):
    latest_posts = ForumPost.objects.all().order_by('-created_at')[:5]
    novels = Book.objects.all()
    context = {'latest_posts': latest_posts, 'novels': novels}
    return render(request, 'app/home.html', context) 

"""Search page"""
    
def search(request):
    keywords = request.GET.get('keywords')
    matched_books = []
    all_book = Book.objects.all()
    if all_book:
        for book in all_book:
            if keywords.lower() in book.title.lower():
                matched_books.append(book)
    return render(request, 'app/search.html', {'keywords': keywords,'matched_books': matched_books})

"""Novel works"""

def novelWorks(request, group_id, book_id):
    if int(book_id) == 0:
        book = {
            'id': 0,
            'title': 'Truyện không có tiêu đề',
            'description': '',
            'img_path': None,
            'anothername': '',
            'author': '',
            'artist': '',
            'isCompleted': None,
            'workerid': None,
            'note': None,
            'quantityVol': None,
            'dateUpload': None,
            'dateUpdate': None,
            'category': None,
        }
    else:
        # Lấy thông tin từ model Book
        try:
            book_obj = Book.objects.get(pk=book_id)
            book = {
                'id': book_obj.id,
                'title': book_obj.title,
                'description': book_obj.description,
                'img_path': book_obj.img.url if book_obj.img else '',
                'anothername': book_obj.anothername,
                'author': book_obj.author,
                'artist': book_obj.artist,
                'isCompleted': book_obj.isCompleted,
                'workerid': book_obj.workerid,
                'note': book_obj.note,
                'quantityVol': book_obj.quantityVol,
                'dateUpload': book_obj.dateUpload,
                'dateUpdate': book_obj.dateUpdate,
                'category': book_obj.category,
            }
        except Book.DoesNotExist:
            book = None  # Không tìm thấy đối tượng Book
    categories = Category.objects.all()
    group = Group.objects.get(pk=group_id)
    context = {'categories': categories, 'book': book, 'group': group}

    return render(request, 'app/novelworks.html', context)

@csrf_exempt
def saveBook(request):
    if request.method == 'POST':
        # Nhận dữ liệu từ yêu cầu POST
        id = int(request.POST.get('novelid', -1))  # Chuyển đổi id sang kiểu int
        title = request.POST.get('title')
        author = request.POST.get('author')
        artist = request.POST.get('artist')
        novelTransTeam = request.POST.get('novelTransTeam')
        category = request.POST.get('category')
        description = request.POST.get('description')
        checkboxChecked = request.POST.get('checkboxChecked')
        isCompleted = checkboxChecked.lower() == 'true' if checkboxChecked else False
        image = request.FILES.get('image')

        # Kiểm tra xem id có phải là 0 (tạo mới) hay không
        if id == 0:
            # Tạo mới đối tượng Book
            new_book = Book.objects.create(
                title=title,
                author=author,
                artist=artist,
                workerid=novelTransTeam,
                category=category,
                description=description,
                isCompleted=isCompleted,
                img=image,
                dateUpload=timezone.now(),
                dateUpdate=timezone.now()
            )
            # Trả về phản hồi thành công
            return redirect('novel-of-trans-team', group_id=novelTransTeam)
        else:
            # Cập nhật thông tin của đối tượng Book đã tồn tại
            try:
                existing_book = Book.objects.get(id=id)
                existing_book.title = title
                existing_book.author = author
                existing_book.artist = artist
                existing_book.workerid = novelTransTeam
                existing_book.category = category
                existing_book.description = description
                existing_book.isCompleted = isCompleted
                existing_book.dateUpdate = timezone.now()
                if image:
                    existing_book.img = image
                existing_book.save()
                # Trả về phản hồi thành công
                return redirect('novel-of-trans-team', group_id=novelTransTeam)
            except Book.DoesNotExist:
                return JsonResponse({'error': 'Không tìm thấy đối tượng Book với id đã cho.'}, status=404)

    else:
        return JsonResponse({'error': 'Yêu cầu không hợp lệ.'}, status=405)
    
"""Profile page"""
    
def profile(request, username):
    userInfo, created = UserInfo.objects.get_or_create(username__username=username) 
    return render(request, 'app/profile.html', {'userInfo': userInfo})

def saveBackground(request):
    if request.method == 'POST':
        if request.user.is_authenticated:  # Đảm bảo người dùng đã xác thực
            username = request.user.username
            background_image = request.FILES.get('backgroundImage')
            scroll_position = request.POST.get('scrollPosition')
            
            try:
                user = get_object_or_404(User, username=username)
                user_info, created = UserInfo.objects.get_or_create(username=user)  # Đảm bảo UserInfo liên quan đến User
                print(1)

                # Nếu background_image không phải None, xóa hình ảnh cũ và lưu hình ảnh mới
                if background_image:
                    user_info.img_background.delete()
                    user_info.img_background = background_image
                    user_info.img_background_position = scroll_position
                    user_info.save()
                    
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
        else:
            return JsonResponse({'success': False, 'error': 'Người dùng chưa được xác thực'}, status=401)
    else:
        return JsonResponse({'success': False, 'error': 'Phương thức không được phép'}, status=405)

def saveAvatar(request):
    if request.method == 'POST':
        username = request.user.username
        avatar_image = request.FILES.get('avatarImage')
        
        try:
            user = User.objects.get(username=username)
            userInfo = UserInfo.objects.get(username=user)
            userInfo.img_avatar.delete()
            userInfo.img_avatar = avatar_image
            userInfo.save()
            return JsonResponse({'success': True})
        except UserInfo.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    

"""Translation Group page"""

def forOfTransTeam(group_member_counts, groups, join):
    for group in groups:
        member = Member.objects.filter(group=group, teamrole__in=['owner', 'admin', 'member'])
        group_member_info = {
            'groupname': group.groupname,
            'groupid': group.id,
            'member_count': member.count(),
            'join': join,
            'is_member': (join == 'Đã tham gia'),  # Đã tham gia: True, Chưa tham gia: False
            'is_waiter': (join == 'Chờ duyệt'),
        }
        group_member_counts.append(group_member_info)

def transTeam(request):
    user = request.user
    member_groups = Member.objects.filter(auth_user=user, teamrole__in=['admin', 'owner', 'member']).values_list('group', flat=True)
    waiter_groups = Member.objects.filter(auth_user=user, teamrole='waiter').values_list('group', flat=True)
    groups = Group.objects.filter(id__in=member_groups)
    groups_waiter = Group.objects.filter(id__in=waiter_groups)
    other_groups = Group.objects.exclude(id__in=member_groups).exclude(id__in=waiter_groups)
    
    group_member_counts = []
    forOfTransTeam(group_member_counts, groups, 'Đã tham gia')
    forOfTransTeam(group_member_counts, groups_waiter, 'Chờ duyệt')
    forOfTransTeam(group_member_counts, other_groups, 'Chưa tham gia')
    
    context = {
        'group_member_counts': group_member_counts,
    }
    return render(request, 'app/transteam.html', context)


def novelOfTransTeam(request, group_id):
    group = Group.objects.get(pk=group_id)
    books = Book.objects.filter(workerid=group_id)
    context = {'books': books, 'group': group}
    return render(request, 'app/novel-of-trans.html', context)
    
def memberOfTransTeam(request, group_id):
    group = Group.objects.get(pk=group_id)
    members = Member.objects.filter(group=group, teamrole__in = ['owner', 'admin', 'member'])
    waiters = Member.objects.filter(group=group, teamrole='waiter')
    
    # Kiểm tra xem người dùng hiện tại có phải là thành viên của nhóm không
    is_member = Member.objects.filter(auth_user=request.user, group=group).exists()
    is_owner = Member.objects.filter(auth_user=request.user, group=group, teamrole='owner').exists()
    is_admin = Member.objects.filter(auth_user=request.user, group=group, teamrole='admin').exists()
    context = {'Members' : members, 'Group':group, 'Waiters': waiters, 
               'is_member': is_member,'is_admin': is_admin, 'is_owner': is_owner}
    
    return render(request, 'app/member-of-trans.html', context)

def addGroup(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Group created successfully")
    context = {'form': form}
    return render(request, 'transteam.html', context)

def deleteGroup(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    group.delete()
    messages.success(request, "Group deleted successfully")
    return redirect('home')

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
    # Đổi vai trò thành admin
    group = get_object_or_404(Group, pk=group_id)
    member = get_object_or_404(Member, pk=member_id)
    
    if Member.objects.filter(auth_user=member.auth_user, group=group, teamrole='member').exists():
        if Member.objects.filter(auth_user=request.user, group=group, teamrole__in=['admin', 'owner']).exists():
            member.teamrole = "admin"
            member.save()
            messages.success(request, "Change member's role successfully")
  
    return redirect('member-of-trans-team', group_id=group_id)

def deleteRoleOfAdmin(request, group_id, member_id):
    # Xoá vai trò thành admin của thành viên
    group = get_object_or_404(Group, pk=group_id)
    member = get_object_or_404(Member, pk=member_id)
    
    if Member.objects.filter(auth_user=member.auth_user, group=group, teamrole='admin').exists():
        if Member.objects.filter(auth_user=request.user, group=group, teamrole='owner').exists():
            member.teamrole = "member"
            member.save()
            messages.success(request, "Change member's role successfully")
  
    return redirect('member-of-trans-team', group_id=group_id)

def changeRoleToOwner(request, group_id, member_id):
    # Nhượng quyền sở hữu cho thành viên khác
    group = get_object_or_404(Group, pk=group_id)
    member = get_object_or_404(Member, pk=member_id)
    owner = Member.objects.filter(group=group, teamrole='owner').first()
    
    if owner.id != member_id:
        if Member.objects.filter(auth_user=request.user, group=group, teamrole='owner').exists():
            member.teamrole = "owner"
            member.save()
            
            auth_member = Member.objects.filter(auth_user=request.user, group=group).first()
            auth_member.teamrole = 'member'
            auth_member.save()
            messages.success(request, "Change member's role successfully")
            
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
            if member.teamrole == "owner":
                messages.error(request, "You can't delete the owner")
            else:
                member.delete()
                messages.success(request, "Delete member successfully")
        elif Member.objects.filter(auth_user=request.user, group=group, teamrole='admin').exists():
            if member.teamrole in ["owner", "admin"]:
                messages.error(request, "Can't delete the admin/owner member")
            else:
                member.delete()
                messages.success(request, "Delete member successfully")
        else:
            messages.error(request, "You must have admin/owner role in the group to delete this member")
    else:
        messages.error(request, "You must be a member of the group to delete this member")
    
    return redirect('member-of-trans-team', group_id=group_id)

def outGroup(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    member = get_object_or_404(Member, auth_user=request.user, group=group)
    
    if request.method == "POST":
        if member.teamrole != 'owner':
            member.delete()
            messages.success(request, "Left group successfully")
        else:
            messages.error(request, "Owner can't leave the group.")
        return redirect('member-of-trans-team', group_id=group_id)
    
    return redirect('member-of-trans-team', group_id=group_id)
