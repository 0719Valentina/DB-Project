import sqlite3

# 连接到数据库
conn = sqlite3.connect('db.sqlite')  # 这里指定的是数据库文件名
cursor = conn.cursor()
# 新视频数据（不包含 Video_ID）
videos_data = [
    (1, "2024-11-15", "Your name", "A video about Your name.", 100, 50, "/static/videos/Your name.mp4", "/static/thumbnails/Your name.jpeg"),
    (1, "2024-11-16", "go out", "A video about go out.", 200, 75, "/static/videos/go out.mp4", "/static/thumbnails/go out.jpeg"),
    (1, "2024-11-17", "mixed cutting of ZHZ", "A video about mixed cutting of ZHZ.", 300, 125, "/static/videos/mixed cutting of ZHZ.mp4", "/static/thumbnails/mixed cutting of ZHZ.jpeg"),
    (1, "2024-11-19", "computer games", "A video about computer games.", 500, 300, "/static/videos/computer games.mp4", "/static/thumbnails/computer games.jpeg"),
    (1, "2024-11-20", "Light Years Away of Deng Ziqi", "A video about Light Years Away of Deng Ziqi.", 800, 600, "/static/videos/Light Years Away of Deng Ziqi.mp4", "/static/thumbnails/Light Years Away of Deng Ziqi.jpeg")
]

# 插入到 Videos 表（不包括 Video_ID）
for video in videos_data:
    cursor.execute('''
    INSERT INTO Videos (User_ID, Upload_Time, Title, Description, Views, Likes, Video_URL, Picture_URL)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', video)

# 提交更改
conn.commit()

print("新视频数据已插入成功！")
