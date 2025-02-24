# Aiko Novel

Aiko Novel là một dự án web sử dụng Django để quản lý và đọc tiểu thuyết.

## Yêu cầu hệ thống

- Python 3.x
- Virtual Environment (optional)

## Cài đặt

### 1. Tạo và kích hoạt môi trường ảo (tùy chọn)
```bash
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux
venv\Scripts\activate  # Trên Windows
```

### 2. Cài đặt các gói phụ thuộc
```bash
pip install -r requirements.txt
```

## Chạy chương trình

### 1. Chạy migration
```bash
python manage.py migrate
```

### 2. Khởi chạy server
```bash
python manage.py runserver
```
Mặc định, server sẽ chạy tại địa chỉ `http://127.0.0.1:8000/`. Bạn có thể thay đổi địa chỉ và cổng bằng cách thêm thông số:
```bash
python manage.py runserver 0.0.0.0:8080
```

## Công nghệ sử dụng
- Django 5.0.1
- Django CKEditor
- Pillow
- asgiref
- sqlparse
- tzdata
- django-js-asset


