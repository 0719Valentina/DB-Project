import sqlite3

# 连接到数据库
conn = sqlite3.connect('db.sqlite')  # 指定数据库文件名
cursor = conn.cursor()

# 创建 Users 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Email TEXT UNIQUE NOT NULL,
    UserName TEXT NOT NULL,
    Password TEXT NOT NULL,
    Create_Time TEXT NOT NULL,
    Last_Login TEXT,
    Picture TEXT,
    Bio TEXT,
    Role TEXT NOT NULL CHECK (Role IN ('Admin', 'Uploader', 'Viewer')) DEFAULT 'Viewer'
)
''')

# 创建 Videos 表，增加 category_id 外键字段
cursor.execute('''
CREATE TABLE IF NOT EXISTS Videos (
    Video_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    User_ID INTEGER NOT NULL,
    Upload_Time TEXT NOT NULL,
    Title TEXT NOT NULL,
    Description TEXT,
    Views INTEGER DEFAULT 0,
    Likes INTEGER DEFAULT 0,
    Video_URL TEXT NOT NULL,
    Picture_URL TEXT,
    Category_ID INTEGER NOT NULL,  -- 新增字段
    FOREIGN KEY (User_ID) REFERENCES Users (User_ID),
    FOREIGN KEY (Category_ID) REFERENCES Video_Category (Category_ID)  -- 外键约束
)
''')

# 创建 History 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS History (
    History_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    User_ID INTEGER NOT NULL,
    Video_ID INTEGER NOT NULL,
    UserName TEXT NOT NULL,
    Watch_Time TEXT NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES Users (User_ID),
    FOREIGN KEY (Video_ID) REFERENCES Videos (Video_ID)
)
''')

# 创建 Liked_Video 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS Liked_Video (
    Video_ID INTEGER NOT NULL PRIMARY KEY,
    User_ID INTEGER NOT NULL,
    Liked_Time TEXT NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES Users (User_ID),
    FOREIGN KEY (Video_ID) REFERENCES Videos (Video_ID)
)
''')

# 创建 Subscription 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS Subscription (
    Subscription_ID INTEGER NOT NULL,
    Subscriber_User_ID INTEGER NOT NULL,
    Subscribed_User_ID INTEGER NOT NULL,
    Subscription_Time TEXT NOT NULL,
    PRIMARY KEY (Subscription_ID, Subscriber_User_ID),
    FOREIGN KEY (Subscriber_User_ID) REFERENCES Users (User_ID),
    FOREIGN KEY (Subscribed_User_ID) REFERENCES Users (User_ID)
)
''')

# 创建 Video_Category 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS Video_Category (
    Category_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Category_Name TEXT NOT NULL
)
''')

# 创建 Comment 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS Comment (
    Comment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Video_ID INTEGER NOT NULL,
    User_ID INTEGER NOT NULL,
    Content TEXT NOT NULL,
    Created_Time TEXT NOT NULL,
    FOREIGN KEY (Video_ID) REFERENCES Videos (Video_ID),
    FOREIGN KEY (User_ID) REFERENCES Users (User_ID)
)
''')



# 提交更改并关闭连接
conn.commit()
conn.close()

print("所有表创建成功！")
