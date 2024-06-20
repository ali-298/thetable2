from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# In-memory data structure to store the schedule and the h1 content
schedule = {
    "الأحد": [("", "")] * 8,
    "الإثنين": [("", "")] * 8,
    "الثلاثاء": [("", "")] * 8,
    "الأربعاء": [("", "")] * 8,
    "الخميس": [("", "")] * 8
}
h1_content = "الجدول الدراسي"

@app.route('/')
def index():
    return render_template('index.html', days=schedule, h1_content=h1_content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'Sultan':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect password. Please try again.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        global h1_content
        h1_content = request.form.get('h1_content')
        day = request.form.get('day')
        classes = [(request.form.get(f'class{i}'), request.form.get(f'link{i}')) for i in range(1, 9)]
        schedule[day] = classes
        return redirect(url_for('index'))
    return render_template('dashboard.html', days=schedule, h1_content=h1_content)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
