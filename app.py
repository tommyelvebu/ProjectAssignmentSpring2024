from flask import Flask, render_template, request, redirect, url_for, g, flash
import sqlite3
from datetime import datetime
import re

DATABASE = 'database.db'

app = Flask(__name__)


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
        return redirect(url_for('thank_you'))
    else:
        teachers = db.execute('SELECT teacher_id, teacher_name FROM teacher').fetchall()
        courses = db.execute('SELECT course_id, course_name FROM course').fetchall()
        students = db.execute('SELECT student_id, student_name FROM student').fetchall()
        return render_template('questionnaire.html', teachers=teachers, courses=courses, students=students)




@app.route('/summary')
def summary():
    insights = {}  
    return render_template('summary.html', insights=insights)



@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


if __name__ == '__main__':
    app.run(debug=True, port=5558)

