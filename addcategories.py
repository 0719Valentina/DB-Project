import sqlite3

# 连接到数据库
conn = sqlite3.connect('db.sqlite')  # 指定数据库文件名
cursor = conn.cursor()

# 插入数据到 Video_Category 表
categories = [
    ('wildlife',),
    ('education',),
    ('sports',),
    ('eating',),
    ('laughter',),
    ('others',)
]

# 使用 executemany 插入多个类别
cursor.executemany('''
INSERT INTO Video_Category (Category_Name)
VALUES (?)
''', categories)

# 提交更改并关闭连接
conn.commit()
conn.close()

print("Video_Category 表已成功插入这些类型！")