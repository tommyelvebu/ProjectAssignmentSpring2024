from flask import Flask, render_template, request, redirect, url_for, g, flash
import sqlite3
from datetime import datetime
import re

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

        # Fetch the class_id for the selected student
        student_class = db.execute(
            'SELECT class_id FROM student WHERE student_id = ?',
            (student_id,)
        ).fetchone()

        # Fetch the class_id for the selected teacher
        teacher_class = db.execute(
            'SELECT class_id FROM class WHERE teacher_id = ?',
            (teacher_id,)
        ).fetchall()  # Teacher might be associated with multiple classes; adjust logic if teachers are restricted to one class.

        # Validate if the student's class is one of the teacher's classes
        if student_class and teacher_class:
            teacher_class_ids = [tc['class_id'] for tc in teacher_class]
            if student_class['class_id'] in teacher_class_ids:
                # Proceed with form processing and saving data
                return redirect(url_for('thank_you'))
            else:
                # Handling the error: Student does not belong to the teacher's class
                flash('The selected student does not belong to the specified teacher’s class.', 'error')
        else:
            # Handle possible errors if no records are found
            flash('Invalid student or teacher selected.', 'error')

        # If validation fails, re-render the form with previously submitted values
        return redirect(url_for('questionnaire'))

    else:
        # Fetch data from database to populate form
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

