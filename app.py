from flask import Flask, render_template, request, redirect, url_for, g, flash, session
import sqlite3

DATABASE = 'database.db'

app = Flask(__name__)
app.secret_key = 'a1b2c3d4e5f6g7h8i9j0'  # for flashing system to work

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # checks if database connection is open, if not opens new connection
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)  # ensuring database is closed after requested
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    db = get_db()
    if request.method == 'POST':
        session['student_id'] = request.form.get('student_id')
        session['teacher_id'] = request.form.get('teacher_id')
        session['course_id'] = request.form.get('course_id')
        return redirect(url_for('preferred_1'))
    else:
        students = db.execute('SELECT student_id, student_name FROM student').fetchall()
        teachers = db.execute('SELECT teacher_id, teacher_name FROM teacher').fetchall()
        courses = db.execute('SELECT course_id, course_name FROM course').fetchall()
        return render_template('questionnaire.html', students=students, teachers=teachers, courses=courses)

@app.route('/preferred_1', methods=['GET', 'POST'])
def preferred_1():
    db = get_db()
    if request.method == 'POST':
        session['preferred1'] = request.form.get('preferred_student_id_1')
        return redirect(url_for('preferred_2'))  # Redirect to the next partner selection
    else:
        student_class_id = db.execute('SELECT class_id FROM student WHERE student_id = ?', (session['student_id'],)).fetchone()['class_id']
        classmates = db.execute('SELECT student_id, student_name FROM student WHERE class_id = ?', (student_class_id,)).fetchall()
        if not classmates:
            flash("No classmates available or unable to fetch data.")
            return redirect(url_for('questionnaire'))
        return render_template('preferred_1.html', classmates=classmates)

@app.route('/preferred_2', methods=['GET', 'POST'])
def preferred_2():
    db = get_db()
    if request.method == 'POST':
        session['preferred2'] = request.form.get('preferred_student_id_2')
        return redirect(url_for('preferred_3'))  # Redirect to the next partner selection
    else:
        student_class_id = db.execute('SELECT class_id FROM student WHERE student_id = ?', (session['student_id'],)).fetchone()['class_id']
        classmates = db.execute('SELECT student_id, student_name FROM student WHERE class_id = ?', (student_class_id,)).fetchall()
        if not classmates:
            flash("No classmates available or unable to fetch data.")
            return redirect(url_for('questionnaire'))
        return render_template('preferred_2.html', classmates=classmates)

@app.route('/preferred_3', methods=['GET', 'POST'])
def preferred_3():
    db = get_db()
    if request.method == 'POST':
        session['preferred3'] = request.form.get('preferred_student_id_3')
        return redirect(url_for('finalize_submission'))
    else:
        student_class_id = db.execute('SELECT class_id FROM student WHERE student_id = ?', (session['student_id'],)).fetchone()['class_id']
        classmates = db.execute('SELECT student_id, student_name FROM student WHERE class_id = ?', (student_class_id,)).fetchall()
        if not classmates:
            flash("No classmates available or unable to fetch data.")
            return redirect(url_for('questionnaire'))
        return render_template('preferred_3.html', classmates=classmates)


@app.route('/finalize_submission', methods=['GET', 'POST'])
def finalize_submission():
    db = get_db()
    try:
        db.execute('''
            INSERT INTO preference (student_id, teacher_id, course_id, preferred_student_id_1, preferred_student_id_2, preferred_student_id_3)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session['student_id'], session['teacher_id'], session['course_id'], session['preferred1'], session['preferred2'], session['preferred3']))
        db.commit()
    except sqlite3.IntegrityError as e:
        flash('There was an error saving your preferences. Please try again.', 'error')
        return redirect(url_for('questionnaire'))
    return redirect(url_for('thank_you_page'))

@app.route('/thank_you')
def thank_you_page():
    return render_template('thank_you.html')

@app.route('/summary')
def summary():
    return render_template('summary.html')


if __name__ == '__main__':
    app.run(debug=True, port=5558)
