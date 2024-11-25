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

# 创建 Music 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS Music (
    Music_ID INTEGER PRIMARY KEY,
    Artist_ID INTEGER NOT NULL,
    Composer_ID INTEGER NOT NULL,
    Title TEXT NOT NULL,
    Album INTEGER NOT NULL,
    Duration INTEGER NOT NULL,
    FOREIGN KEY (Music_ID) REFERENCES Videos (Video_ID),
    FOREIGN KEY (Artist_ID) REFERENCES Users (User_ID),
    FOREIGN KEY (Composer_ID) REFERENCES Users (User_ID),
    FOREIGN KEY (Album) REFERENCES Album (Album_ID)
)
''')

# 创建 Album 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS Album (
    Album_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    Release_Date TEXT NOT NULL,
    Cover_Image TEXT
)
''')

# 创建 Music Section 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS Music_Section (
    Section_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Section_Name TEXT NOT NULL
)
''')

# 创建 Section_Album 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS Section_Album (
    Section_ID INTEGER NOT NULL,
    Album_ID INTEGER NOT NULL,
    Recommendation_Order INTEGER NOT NULL,
    PRIMARY KEY (Section_ID, Album_ID),
    FOREIGN KEY (Section_ID) REFERENCES Music_Section (Section_ID),
    FOREIGN KEY (Album_ID) REFERENCES Album (Album_ID)
)
''')

# 创建 Game 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS Game (
    Game_ID INTEGER PRIMARY KEY,
    Game_Name TEXT NOT NULL,
    Genre TEXT NOT NULL,
    Developer INTEGER NOT NULL,
    Section INTEGER NOT NULL,
    FOREIGN KEY (Game_ID) REFERENCES Videos (Video_ID),
    FOREIGN KEY (Developer) REFERENCES Users (User_ID),
    FOREIGN KEY (Section) REFERENCES Game_Page (Section_ID)
)
''')

# 创建 Game_Page 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS Game_Page (
    Section_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Section_Name TEXT NOT NULL
)
''')

# 创建 Movies 表
cursor.execute('''
CREATE TABLE IF NOT EXISTS Movies (
    Movie_ID INTEGER PRIMARY KEY,
    Title TEXT NOT NULL,
    Content TEXT NOT NULL,
    Director_ID INTEGER NOT NULL,
    Genre TEXT NOT NULL,
    Release_Date TEXT NOT NULL,
    FOREIGN KEY (Movie_ID) REFERENCES Videos (Video_ID),
    FOREIGN KEY (Director_ID) REFERENCES Users (User_ID)
)
''')

# 提交更改并关闭连接
conn.commit()
conn.close()

print("所有表创建成功！")