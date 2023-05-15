import sqlite3
# Tạo kết nối đến cơ sở dữ liệu
conn = sqlite3.connect('db.db')
# Tạo bảng Follows
conn.execute("INSERT INTO User VALUES(1,'Binh','123456','Quang Tri','09123314')")
