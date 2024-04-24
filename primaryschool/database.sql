CREATE TABLE teacher
(
  teacher_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  teacher_name TEXT NOT NULL UNIQUE
);

CREATE TABLE course
(
  course_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  course_name TEXT NOT NULL UNIQUE
);

CREATE TABLE class
(
  class_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  class_name TEXT NOT NULL UNIQUE,
  teacher_id INTEGER NOT NULL,
  FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id)
);

CREATE TABLE student
(
  student_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  student_name TEXT NOT NULL UNIQUE,
  class_id INTEGER NOT NULL,
  FOREIGN KEY (class_id) REFERENCES class(class_id)
);

CREATE TABLE study
(
  course_id INTEGER NOT NULL,
  student_id INTEGER NOT NULL,
  PRIMARY KEY (course_id, student_id),
  FOREIGN KEY (course_id) REFERENCES course(course_id),
  FOREIGN KEY (student_id) REFERENCES student(student_id)
);

CREATE TABLE preferences
(
  preference_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  preferred_student_id INTEGER NOT NULL,
  preference_rank INTEGER NOT NULL CHECK (preference_rank IN (1, 2, 3)),
  UNIQUE (student_id, preferred_student_id, preference_rank),
  FOREIGN KEY (student_id) REFERENCES student(student_id),
  FOREIGN KEY (preferred_student_id) REFERENCES student(student_id)
);
