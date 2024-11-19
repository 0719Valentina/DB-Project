import sqlite3

# 连接到数据库
conn = sqlite3.connect('db.sqlite')  # 这里指定的是数据库文件名
cursor = conn.cursor()

# 创建 Users 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Email TEXT UNIQUE NOT NULL,
    UserName TEXT NOT NULL,
    Password_Hash TEXT NOT NULL,
    Create_Time TEXT NOT NULL,
    Last_Login TEXT,
    Picture TEXT,
    Bio TEXT
)
''')

# 创建 Videos 表
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
    FOREIGN KEY (User_ID) REFERENCES Users (User_ID)
)
''')

# 创建 History 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS History (
    History_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    User_ID INTEGER NOT NULL,
    Video_ID INTEGER NOT NULL,
    Watch_Time TEXT NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES Users (User_ID),
    FOREIGN KEY (Video_ID) REFERENCES Videos (Video_ID)
)
''')

# 创建 Liked_Video 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS Liked_Video (
    User_ID INTEGER NOT NULL,
    Video_ID INTEGER NOT NULL,
    Liked_Time TEXT NOT NULL,
    PRIMARY KEY (User_ID, Video_ID),
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

# 插入初始数据到 Users 表
cursor.execute('''
INSERT INTO Users (Email, UserName, Password_Hash, Create_Time, Picture, Bio)
VALUES (?, ?, ?, ?, ?, ?)
''', ("user1@example.com", "user1", "hashed_password_123", "2024-11-01", "/static/images/user1.png", "Hello, I love videos!"))

# 插入初始数据到 Videos 表

#cursor.execute('''
#INSERT INTO Videos (Video_ID, User_ID, Upload_Time, Title, Description, Video_URL, Picture_URL)
#VALUES (?, ?, ?, ?, ?, ?)
#''', (2, 1, "2024-11-06", "How to Install Visual Studio", 
#      "A tutorial on installing Visual Studio Code on Windows 11.", 
#      "/static/videos/How Install Visual Studio Code on Windows 11 (VS Code) (2024).mp4", 
#      "/static/thumbnails/vscode.jpeg"))

# 提交更改并关闭连接
conn.commit()
conn.close()

print("所有表创建成功并插入了初始数据！")
