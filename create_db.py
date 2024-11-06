import sqlite3

# 连接到数据库
conn = sqlite3.connect('db.sqlite')  # 这里指定的是数据库文件名
cursor = conn.cursor()

# 创建videos表
cursor.execute('''
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,         -- 视频标题
    url TEXT NOT NULL,           -- 视频链接
    upload_date TEXT,            -- 上传日期
    duration INTEGER,            -- 视频时长，单位秒
    thumbnail_url TEXT           -- 视频缩略图链接
)
''')

# 插入表项到videos表
# 插入视频数据
cursor.execute('''
INSERT INTO videos (id, title, url, upload_date, duration, thumbnail_url)
VALUES (?, ?, ?, ?, ?, ?)
''', (1, "How to Install Visual Studio", 
      "/static/videos/How Install Visual Studio Code on Windows 11 (VS Code) (2024).mp4", "2024-11-06", 300, 
      "/static/thumbnails/vscode.jpeg"))

# 提交更改并关闭连接
conn.commit()
conn.close()

print("数据库和表创建成功！")