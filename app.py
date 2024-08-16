from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import string
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

DATABASE = 'urls.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS urls
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         original_url TEXT NOT NULL,
                         short_url TEXT NOT NULL UNIQUE)''')
        conn.commit()

def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        with get_db() as conn:
            short_url = generate_short_url()
            conn.execute('INSERT INTO urls (original_url, short_url) VALUES (?, ?)',
                         (original_url, short_url))
            conn.commit()
        flash(f'Short URL created: {request.url_root}{short_url}')
        return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_url(short_url):
    with get_db() as conn:
        cur = conn.execute('SELECT original_url FROM urls WHERE short_url = ?',
                           (short_url,))
        result = cur.fetchone()
        if result:
            return redirect(result[0])
        else:
            flash('Invalid URL!')
            return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
