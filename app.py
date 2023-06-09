from flask import Flask, render_template, request, redirect, url_for,send_from_directory, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret key'

# 设置数据库名称
DATABASE = 'downloads.db'

# 创建数据库表
def create_table():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    #创建数据表
    cur.execute('''CREATE TABLE IF NOT EXISTS downloads
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                download_url TEXT NOT NULL,
                upload_date TEXT NOT NULL,
                priority INTEGER DEFAULT 0,
                category TEXT NOT NULL DEFAULT 0)''')
    #创建分类表
    cur.execute('''CREATE TABLE IF NOT EXISTS categorys
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT NOT NULL,
                category_id INTEGER DEFAULT 0)''')
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
    cur.execute('SELECT * FROM downloads JOIN categorys ON downloads.category = categorys.category_name ORDER BY categorys.category_id DESC, downloads.priority DESC')
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
        #判断分类是否存在
        cur.execute('SELECT * FROM categorys WHERE category_name=?', (category,))
        row = cur.fetchone()
        if row is None:
            cur.execute('''INSERT INTO categorys(category_name, category_id)
                        VALUES(?, ?)''', (category, 0))
        else:
            pass
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

# 编辑分类
@app.route('/edit_category', methods=['GET', 'POST'])
def edit_category():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM categorys')
    categorys = cur.fetchall()
    conn.close()

    if request.method == 'POST':
        category_name = request.form['category_name']
        category_id = request.form['category_id']

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        # 判断分类是否存在
        cur.execute('SELECT * FROM categorys WHERE category_name=?', (category_name,))
        row = cur.fetchone()
        if row is None or category_name == row[1]:
            cur.execute('''UPDATE categorys SET category_name=?, category_id=? WHERE category_name=?''', (category_name, category_id, category_name))
        conn.commit()
        conn.close()

        return redirect(url_for('admin'))
    else:
        return render_template('edit_category.html', categorys=categorys)
    
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
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM downloads JOIN categorys ON downloads.category = categorys.category_name ORDER BY categorys.category_id DESC, downloads.priority DESC')
    categories = {}
    downloads = cur.fetchall()
    for download in downloads:
        if download[6] not in categories:  
            categories[download[6]] = []  
        categories[download[6]].append(download)
    conn.close()
    return render_template('admin.html', categories=categories)

# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
         # 判断用户名和密码是否为空
        if not username or not password:
            return render_template('login.html', error='用户名或密码为空')
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='用户名或密码错误')
    else:
        return render_template('login.html')

# 退出登录
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,port=80,host='0.0.0.0')