from flask import Flask, request, render_template, jsonify, session, send_from_directory
import sqlite3
import openai  # 使用OpenAI API

app = Flask(__name__, template_folder='Youtube-Clone/templates', 
            static_folder='Youtube-Clone/static')
openai.api_key = "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"  # 替换为你的API密钥

# 获取数据库用户
def get_user(user_id):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    cursor.execute('SELECT user_id, password, is_admin FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    return user

# 数据库查询功能
def execute_sql(sql_query):
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result

# 权限检查
def check_permission(user_role, action):
    if action == "view_password" and user_role != "admin":
        return False
    return True

# 调用大模型，将自然语言转变为SQL
def generate_sql(natural_language_request):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Convert this request into SQL: {natural_language_request}",
        max_tokens=50
    )
    return response.choices[0].text.strip()

# 处理用户的log in请求（只处理POST请求）
@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        # 获取用户输入的 user_id 和 password
        user_id = request.form["user_id"]
        password = request.form["password"]

        # 从数据库获取用户信息
        user = get_user(user_id)

        if user:
            # 用户存在，检查密码是否正确
            stored_password = user[1]
            if stored_password == password:
                # 登录成功，检查是否是管理员
                is_admin = user[2]
                # 将 is_admin 保存到 session 中
                session["user_id"] = user_id
                session["is_admin"] = is_admin
                return jsonify({"message": "Successful!"})
            else:
                return jsonify({"error": "Wrong Password!"}), 401
        else:
            return jsonify({"error": "Invalid User!"}), 404
    
# 处理用户的search请求（只接受GET请求）
@app.route("/search", methods=["GET"])
def search():
    user_request = request.args.get("user_request")
    action = "search title like "
    field = "from video table"
    combined_request = f"{action} - {user_request} - {field}"
    user_role = session["is_admin"]

    # 调用大模型生成SQL
    sql_query = generate_sql(combined_request)

    # # 检查权限和业务逻辑
    # action = "query"  # 简单示例，设定操作类型
    # if not check_permission(user_role, action):
    #     return jsonify({"error": "无权执行此操作"})

    # 执行SQL并返回结果
    try:
        result = execute_sql(sql_query)
        return jsonify({"result": result})
    except Exception as e:
            return jsonify({"error": str(e)})

    return render_template("index.html")

# 处理用户的search subscription请求（只接受GET请求）
@app.route("/search_sub", methods=["GET"])
def search_sub():
    # user_request = request.args.get("user_request")
    action = "search all video"
    field = "from subscribe table"
    combined_request = f"{action} - {field}"
    user_role = session["is_admin"]

    # 调用大模型生成SQL
    sql_query = generate_sql(combined_request)

    # # 检查权限和业务逻辑
    # action = "query"  # 简单示例，设定操作类型
    # if not check_permission(user_role, action):
    #     return jsonify({"error": "无权执行此操作"})

    # 执行SQL并返回结果
    result = execute_sql(sql_query)
    return render_template("index.html", videos=result)

# 处理用户的search liked video请求（只接受GET请求）
@app.route("/search_liked", methods=["GET"])
def search_liked():
    # user_request = request.args.get("user_request")
    action = "search all video "
    field = "from liked video table"
    combined_request = f"{action} - {field}"
    user_role = session["is_admin"]

    # 调用大模型生成SQL
    sql_query = generate_sql(combined_request)

    # # 检查权限和业务逻辑
    # action = "query"  # 简单示例，设定操作类型
    # if not check_permission(user_role, action):
    #     return jsonify({"error": "无权执行此操作"})

    # 执行SQL并返回结果
    result = execute_sql(sql_query)
    return render_template("index.html", videos=result)

# 处理用户的delete请求（只接受POST请求）
@app.route("/delete", methods=["POST"])
def delete():#
    video_id = request.form.get("video_id")
    action = "delete video id = "
    field = "from video table"
    combined_request = f"{action} - {video_id} - {field}"
    user_role = session["is_admin"]

    # 调用大模型生成SQL
    sql_query = generate_sql(combined_request)

    # 检查权限和业务逻辑
    if not user_role:
        return jsonify({"error": "No Authorization!"})

    # 执行SQL并返回结果
    try:
        result = execute_sql(sql_query)
        return jsonify({"Success!"})
    except Exception as e:
            return jsonify({"Failed"})

    return render_template("index.html")

# 处理用户的delete subscribe video请求（只接受POST请求）
@app.route("/delete_sub", methods=["POST"])
def delete_sub():#
    video_id = request.form.get("video_id")
    action = "delete video id = "
    field = "from subscribe table"
    combined_request = f"{action} - {video_id} - {field}"
    user_role = session["is_admin"]

    # 调用大模型生成SQL
    sql_query = generate_sql(combined_request)

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
    sql_query = generate_sql(combined_request)

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
    sql_query = generate_sql(combined_request)

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
def add_liked():#
    video_id = request.form.get("video_id")
    action = "add video id = "
    field = "to liked video table"
    combined_request = f"{action} - {video_id} - {field}"
    user_role = session["is_admin"]

    # 调用大模型生成SQL
    sql_query = generate_sql(combined_request)

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

# 主页面：展示所有视频
@app.route('/')
def index():
    print("Index function called")  # 在控制台输出信息
    conn = sqlite3.connect('db.sqlite')  # 使用 SQLite 数据库
    conn.row_factory = sqlite3.Row  # 使得返回的查询结果为字典格式

    videos = conn.execute('SELECT * FROM videos').fetchall()  # 从数据库中获取所有视频
    conn.close()
    return render_template('index.html', videos=videos)

if __name__ == "__main__":
    app.run(debug=True)
