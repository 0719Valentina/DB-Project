import sqlite3

# 连接到数据库
conn = sqlite3.connect('db.sqlite')  # 这里指定的是数据库文件名
cursor = conn.cursor()
# 新视频数据
videos_data = [
    (1, 1, "2024-11-15", "Your name",6, "A video about Your name.", 100, 50, "/static/videos/Your name.mp4", "/static/thumbnails/Your name.png"),
    (2, 1, "2024-11-16", "go out",6, "A video about go out.", 200, 75, "/static/videos/go out.mp4", "/static/thumbnails/go out.png"),
    (3, 1, "2024-11-17", "mixed cutting of ZHZ",6, "A video about mixed cutting of ZHZ.", 300, 125, "/static/videos/mixed cutting of ZHZ.mp4", "/static/thumbnails/mixed cutting of ZHZ.png"),
    (4, 1, "2024-11-19", "computer games",6, "A video about computer games.", 500, 300, "/static/videos/computer games.mp4", "/static/thumbnails/computer games.png"),
    (5, 1, "2024-11-20", "traditional Chinese opera of Zhou Shen", 6,"A video about traditional Chinese opera of Zhou Shen.", 800, 600, "/static/videos/traditional Chinese opera of Zhou Shen.mp4", "/static/thumbnails/traditional Chinese opera of Zhou Shen.png"),
    (6, 1, "2024-11-20", "eat1",4, "A video about eating.", 120, 80, "/static/videos/eat1.mp4", "/static/thumbnails/eat1.png"),
    (7, 1, "2024-11-20", "eat2",4, "A video about eating.", 150, 95, "/static/videos/eat2.mp4", "/static/thumbnails/eat2.png"),
    (8, 1, "2024-11-20", "eat3",4, "A video about eating.", 180, 110, "/static/videos/eat3.mp4", "/static/thumbnails/eat3.png"),
    (9, 1, "2024-11-21", "sports1",3, "A video about sports.", 250, 140, "/static/videos/sports1.mp4", "/static/thumbnails/sports1.png"),
    (10, 1, "2024-11-21", "sports2", 3,"A video about sports.", 275, 155, "/static/videos/sports2.mp4", "/static/thumbnails/sports2.png"),
    (11, 2, "2024-11-21", "sports3", 3,"A video about sports.", 300, 175, "/static/videos/sports3.mp4", "/static/thumbnails/sports3.png"),
    (12, 3, "2024-11-22", "edu1",2, "A video about education.", 320, 190, "/static/videos/edu1.mp4", "/static/thumbnails/edu1.png"),
    (13, 2, "2024-11-22", "edu2", 2,"A video about education.", 340, 200, "/static/videos/edu2.mp4", "/static/thumbnails/edu2.png"),
    (14, 2, "2024-11-22", "edu3",2, "A video about education.", 360, 215, "/static/videos/edu3.mp4", "/static/thumbnails/edu3.png"),
    (15, 1, "2024-11-23", "wl1",1, "A video about wildlife.", 150, 90, "/static/videos/wl1.mp4", "/static/thumbnails/wl1.png"),
    (16, 2, "2024-11-23", "wl2",1, "A video about wildlife.", 180, 110, "/static/videos/wl2.mp4", "/static/thumbnails/wl2.png"),
    (17, 1, "2024-11-23", "wl3",1, "A video about wildlife.", 200, 120, "/static/videos/wl3.mp4", "/static/thumbnails/wl3.png"),
    (18, 3, "2024-11-24", "laugh1",5, "A video about laughter.", 100, 70, "/static/videos/laugh1.mp4", "/static/thumbnails/laugh1.png"),
    (19, 1, "2024-11-24", "laugh2",5, "A video about laughter.", 150, 90, "/static/videos/laugh2.mp4", "/static/thumbnails/laugh2.png"),
    (20, 4, "2024-11-24", "laugh3",5, "A video about laughter.", 200, 110, "/static/videos/laugh3.mp4", "/static/thumbnails/laugh3.png")
]

# 插入到 Videos 表
for video in videos_data:
    cursor.execute('''
    INSERT INTO Videos (Video_ID, User_ID, Upload_Time, Title, Category_ID, Description, Views, Likes, Video_URL, Picture_URL)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', video)

# 提交更改
conn.commit()

print("新视频数据已插入成功！")