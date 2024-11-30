import sqlite3
from datetime import datetime
import bcrypt

# 连接到数据库
conn = sqlite3.connect('db.sqlite')  # 这里指定的是数据库文件名
cursor = conn.cursor()

# 生成哈希值函数
def hash_password(plain_password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# 样例用户数据
sample_users = [
    (1, 'user4@example.com', 'User4', "securePass456", datetime.now().strftime('%Y-%m-%d'), None, '/static/images/user4.jpeg', 'Fan of technology and gaming.', 'Viewer'),
    (2, 'user5@example.com', 'User5', "mySecret789", datetime.now().strftime('%Y-%m-%d'), None, '/static/images/user5.jpeg', 'Passionate about art and design.', 'Uploader'),
    (3, 'user6@example.com', 'User6', "fitness2023", datetime.now().strftime('%Y-%m-%d'), None, '/static/images/user6.jpeg', 'Loves cooking and fitness activities.', 'Viewer'),
    (4, 'user8@example.com', 'User8', "musicLover01", datetime.now().strftime('%Y-%m-%d'), None, '/static/images/user8.jpeg', 'Aspiring musician and coffee enthusiast.', 'Admin'),
]

# 插入到 Users 表
for user in sample_users:
    try:
        cursor.execute('''
        INSERT INTO Users (User_ID, Email, UserName, Password, Create_Time, Last_Login, Picture, Bio, Role)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', user)
    except sqlite3.IntegrityError as e:
        print(f"插入用户 {user[1]} 时出错：{e}")

# 提交更改
conn.commit()

print("新数据已插入成功！")

# 关闭连接
conn.close()