from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app) # 解决跨域问题（让 Godot 网页能请求到这个接口）

# 1. 初始化数据库（第一次运行会自动生成 game.db 文件）
def init_db():
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 2. 提交分数的接口 (POST)
@app.route('/api/submit', methods=['POST'])
def submit_score():
    data = request.json
    name = data.get('name')
    score = data.get('score')
    
    if not name or not score:
        return jsonify({"status": "error", "message": "名字和分数不能为空"}), 400

    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leaderboard (name, score) VALUES (?, ?)", (name, score))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "分数已记录"})

# 3. 获取排行榜的接口 (GET)
@app.route('/api/rank', methods=['GET'])
def get_rank():
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    # 按分数从高到低，取前10名
    cursor.execute("SELECT name, score FROM leaderboard ORDER BY score DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    
    # 转换成字典列表格式返回
    result = [{"name": row[0], "score": row[1]} for row in rows]
    return jsonify(result)

if __name__ == '__main__':
    init_db()
    # 运行在本地 5000 端口
    app.run(host='127.0.0.1', port=5000, debug=True)