from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users
                      (username text, balance real)
                   """)
    cursor.execute("SELECT username, balance FROM users ORDER BY balance DESC LIMIT 3")
    top_users = cursor.fetchall()
    return render_template('index.html', top_users=top_users)

@app.route('/click', methods=['POST'])
def click():
    username = request.form.get('username')  # получаем имя пользователя из формы
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT balance FROM users WHERE username = '{username}'")
    balance = cursor.fetchone()
    if balance is None:
        cursor.execute(f"INSERT INTO users VALUES ('{username}', 0.001)")
    else:
        cursor.execute(f"UPDATE users SET balance = {balance[0] + 0.001} WHERE username = '{username}'")
    conn.commit()
    return 'Success', 200

if __name__ == '__main__':
    app.run(debug=True)
