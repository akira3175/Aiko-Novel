import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect('db.sqlite3')

# Tạo một đối tượng cursor để thực hiện các truy vấn SQL
cursor = conn.cursor()

try:
    # Thực hiện lệnh DROP TABLE
    cursor.execute("DROP TABLE IF EXISTS forum_comment")
    print("Bảng app_chapter đã được xóa thành công.")
except sqlite3.Error as e:
    print(f"Lỗi xảy ra khi xóa bảng app_chapter: {e}")

# Đóng kết nối
conn.close()
