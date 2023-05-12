from flask import Flask, render_template, request, redirect, url_for,send_from_directory
import sqlite3

app = Flask(__name__)

# 设置数据库名称
DATABASE = 'downloads.db'

# 创建数据库表
def create_table():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS downloads
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                download_url TEXT NOT NULL,
                upload_date TEXT NOT NULL,
                priority INTEGER DEFAULT 0,
                category TEXT NOT NULL DEFAULT 0)''')
    conn.commit()
    conn.close()

# 在应用程序启动时创建数据库表和添加初始数据
@app.before_first_request
def init_db():
    create_table()

# 显示软件包列表
@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM downloads ORDER BY category,priority DESC')
    categories = {}
    downloads = cur.fetchall()
    for download in downloads:
        if download[6] not in categories:  
            categories[download[6]] = []  
        categories[download[6]].append(download)
    conn.close()
    return render_template('index.html', categories=categories)

# 添加软件包
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        download_url = request.form['download_url']
        upload_date = request.form['upload_date']
        priority = request.form['priority']   # 接收priority
        category = request.form['category'] # 分类

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute('''INSERT INTO downloads(name, description, download_url, upload_date, priority, category)
                    VALUES(?, ?, ?, ?, ?, ?)''', (name, description, download_url, upload_date, priority, category))
        conn.commit()
        conn.close()

        return redirect(url_for('admin'))
    else:
        return render_template('add.html')

# 编辑软件包
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM downloads WHERE id=?', (id,))
    download = cur.fetchone()
    conn.close()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        download_url = request.form['download_url']
        upload_date = request.form['upload_date']
        priority = request.form['priority']
        category = request.form['category']

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute('''UPDATE downloads SET name=?, description=?, download_url=?, upload_date=?, priority=?,category=? WHERE id=?''', (name, description, download_url, upload_date, priority, category, id))
        conn.commit()
        conn.close()

        return redirect(url_for('admin'))
    else:
        return render_template('edit.html', download=download)
    
# 删除软件包
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('DELETE FROM downloads WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/data/<path:filename>')
def data(filename):
    dir = '/app/data'
    return send_from_directory(dir, filename, as_attachment=True)

# 显示软件包列表
@app.route('/admin')
def admin():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM downloads ORDER BY category, priority DESC')
    categories = {}
    downloads = cur.fetchall()
    for download in downloads:
        if download[6] not in categories:  
            categories[download[6]] = []  
        categories[download[6]].append(download)
    conn.close()
    return render_template('admin.html', categories=categories)

if __name__ == '__main__':
    app.run(debug=True,port=80,host='0.0.0.0')