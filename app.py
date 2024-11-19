from flask import Flask, request, jsonify, render_template
import sqlite3
import random

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            coins INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Route: Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route: Register new user
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
        conn.commit()
        return jsonify({"message": f"User '{username}' registered successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists!"}), 400
    finally:
        conn.close()

# Route: Mine resources
@app.route('/mine', methods=['POST'])
def mine():
    username = request.form.get('username')
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute('SELECT coins FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result:
        coins_gained = random.randint(1, 10)  # Simulate mining
        new_total = result[0] + coins_gained
        cursor.execute('UPDATE users SET coins = ? WHERE username = ?', (new_total, username))
        conn.commit()
        conn.close()
        return jsonify({"message": f"{username} mined {coins_gained} coins!", "total_coins": new_total})
    else:
        conn.close()
        return jsonify({"error": "User not found!"}), 404

# Route: Leaderboard
@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, coins FROM users ORDER BY coins DESC LIMIT 10')
    leaderboard = cursor.fetchall()
    conn.close()
    return jsonify({"leaderboard": leaderboard})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
