from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database setup function
def init_db():
    if not os.path.exists('blog.db'):
        with sqlite3.connect('blog.db') as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS blog (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL
                )
            ''')
        print("Database created and table initialized.")
    else:
        print("Database already exists.")

# Initialize the database
init_db()

# Route for the home page
@app.route('/')
def home():
    with sqlite3.connect('blog.db') as conn:
        cursor = conn.execute('SELECT id, title FROM blog')
        blogs = cursor.fetchall()
    return render_template('home.html', blogs=blogs)

# Route to write a new blog post
@app.route('/write', methods=['GET', 'POST'])
def write_blog():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        with sqlite3.connect('blog.db') as conn:
            conn.execute('INSERT INTO blog (title, content) VALUES (?, ?)', (title, content))
        return redirect(url_for('home'))
    return render_template('write_blog.html')

# Route to view a specific blog post
@app.route('/blog/<int:blog_id>')
def view_blog(blog_id):
    with sqlite3.connect('blog.db') as conn:
        cursor = conn.execute('SELECT title, content FROM blog WHERE id = ?', (blog_id,))
        blog = cursor.fetchone()
    if blog:
        return render_template('view_blog.html', title=blog[0], content=blog[1])
    return "Blog not found", 404

if __name__ == '__main__':
    app.run(debug=True)
