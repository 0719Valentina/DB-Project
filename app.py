from flask import Flask, request, render_template, jsonify, session, send_from_directory, redirect, url_for
import sqlite3
import os
import time
from datetime import datetime
from openai import OpenAI # 使用OpenAI API
from ratelimit import limits, sleep_and_retry

app = Flask(__name__, template_folder='Youtube-Clone/templates', 
            static_folder='Youtube-Clone/static')
app.secret_key = os.urandom(24)

# client = OpenAI(
#     api_key="sk-Dk1Bl0YFOFHsv9hjH7m3G7IJBqEkNvsUIGH5W6XdC7PtaQnh", 
#     base_url="https://api.moonshot.cn/v1",
# )

# # 数据库的表格信息
# path = 'create_db.py'
# # 打开文件并读取所有内容
# with open(path, 'r', encoding='utf-8') as file:
#     preInfo = file.read()

# 获取数据库用户
def get_user(user_name):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    cursor.execute('SELECT UserName, Password, Role FROM users WHERE UserName = ?', (user_name,))
    user = cursor.fetchone()
    conn.close()

    return user

# 更新用户最新登陆时间
def update_login_time(user_id):
    """更新用户的最后登录时间"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE users SET last_login = ? WHERE user_id = ?", (now, user_id))
    conn.commit()
    conn.close()


# 数据库查询功能
def execute_sql(sql_query, params=()):
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    result = cursor.execute(sql_query, params).fetchall()
    conn.commit()
    conn.close()
    return result

# 权限检查
def check_permission(user_role, action):
    if action == "view_password" and user_role != "admin":
        return False
    return True

# # 调用大模型，将自然语言转变为SQL
# @sleep_and_retry
# @limits(calls=1, period=5)  # 每 1 秒限制 1 次调用
# def generate_sql(natural_language_request):
#     response = client.chat.completions.create(
#         model = "moonshot-v1-8k",
#         messages=[
#             {"role": "system", "content": "This is the database information:" + preInfo},
#             {"role": "user", "content": f"Convert this request into correct SQL command. Provide only the SQL query without extra comments: {natural_language_request}"}
#         ],
#         temperature = 0.3,
#     )
#     sql_query = response.choices[0].message.content

#     # 去除可能存在的代码块标记（'''sql 和 '''）
#     if sql_query.startswith("```sql"):
#         sql_query = sql_query[6:]  # 去掉开头的 '''sql
#     if sql_query.endswith("```"):
#         sql_query = sql_query[:-3]  # 去掉结尾的 '''

#     # 去除额外的空白字符
#     return sql_query.strip()

@app.route('/update_history', methods=['POST'])
def update_history():
    data = request.json
    user_id = data.get('user_id')
    video_id = data.get('video_id')
    username = data.get('username')
    session["user_id"] = user_id

    if not video_id or not user_id:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    try:
        # 插入或更新历史记录
        cursor.execute('''
        INSERT OR REPLACE INTO History (User_ID, Video_ID, UserName, Watch_Time) 
        VALUES (?, ?, ?, datetime('now'))
        ''', (user_id, video_id, username))
        
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        conn.close()

@app.route('/get_user_id', methods=["POST"])
def get_user_id():
    try:
        username = session["user_name"]
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()

        cursor.execute('SELECT User_ID, UserName FROM users WHERE UserName = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            user_id = result[0]  # 假设查询返回的是一个元组 (user_id,)
            return jsonify({"user_id": user_id})
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": "Error retrieving user ID", "details": str(e)}), 500

# 处理用户的log in请求（只处理POST请求）
@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        # 获取用户输入的 user_id 和 password
        user_name = request.form["username"]
        password = request.form["password"]

        # 从数据库获取用户信息
        user = get_user(user_name)

        if user:
            # 用户存在，检查密码是否正确
            stored_password = user[1]
    
            if stored_password == password:
                # 登录成功，检查是否是管理员
                is_admin = user[2]
                # 将 is_admin 保存到中
                session["user_name"] = user_name
                session["is_admin"] = is_admin
                return index()
            else:
                return jsonify({"error": "Wrong Password!"}), 401
        else:
            return jsonify({"error": "Invalid User!"}), 404
        
    elif request.method == "GET":
        # 处理 GET 请求，渲染 login.html 页面
        return render_template("login.html")
    
# 处理用户的search请求（只接受GET请求）
@app.route("/search", methods=["GET"])
def search():
    user_request = request.args.get("user_request")

    sql_query = "SELECT * FROM videos WHERE title LIKE ?"
    result = execute_sql(sql_query, (f"%{user_request}%",))
    return render_template("likedVideos.html", videos=result)


# 处理用户的search subscription请求（只接受GET请求）
@app.route("/search_sub", methods=["GET"])
def search_sub():
    # user_request = request.args.get("user_request")
    action = "search all video"
    field = "from subscribe table"
    combined_request = f"{action} - {field}"
    user_role = session["is_admin"]

    sql_query = ''

    # # 检查权限和业务逻辑
    # action = "query"  # 简单示例，设定操作类型
    # if not check_permission(user_role, action):
    #     return jsonify({"error": "无权执行此操作"})

    # 执行SQL并返回结果
    result = execute_sql(sql_query)
    return render_template("index.html", videos=result)

# 处理用户的search liked video请求（只接受GET请求）
@app.route("/search_liked")
def search_liked():
    # user_request = request.args.get("user_request")
    user_id = session.get("user_id", None)  # 使用 `get` 来避免 KeyError
    if user_id is None:
        # 处理未登录或没有权限的情况
        return render_template("likedVideos.html", videos=None)
    
    sql_query = "SELECT * FROM Videos WHERE Video_ID IN (SELECT Video_ID FROM Liked_Video WHERE User_ID =?)"
    
    result = execute_sql(sql_query, (user_id,))
    return render_template("likedVideos.html", videos=result)

# 处理用户的search history请求
@app.route("/search_history")
def search_history():
    # user_request = request.args.get("user_request")
    username = session.get("user_name", None)  # 使用 `get` 来避免 KeyError
    
    if username is None:
        # 处理未登录或没有权限的情况
        return render_template("likedVideos.html", videos=None)

    sql_query = 'SELECT * FROM Videos WHERE Video_ID IN (SELECT Video_ID FROM History WHERE UserName =?)'
    result = execute_sql(sql_query,(username,))
    return render_template("likedVideos.html", videos=result)

# 处理用户的delete请求（只接受POST请求）
@app.route("/delete", methods=["POST"])
def delete():#
    data = request.get_json()  
    video_id = data["videoId"] 
    user_role = session.get("is_admin", None)  
    if user_role is None:
        # 处理未登录或没有权限的情况
        return jsonify({"message": "Not Login", "redirect": url_for('index')})

    sql_query = 'DELETE FROM Videos WHERE Video_ID=?'
    # 检查权限和业务逻辑
    if user_role != "Admin":
        return jsonify({"message": "No Authorization", "redirect": url_for('index')})

    # 执行SQL并返回结果
    try:
        result = execute_sql(sql_query,(video_id,))
        return jsonify({"message": "Success", "redirect": url_for('index')})
    except Exception as e:
            return jsonify({"message":"Failed"})

    return redirect(url_for("index"))

# 处理用户的delete subscribe video请求（只接受POST请求）
@app.route("/delete_sub", methods=["POST"])
def delete_sub():#
    video_id = request.form.get("video_id")
    action = "delete video id = "
    field = "from subscribe table"
    combined_request = f"{action} - {video_id} - {field}"
    user_role = session.get("is_admin", None)  # 使用 `get` 来避免 KeyError
    if user_role is None:
        # 处理未登录或没有权限的情况
        return redirect(url_for("login"))

    # 调用大模型生成SQL
    sql_query = ''

    # # 检查权限和业务逻辑
    # if not user_role:
    #     return jsonify({"error": "No Authorization!"})

    # 执行SQL并返回结果
    try:
        result = execute_sql(sql_query)
        return jsonify({"Success!"})
    except Exception as e:
            return jsonify({"Failed"})

    return render_template("index.html")

# 处理用户的delete liked video请求（只接受POST请求）
@app.route("/delete_liked", methods=["POST"])
def delete_liked():#
    video_id = request.form.get("video_id")
    action = "delete video id = "
    field = "from liked video table"
    combined_request = f"{action} - {video_id} - {field}"
    user_role = session["is_admin"]

    # 调用大模型生成SQL
    sql_query = ''

    # # 检查权限和业务逻辑
    # if not user_role:
    #     return jsonify({"error": "No Authorization!"})

    # 执行SQL并返回结果
    try:
        result = execute_sql(sql_query)
        return jsonify({"Success!"})
    except Exception as e:
            return jsonify({"Failed"})

    return render_template("index.html")

# 处理用户的add subscription请求（只接受POST请求）
@app.route("/add_sub", methods=["POST"])
def add_sub():#
    video_id = request.form.get("video_id")
    action = "add video id = "
    field = "to subscribe table"
    combined_request = f"{action} - {video_id} - {field}"
    user_role = session["is_admin"]

    # 调用大模型生成SQL
    sql_query = ""

    # # 检查权限和业务逻辑
    # if not user_role:
    #     return jsonify({"error": "No Authorization!"})

    # 执行SQL并返回结果
    try:
        result = execute_sql(sql_query)
        return jsonify({"Success!"})
    except Exception as e:
            return jsonify({"Failed"})

    return render_template("index.html")

# 处理用户的add liked video请求（只接受POST请求）
@app.route("/add_liked", methods=["POST"])
def add_liked():
    data = request.get_json()  
    user_id = data["userId"]   
    video_id = data["videoId"] 
    
    user_role = session["is_admin"]
    sql_query = '''
        INSERT OR REPLACE INTO Liked_Video (User_ID, Video_ID, Liked_Time) 
        VALUES (?, ?, datetime('now'))
        '''

    try:
        result = execute_sql(sql_query, (user_id, video_id))
        return jsonify({"message":"Success"})
    except Exception as e:
            return jsonify({"message":"Failed"})

    return render_template("index.html")

# 主页面：展示所有视频
@app.route('/')
def index():
    username = session.get('user_name')
    
    conn = sqlite3.connect('db.sqlite')  # 使用 SQLite 数据库
    conn.row_factory = sqlite3.Row  # 使得返回的查询结果为字典格式

    videos = conn.execute('SELECT * FROM videos').fetchall()  # 从数据库中获取所有视频
    wildlife_videos = conn.execute('SELECT * FROM videos WHERE Category_ID=1').fetchall()
    edu_videos = conn.execute('SELECT * FROM videos WHERE Category_ID=2').fetchall()
    sports_videos = conn.execute('SELECT * FROM videos WHERE Category_ID=3').fetchall()
    eating_videos = conn.execute('SELECT * FROM videos WHERE Category_ID=4').fetchall()
    Laughter_videos = conn.execute('SELECT * FROM videos WHERE Category_ID=5').fetchall()
    
    conn.close()
    return render_template('index.html', videos=videos, username=username, wildlife_videos=wildlife_videos, edu_videos=edu_videos,
                           sports_videos=sports_videos, eating_videos=eating_videos, Laughter_videos=Laughter_videos)

# 用户页面：展示用户信息或其他内容
@app.route('/user')
def user():
    print("User function called")  # 在控制台输出信息
    return render_template('user.html')  # 渲染 user.html

@app.route('/videoplayer/<int:video_id>')
def videoplayer(video_id):
    return render_template('videoplayer.html',video_id=video_id)  # 渲染 user.html

if __name__ == "__main__":
    app.run(debug=True)
