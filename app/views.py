from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from app.models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User, AnonymousUser
from django.contrib import messages
from forum.models import ForumPost
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Sum, Max
from django import forms

# Create your views here.

"""Login and Register"""
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        current_url = request.POST.get('current-url')

        if password == repassword:
            # Tạo một người dùng mới
            myuser = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
            )

            # Tạo một đối tượng UserInfo và liên kết với người dùng mới
            UserInfo.objects.create(username=myuser, full_name=myuser.username)

            messages.success(request, "Your account has been registered")
            return redirect(current_url)
        else:
            messages.error(request, "Passwords do not match")
        current_url = request.POST.get('current-url')

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
        current_url = request.POST.get('current-url')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(current_url)
        else:
            messages.error(request, "Username or password is incorrect!")
        return redirect(current_url)

    return JsonResponse({'success': False, 'error_message': 'Invalid request method'}, status=400)

def logoutPage(request):
    logout(request)
    return redirect('home')

"""Home page"""
    
def home(request):
    latest_posts = ForumPost.objects.all().order_by('-created_at')[:5]
    novels = Book.objects.filter(isDeleted=False)
    trending_novels = Book.objects.annotate(total_views=Sum('volumes__chapters__view')).order_by('-total_views')[:8]
    latest_chapters = Chapter.objects.values('volume_id').annotate(
        latest_chapter_date=Max('date_upload')
    ).order_by('-latest_chapter_date')
    
    new_update_novels = []
    book_ids_added = set()  # Set để lưu trữ các book_id đã thêm vào danh sách
    for chapter_info in latest_chapters:
        if len(new_update_novels) >= 14:
            break 

        latest_chapter = Chapter.objects.filter(
            volume_id=chapter_info['volume_id'],
            date_upload=chapter_info['latest_chapter_date']
        ).first()

        if latest_chapter and latest_chapter.volume.book_id not in book_ids_added:
            volume = latest_chapter.volume
            book = volume.book
            new_update_novels.append({'book': book, 'volume': volume, 'chapter': latest_chapter})
            book_ids_added.add(latest_chapter.volume.book_id) 


    context = {
            'latest_posts': latest_posts,
            'novels': novels,
            'trending_novels': trending_novels,
            'new_update_novels': new_update_novels,
        }
    return render(request, 'app/home.html', context)

"""Search page"""
    
def search(request):
    keywords = request.GET.get('keywords')
    matched_books = []
    all_book = Book.objects.filter(isDeleted=False)
    if all_book:
        for book in all_book:
            if keywords.lower() in book.title.lower():
                matched_books.append(book)
    return render(request, 'app/search.html', {'keywords': keywords,'matched_books': matched_books})

"""Novel page"""

def novel(request,id):
    book = Book.objects.get(id=id, isDeleted=False)
    volumes = Volume.objects.filter(book=book).order_by('-id')
    chapters = Chapter.objects.filter(volume__in=volumes, date_upload__isnull=False)
    group = Group.objects.get(id=book.workerid)
    if isinstance(request.user, AnonymousUser):
        is_follow = False  # Đối với người dùng không xác định, không có trạng thái follow
        number_followers = BookFollowing.objects.filter(book=book).count()
    else:
        is_follow = BookFollowing.objects.filter(user=request.user, book=book).exists()
        number_followers = BookFollowing.objects.filter(book=book).count()
    follow_status = 'follow' if not is_follow else 'unfollow'
    number_followers = BookFollowing.objects.filter(book=book).count()
    context = {'book': book, 'volumes': volumes, 'chapters': chapters, 'follow_status': follow_status, 'number_followers': number_followers, 'group': group}

    # Tính tổng số bình luận của tất cả các chương
    total_comments = 0
    for chapter in chapters:
        total_comments += ChapterComment.objects.filter(chapter=chapter).count()

    context['total_comments'] = total_comments
    
    return render(request, 'app/novel.html', context)

def read(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id, date_upload__isnull=False)
    volume = Volume.objects.get(id=chapter.volume.id)
    book = Book.objects.get(id=volume.book.id, isDeleted=False)
    chapter.increase_views()

    previous_chapter_same_volume = Chapter.objects.filter(volume__book=book, volume__id=volume.id, id__lt=chapter.id, date_upload__isnull=False).order_by('-id').first()
    previous_chapter_prev_volume = None
    prev_volume = Volume.objects.filter(book=book, id__lt=volume.id).order_by('-id').first()
    if prev_volume:
        previous_chapter_prev_volume = Chapter.objects.filter(volume=prev_volume, date_upload__isnull=False).order_by('-id').first()

    next_chapter_same_volume = Chapter.objects.filter(volume__book=book, volume__id=volume.id, id__gt=chapter.id, date_upload__isnull=False).order_by('id').first()
    next_chapter_next_volume = None
    next_volume = Volume.objects.filter(book=book, id__gt=volume.id).order_by('id').first()
    if next_volume:
        next_chapter_next_volume = Chapter.objects.filter(volume=next_volume, date_upload__isnull=False).order_by('id').first()
        
    context = {
        'chapter': chapter,
        'volume': volume,
        'book': book,
        'previous_chapter': previous_chapter_same_volume or previous_chapter_prev_volume or None,
        'next_chapter': next_chapter_same_volume or next_chapter_next_volume or None,
    }
    
    if request.method == 'POST':
        form = ChapterCommentForm(request.POST)
        if form.is_valid():
            chapter_comment = form.save(commit=False)
            chapter_comment.chapter = chapter
            chapter_comment.user_info = UserInfo.objects.get(username=request.user)
            chapter_comment.save()
            return redirect('read', chapter_id=chapter_id)
    else:
        form = ChapterCommentForm()

    context['chapter_comment_form'] = form
    context['chapter_comments'] = ChapterComment.objects.filter(chapter=chapter, is_deleted=False).order_by('-created_at')
    
    return render(request, 'app/read.html', context)

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
            'categories': None,
        }
        categories = Category.objects.all()
        volumes = None
        chapters = None
    else:
        # Lấy thông tin từ model Book
        try:
            book_obj = Book.objects.get(id=book_id, isDeleted=False)
            categories = Category.objects.exclude(id__in=book_obj.categories.all())
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
                'categories': [(category.id, category.name) for category in book_obj.categories.all()],
            }
            volumes = Volume.objects.filter(book=book_obj)
            chapters = Chapter.objects.filter(volume__in=volumes)
        except Book.DoesNotExist:
            book = None  # Không tìm thấy đối tượng Book
    group = Group.objects.get(pk=group_id)
    context = {'categories': categories, 'book': book, 'group': group, 'volumes': volumes, 'chapters': chapters}
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
        category_ids_str = request.POST.get('category')
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
                description=description,
                isCompleted=isCompleted,
                img=image,
                dateUpload=timezone.now(),
                dateUpdate=timezone.now()
            )
            # Thêm categories cho đối tượng mới
            if category_ids_str:
                category_ids = [int(cat_id) for cat_id in category_ids_str.split(',')]
                categories = Category.objects.filter(id__in=category_ids)
                new_book.categories.add(*categories)

            # Trả về phản hồi thành công
            return redirect('novel-of-trans-team', group_id=novelTransTeam)
        else:
            # Cập nhật thông tin của đối tượng Book đã tồn tại
            existing_book = get_object_or_404(Book, id=id)
            existing_book.title = title
            existing_book.author = author
            existing_book.artist = artist
            existing_book.workerid = novelTransTeam
            existing_book.description = description
            existing_book.isCompleted = isCompleted
            existing_book.dateUpdate = timezone.now()
            if image:
                existing_book.img = image

            # Xóa hết categories cũ và thêm lại categories mới
            existing_book.categories.clear()
            if category_ids_str:
                category_ids = [int(cat_id) for cat_id in category_ids_str.split(',')]
                categories = Category.objects.filter(id__in=category_ids)
                existing_book.categories.add(*categories)

            existing_book.save()
            # Trả về phản hồi thành công
            return redirect('novel-of-trans-team', group_id=novelTransTeam)
    else:
        return JsonResponse({'error': 'Yêu cầu không hợp lệ.'}, status=405)
    
@csrf_exempt
def saveBookSub(request):
    if request.method == 'POST':
        # Nhận dữ liệu từ yêu cầu POST
        id = int(request.POST.get('novelid', -1))  # Chuyển đổi id sang kiểu int
        title = request.POST.get('title')
        author = request.POST.get('author')
        artist = request.POST.get('artist')
        novelTransTeam = request.POST.get('novelTransTeam')
        category_ids_str = request.POST.get('category')
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
                description=description,
                isCompleted=isCompleted,
                img=image,
                dateUpload=timezone.now(),
                dateUpdate=timezone.now()
            )
            # Thêm categories cho đối tượng mới
            if category_ids_str:
                category_ids = [int(cat_id) for cat_id in category_ids_str.split(',')]
                categories = Category.objects.filter(id__in=category_ids)
                new_book.categories.add(*categories)

            # Trả về phản hồi thành công
            return JsonResponse({'book_id': new_book.id})
        else:
            # Cập nhật thông tin của đối tượng Book đã tồn tại
            existing_book = get_object_or_404(Book, id=id)
            existing_book.title = title
            existing_book.author = author
            existing_book.artist = artist
            existing_book.workerid = novelTransTeam
            existing_book.description = description
            existing_book.isCompleted = isCompleted
            existing_book.dateUpdate = timezone.now()
            if image:
                existing_book.img = image

            # Xóa hết categories cũ và thêm lại categories mới
            existing_book.categories.clear()
            if category_ids_str:
                category_ids = [int(cat_id) for cat_id in category_ids_str.split(',')]
                categories = Category.objects.filter(id__in=category_ids)
                existing_book.categories.add(*categories)

            existing_book.save()
            # Trả về phản hồi thành công
            return JsonResponse({'book_id': existing_book.id})
    else:
        return JsonResponse({'error': 'Yêu cầu không hợp lệ.'}, status=405)
    
def deleteBook(request, book_id):
    book = Book.objects.get(id=book_id)
    book.isDeleted = True
    book.save()
    return redirect('novel-of-trans-team', group_id=book.workerid)
    
@csrf_exempt
def saveVolume(request):
    if request.method == 'POST':
        book_id = int(request.POST.get('book-id'))
        volume_id = int(request.POST.get('volume-id'))
        volume_image = request.FILES.get('volume-image')
        volume_title = request.POST.get('volume-title')
        
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Sách không tồn tại'}, status=404)

        if volume_id == 0:  # Nếu volume_id là '0', tạo tập mới
            volume = Volume.objects.create(book=book, title=volume_title)
            if volume_image:
                volume.img = volume_image
                volume.save()
            redirect_url = f'/novel-works/{book.workerid}/{book.id}'  # Tạo chuỗi URL trực tiếp
            return JsonResponse({'redirect_url': redirect_url})

        else:  # Ngược lại, sửa tập đã tồn tại
            try:
                volume = Volume.objects.get(id=volume_id)
                volume.title = volume_title
                if volume_image:
                    volume.img = volume_image
                volume.save()
                redirect_url = f'/novel-works/{book.workerid}/{book.id}'  # Tạo chuỗi URL trực tiếp
                return JsonResponse({'redirect_url': redirect_url})

            except Volume.DoesNotExist:
                return JsonResponse({'error': 'Tập không tồn tại'}, status=404)

    return JsonResponse({'error': 'Phương thức yêu cầu không hợp lệ'}, status=400)
    
def deleteVolume(request, volume_id):
    volume = Volume.objects.get(id=volume_id)
    book = volume.book
    volume.delete()
    return redirect('novel-works', group_id=book.workerid, book_id=book.id)

"""Write page"""
    
def write(request, volume_id, chapter_id):
    volume = Volume.objects.get(id=volume_id)
    book = Book.objects.get(id=volume.book.id, isDeleted=False)
    if chapter_id == 0:
        chapter = Chapter.objects.create(volume=volume)
    else: 
        chapter = Chapter.objects.get(id=chapter_id)
    context = {'chapter': chapter, 'volume': volume, 'book': book}
    return render(request, 'app/write.html', context)

def saveChapter(request):
    if request.method == 'POST':
        chapterId = request.POST.get('chapter-id')
        novelId = request.POST.get('novel-id')
        content = request.POST.get('content')
        title = request.POST.get('title')
        

        try:
            book = Book.objects.get(id=novelId)
            chapter = Chapter.objects.get(id=chapterId)
            chapter.title = title
            chapter.content = content
            chapter.save()
            redirect_url = f'/novel-works/{book.workerid}/{book.id}'  # Tạo chuỗi URL trực tiếp
            return JsonResponse({'redirect_url': redirect_url})
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)
        except Chapter.DoesNotExist:
            return JsonResponse({'error': 'Chapter not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def uploadChapter(request):
    if request.method == 'POST':
        chapterId = request.POST.get('chapter-id')
        novelId = request.POST.get('novel-id')
        content = request.POST.get('content')
        title = request.POST.get('title')
        

        try:
            book = Book.objects.get(id=novelId)
            chapter = Chapter.objects.get(id=chapterId)
            chapter.title = title
            chapter.content = content
            chapter.date_upload = timezone.now()
            chapter.save()
            book.dateUpdate = timezone.now()
            book.save()
            # Redirect đến trang novelWorks với các tham số group_id và book_id
            redirect_url = f'/novel-works/{book.workerid}/{book.id}'  # Tạo chuỗi URL trực tiếp
            return JsonResponse({'redirect_url': redirect_url})
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)
        except Chapter.DoesNotExist:
            return JsonResponse({'error': 'Chapter not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def deleteChapter(request):
    if request.method == 'POST':
        chapterId = request.POST.get('chapter-id')
        novelId = request.POST.get('novel-id')
        
        try:
            book = Book.objects.get(id=novelId)
            chapter = Chapter.objects.get(id=chapterId)
            chapter.delete()
            redirect_url = f'/novel-works/{book.workerid}/{book.id}'  
            return JsonResponse({'redirect_url': redirect_url})
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)
        except Chapter.DoesNotExist:
            return JsonResponse({'error': 'Chapter not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

"""Profile page"""
    
def profile(request, username):
    userInfo, created = UserInfo.objects.get_or_create(username__username=username)
    groups = Group.objects.filter(members__auth_user=userInfo.username)
    context = {'groups': groups, 'userInfo': userInfo}
    return render(request, 'app/profile.html', context)

def saveBackground(request):
    if request.method == 'POST':
        if request.user.is_authenticated:  # Đảm bảo người dùng đã xác thực
            username = request.user.username
            background_image = request.FILES.get('backgroundImage')
            scroll_position = request.POST.get('scrollPosition')
            
            try:
                user = get_object_or_404(User, username=username)
                user_info, created = UserInfo.objects.get_or_create(username=user)  # Đảm bảo UserInfo liên quan đến User

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
    
def saveFullName(request):
    if request.method == 'POST':
        newFullName = request.POST.get('fullname')
        userInfo = UserInfo.objects.get(username=request.user)
        userInfo.full_name = newFullName
        userInfo.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

"""Translation Group page"""

def group(request, group_id):
    group = Group.objects.get(id=group_id)
    novels = Book.objects.filter(isDeleted=False, workerid=group_id).order_by('-dateUpdate')
    is_owner = Member.objects.filter(auth_user=request.user, group=group, teamrole='Trưởng nhóm').exists()
    
    context = {'novels': novels, 'group': group, 'is_owner': is_owner}
    return render(request, 'app/group.html', context)

def forOfTransTeam(group_member_counts, groups, join):
    for group in groups:
        member = Member.objects.filter(group=group, teamrole__in=['Trưởng nhóm', 'Admin', 'Thành viên'])
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
    member_groups = Member.objects.filter(auth_user=user, teamrole__in=['Admin', 'Trưởng nhóm', 'Thành viên']).values_list('group', flat=True)
    waiter_groups = Member.objects.filter(auth_user=user, teamrole='Chờ duyệt').values_list('group', flat=True)
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
    books = Book.objects.filter(workerid=group_id, isDeleted=False).order_by('-dateUpdate')
    books_with_volumes_count = []
    
    for book in books:
        volume_count = book.volumes.count()
        books_with_volumes_count.append({'book': book, 'volume_count': volume_count})
    context = {'group': group, 'books_with_volumes_count': books_with_volumes_count}
    return render(request, 'app/novel-of-trans.html', context)
    
def memberOfTransTeam(request, group_id):
    group = Group.objects.get(pk=group_id)
    members = Member.objects.filter(group=group, teamrole__in=['Trưởng nhóm', 'Admin', 'Thành viên'])
    waiters = Member.objects.filter(group=group, teamrole='Chờ duyệt')

    for member in members:
        try:
            info_user = UserInfo.objects.get(username=member.auth_user)
            member.full_name = info_user.full_name
            member.img_avatar = info_user.img_avatar if info_user.img_avatar else None
        except UserInfo.DoesNotExist:
            member.full_name = None
            member.img_avatar = None
    
    for waiter in waiters:
        try:
            info_user = UserInfo.objects.get(username=waiter.auth_user)
            waiter.full_name = info_user.full_name
            waiter.img_avatar = info_user.img_avatar if info_user.img_avatar else None
        except UserInfo.DoesNotExist:
            waiter.full_name = None
            waiter.img_avatar = None
    
    is_member = Member.objects.filter(auth_user=request.user, group=group).exists()
    is_owner = Member.objects.filter(auth_user=request.user, group=group, teamrole='Trưởng nhóm').exists()
    is_admin = Member.objects.filter(auth_user=request.user, group=group, teamrole='Admin').exists()

    context = {
        'Members': members,
        'Waiters': waiters,
        'Group': group,
        'is_member': is_member,
        'is_admin': is_admin,
        'is_owner': is_owner,
    }

    return render(request, 'app/member-of-trans.html', context)   

def changeDescription(request, group_id):
    if request.method == 'POST':
        group = get_object_or_404(Group, pk=group_id)
        description = request.POST.get('description')
        if description:
            group.description = description
            group.save()
            messages.success(request, "Changed description successfully")
        else:
            messages.error(request, "Error: Description cannot be empty.")
    else:
        messages.error(request, "Error: Invalid request method for changing description.")
    
    return redirect('group', group_id=group_id)


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
                member = Member(auth_user_id=current_user.id, group_id=group.id, teamrole='Trưởng nhóm')
                member.save()
                messages.success(request, "Group created successfully")
        else:   
            messages.error(request, "Error add group. Please check the addGroup.")
    return redirect('transteam')

    
def wantToJoin(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if Member.objects.filter(auth_user=request.user, group=group, teamrole='Chờ duyệt').exists():
        messages.success(request, 'Please waiting for the admin acceptance')
    elif Member.objects.exclude(auth_user=request.user, group=group).exists():
        member = Member(auth_user_id=request.user.id, group_id=group.id, teamrole='Chờ duyệt')
        member.save()
        messages.success(request, 'Join successfully')
    return redirect('transteam')

def approveMember(request, group_id, member_id):
    group = get_object_or_404(Group, pk=group_id)
    member = get_object_or_404(Member, pk=member_id)
    
    if Member.objects.filter(auth_user=request.user, group=group, teamrole__in=['Admin', 'Trưởng nhóm', 'Thành viên']).exists():
        if request.method == 'POST':
            member.teamrole = "Thành viên"
            member.save()
            messages.success(request, "Approve successfully")
    else:
        messages.error(request, "You must have admin/owner/member role in the group to approve members")
    return redirect('member-of-trans-team', group_id=group_id)

def changeRoleToAdmin(request, group_id, member_id):
    # Đổi vai trò thành admin
    group = get_object_or_404(Group, pk=group_id)
    member = get_object_or_404(Member, pk=member_id)
    
    if Member.objects.filter(auth_user=member.auth_user, group=group, teamrole='Thành viên').exists():
        if Member.objects.filter(auth_user=request.user, group=group, teamrole__in=['Admin', 'Trưởng nhóm']).exists():
            member.teamrole = "Admin"
            member.save()
            messages.success(request, "Change member's role successfully")
  
    return redirect('member-of-trans-team', group_id=group_id)

def deleteRoleOfAdmin(request, group_id, member_id):
    # Xoá vai trò thành admin của thành viên
    group = get_object_or_404(Group, pk=group_id)
    member = get_object_or_404(Member, pk=member_id)
    
    if Member.objects.filter(auth_user=member.auth_user, group=group, teamrole='Admin').exists():
        if Member.objects.filter(auth_user=request.user, group=group, teamrole='Trưởng nhóm').exists():
            member.teamrole = "Thành viên"
            member.save()
            messages.success(request, "Change member's role successfully")
  
    return redirect('member-of-trans-team', group_id=group_id)

def changeRoleToOwner(request, group_id, member_id):
    # Nhượng quyền sở hữu cho thành viên khác
    group = get_object_or_404(Group, pk=group_id)
    member = get_object_or_404(Member, pk=member_id)
    owner = Member.objects.filter(group=group, teamrole='Trưởng nhóm').first()
    
    if owner.id != member_id:
        if Member.objects.filter(auth_user=request.user, group=group, teamrole='Trưởng nhóm').exists():
            member.teamrole = "Trưởng nhóm"
            member.save()
            
            auth_member = Member.objects.filter(auth_user=request.user, group=group).first()
            auth_member.teamrole = 'Thành viên'
            auth_member.save()
            messages.success(request, "Change member's role successfully")
            
    return redirect('member-of-trans-team', group_id=group_id)


    
def deleteGroup(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    # Kiểm tra xem người dùng hiện tại có trong nhóm và có vai trò owner trong nhóm đó không
    if Member.objects.filter(auth_user=request.user, group=group, teamrole='Trưởng nhóm').exists():
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
        # Kiểm tra xem người dùng hiện tại có vai trò "Trưởng nhóm" trong nhóm đó không
        if Member.objects.filter(auth_user=request.user, group=group, teamrole='Trưởng nhóm').exists():
            if member.teamrole == "Trưởng nhóm":
                messages.error(request, "You can't delete the owner")
            else:
                member.delete()
                messages.success(request, "Delete member successfully")
        elif Member.objects.filter(auth_user=request.user, group=group, teamrole='Admin').exists():
            if member.teamrole in ["Trưởng nhóm", "Admin"]:
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
        if member.teamrole != 'Trưởng nhóm':
            member.delete()
            messages.success(request, "Left group successfully")
        else:
            messages.error(request, "Owner can't leave the group.")
        return redirect('member-of-trans-team', group_id=group_id)
    
    return redirect('member-of-trans-team', group_id=group_id)

"""Libraby"""
def library(request):
    book_following = Book.objects.filter(bookfollowing__user=request.user)
    book_following_list = []
    for book in book_following:
        lastest_chapter = Chapter.objects.filter(volume__book=book, date_upload__isnull=False).order_by('-date_upload').first()
        if lastest_chapter:
            lastest_volume = lastest_chapter.volume
        else:
            lastest_volume = None
        
        book_following_list.append({
            'book': book,
            'lastest_volume': lastest_volume,
            'lastest_chapter': lastest_chapter,
        })
    book_following_list.sort(key=lambda x: x['book'].dateUpdate, reverse=True)
    context = {
        'book_following_list': book_following_list,
    }
    return render(request, 'app/library.html', context)

@require_POST
def followBook(request, book_id):
    action = request.POST.get('action') 
    user = request.user 

    if action == 'follow':
        BookFollowing.objects.get_or_create(user=user, book_id=book_id)
        message = 'Sách đã được theo dõi.'
    elif action == 'unfollow':
        BookFollowing.objects.filter(user=user, book_id=book_id).delete()
        message = 'Sách đã bị bỏ theo dõi.'
    else:
        message = 'Hành động không hợp lệ.'

    return JsonResponse({'success': True, 'message': message})
                                   

"""Ckeditor"""
def ckeditor_admin(request):
    return render(request, 'admin/ckeditor.html')