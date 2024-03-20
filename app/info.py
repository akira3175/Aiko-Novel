#lấy tên người dùng mỗi khi request
def username(request):
    name = None
    if request.user.is_authenticated:
        name = request.user.username
    return {'name': name}