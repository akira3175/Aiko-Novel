import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect('db.sqlite3')

# Tạo một đối tượng cursor để thực hiện các truy vấn SQL
cursor = conn.cursor()

# Thực hiện truy vấn SELECT
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Lấy kết quả của truy vấn
rows = cursor.fetchall()

# In ra các hàng trong kết quả
for row in rows:
    print(row)

# Đóng kết nối
conn.close()
