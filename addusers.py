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
    ('user4@example.com', 'User4', hash_password("securePass456"), datetime.now().isoformat(), None, 'user4.jpg', 'Fan of technology and gaming.'),
    ('user5@example.com', 'User5', hash_password("mySecret789"), datetime.now().isoformat(), None, 'user5.jpg', 'Passionate about art and design.'),
    ('user6@example.com', 'User6', hash_password("fitness2023"), datetime.now().isoformat(), None, 'user6.jpg', 'Loves cooking and fitness activities.'),
    ('user8@example.com', 'User8', hash_password("musicLover01"), datetime.now().isoformat(), None, 'user8.jpg', 'Aspiring musician and coffee enthusiast.'),
]
# 插入到 Users 表
for User in sample_users:
    cursor.execute('''
    INSERT INTO Users (Email, UserName, Password_Hash, Create_Time, Last_Login, Picture, Bio)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', User)

# 提交更改
conn.commit()

print("新数据已插入成功！")

# 关闭连接
conn.close()
