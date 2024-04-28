from flask import Flask, render_template, request, redirect, url_for, g, flash
import sqlite3

DATABASE = 'database.db'

app = Flask(__name__)
app.secret_key = 'a1b2c3d4e5f6g7h8i9j0' #for flashing system to work 

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row      #checks if database connection is open, if not opens new connection
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)    #ensuring database is closed after requested
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
        preferred1 = request.form.get('preferred_student_id_1')
        preferred2 = request.form.get('preferred_student_id_2')
        preferred3 = request.form.get('preferred_student_id_3')

        print("IDs:", student_id, teacher_id, course_id, preferred1, preferred2, preferred3)  # Debugging output


        # checks if the student_id has already submitted a form
        existing_submission = db.execute(
            'SELECT * FROM preference WHERE student_id = ? AND course_id = ?', (student_id, course_id)).fetchone()
        if existing_submission:
            flash('You have already submitted this form for this course. Multiple submissions are not allowed.', 'error')
            return redirect(url_for('questionnaire'))

        # checks if student and teacher are in the same class
        student_class = db.execute(
            'SELECT class_id FROM student WHERE student_id = ?', (student_id,)).fetchone()
        teacher_class = db.execute(
            'SELECT class_id FROM class WHERE teacher_id = ?', (teacher_id,)).fetchone()
        if student_class['class_id'] != teacher_class['class_id']:
            flash('The selected student does not belong to the selected teacher\'s class.', 'error')
            return redirect(url_for('questionnaire'))

        # checks if all students (from preference 1,2,3) are unique 
        if len({preferred1, preferred2, preferred3}) < 3 or "" in [preferred1, preferred2, preferred3]:
            flash('Please select three different students for the preferences.', 'error')
            return redirect(url_for('questionnaire'))

        try:
            db.execute('''
                INSERT INTO preference (student_id, teacher_id, course_id, preferred_student_id_1, preferred_student_id_2, preferred_student_id_3)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, teacher_id, course_id, preferred1, preferred2, preferred3))
            db.commit()
        except sqlite3.IntegrityError as e:
            flash('There was an error saving your preferences. Please try again.', 'error')
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
