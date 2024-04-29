from flask import Flask, render_template, request, redirect, url_for, g, flash
import sqlite3

DATABASE = 'database.db'

app = Flask(__name__)
app.secret_key = 'a1b2c3d4e5f6g7h8i9j0'  # For flashing system to work

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Checks if database connection is open, if not opens new connection
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)  # Ensuring database is closed after request
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    db = get_db()
    selected_teacher = None
    selected_student = None
    selected_teacher_name = None
    selected_student_name = None
    selected_course = None  
    selected_course_name = None  
    classmates = []
    students = []
    if request.method == 'POST':
        teacher_id = request.form.get('teacher_id')
        student_id = request.form.get('student_id')
        course_id = request.form.get('course_id') 

        if teacher_id:
            selected_teacher = teacher_id
            teacher_info = db.execute('SELECT teacher_name FROM teacher WHERE teacher_id = ?', (teacher_id,)).fetchone()
            selected_teacher_name = teacher_info['teacher_name'] if teacher_info else 'Teacher not found'
            students = db.execute('''
                SELECT s.student_id, s.student_name 
                FROM student s
                JOIN class c ON s.class_id = c.class_id
                WHERE c.teacher_id = ?
            ''', (teacher_id,)).fetchall()

        if student_id:
            selected_student = student_id
            student_info = db.execute('SELECT student_name FROM student WHERE student_id = ?', (student_id,)).fetchone()
            selected_student_name = student_info['student_name'] if student_info else 'Student not found'
            classmates = db.execute(
                'SELECT student_id, student_name FROM student WHERE class_id = (SELECT class_id FROM student WHERE student_id = ?) AND student_id != ?',
                (student_id, student_id)
            ).fetchall()

        if course_id: 
            selected_course = course_id
            course_info = db.execute('SELECT course_name FROM course WHERE course_id = ?', (course_id,)).fetchone()
            selected_course_name = course_info['course_name'] if course_info else 'Course not found'

    teachers = db.execute('SELECT teacher_id, teacher_name FROM teacher').fetchall()
    courses = db.execute('SELECT course_id, course_name FROM course').fetchall() 
    return render_template('questionnaire.html', teachers=teachers, students=students, classmates=classmates, courses=courses, 
                           selected_teacher=selected_teacher, selected_student=selected_student,
                           selected_course=selected_course, selected_teacher_name=selected_teacher_name,
                           selected_student_name=selected_student_name, selected_course_name=selected_course_name)  


@app.route('/get_students/<int:teacher_id>')
def get_students(teacher_id):
    db = get_db()
    students = db.execute('''
        SELECT s.student_id, s.student_name 
        FROM student s
        JOIN class c ON s.class_id = c.class_id
        WHERE c.teacher_id = ?
    ''', (teacher_id,)).fetchall()
    return {'students': [dict(student) for student in students]}

@app.route('/get_classmates/<int:student_id>')
def get_classmates(student_id):
    db = get_db()
    class_id = db.execute('SELECT class_id FROM student WHERE student_id = ?', (student_id,)).fetchone()
    if class_id:
        classmates = db.execute(
            'SELECT student_id, student_name FROM student WHERE class_id = ? AND student_id != ?',
            (class_id['class_id'], student_id)
        ).fetchall()
        return {'classmates': [dict(classmate) for classmate in classmates]}
    return {'classmates': []}

@app.route('/summary')
def summary():
    cursor = get_db().cursor()
    cursor.execute(
        """
        SELECT s1.student_name, c1.course_name, s2.student_name AS preferred_student_name, c2.course_name AS preferred_student_preferred_course
        FROM (
            SELECT p1.student_id, p1.course_id, p2.student_id AS p2_student_id, p2.course_id AS p2_course_id
            FROM preference AS p1
            JOIN preference AS p2 
            ON (p1.preferred_student_id_1=p2.student_id OR p1.preferred_student_id_2=p2.student_id OR p1.preferred_student_id_3=p2.student_id)
            AND (p1.student_id=p2.preferred_student_id_1 OR p1.student_id=p2.preferred_student_id_2 OR p1.student_id=p2.preferred_student_id_3)
            WHERE p1.student_id<p2.student_id
            ) AS a
        JOIN student s1 ON a.student_id=s1.student_id 
        JOIN student s2 ON a.P2_student_id=s2.student_id
        JOIN course c1 ON a.course_id=c1.course_id
        JOIN course c2 ON a.p2_course_id=c2.course_id
         """
             )
    student_pairs=cursor.fetchall()
    

    cursor.execute(
        """
    SELECT class_name, student_name, ranking
    FROM(
        SELECT c.class_name, s.student_name, COUNT(*) AS counts, DENSE_RANK() OVER(PARTITION BY c.class_id ORDER BY COUNT(*) DESC) AS ranking
        FROM student s
        JOIN preference p ON p.preferred_student_id_1=s.student_id 
        JOIN class c ON s.class_id=c.class_id
        GROUP BY class_name, student_name
        )
    WHERE ranking<=3
        
        """
    )
    popular_students=cursor.fetchall()
    

    cursor.execute(
        """
        SELECT DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS rank, c.course_name
        FROM course c
        JOIN preference p ON c.course_id=p.course_id
        GROUP BY c.course_id, c.course_name
        ORDER BY COUNT(*) DESC
        """
    )
    popular_courses=cursor.fetchall()
    
    return render_template('summary.html', student_pairs=student_pairs, popular_students=popular_students, popular_courses=popular_courses)

@app.route('/thank_you')
def thank_you_page():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True, port=5558)
