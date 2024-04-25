from flask import Flask, render_template, request, redirect, url_for, g, flash
import sqlite3

DATABASE = 'database.db'

app = Flask(__name__)
app.secret_key = 'a1b2c3d4e5f6g7h8i9j0'

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    db = get_db()
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        teacher_id = request.form.get('teacher_id')
        course_id = request.form.get('course_id')
        preferred1 = request.form.get('preferred1')
        preferred2 = request.form.get('preferred2')
        preferred3 = request.form.get('preferred3')

        all_preferences = {preferred1, preferred2, preferred3}
        if len(all_preferences) < 3 or "" in all_preferences:
            flash('Please select three different students for the preferences.', 'error')
            return redirect(url_for('questionnaire'))

        return redirect(url_for('thank_you_page'))
    else:
        students = db.execute('SELECT student_id, student_name FROM student').fetchall()
        teachers = db.execute('SELECT teacher_id, teacher_name FROM teacher').fetchall()
        courses = db.execute('SELECT course_id, course_name FROM course').fetchall()
        return render_template('questionnaire.html', students=students, teachers=teachers, courses=courses)

@app.route('/summary')
def summary():
    insights = {}  
    return render_template('summary.html', insights=insights)

@app.route('/thank_you')
def thank_you_page():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True, port=5558)
