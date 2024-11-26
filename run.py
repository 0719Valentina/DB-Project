import subprocess
import os

# 获取当前运行脚本的目录
base_dir = os.path.dirname(os.path.abspath(__file__))

try:
    # 运行 create_db.py
    print("正在运行 create_db.py...")
    subprocess.run(["python", os.path.join(base_dir, "create_db.py")], check=True)
    print("create_db.py 运行成功！")

    print("正在运行 addcategories.py...")
    subprocess.run(["python", os.path.join(base_dir, "addcategories.py")], check=True)
    print("addcategories.py 运行成功！")
    
    # 运行 addusers.py
    print("正在运行 addusers.py...")
    subprocess.run(["python", os.path.join(base_dir, "addusers.py")], check=True)
    print("addusers.py 运行成功！")

    # 运行 addvideos.py
    print("正在运行 addvideos.py...")
    subprocess.run(["python", os.path.join(base_dir, "addvideos.py")], check=True)
    print("addvideos.py 运行成功！")

    print("所有脚本运行完毕！")

except subprocess.CalledProcessError as e:
    print(f"运行脚本时出错：{e}")
except Exception as e:
    print(f"运行脚本时遇到未知错误：{e}")