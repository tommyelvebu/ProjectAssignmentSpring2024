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
  student_name TEXT NOT NULL UNIQUE,
  student_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  class_id INTEGER NOT NULL,
  FOREIGN KEY (class_id) REFERENCES class(class_id)
);

CREATE TABLE preference
(
  course_id INTEGER NOT NULL ,
  student_id INTEGER NOT NULL,
  prefererence_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  preference_rank INTEGER NOT NULL CHECK (preference_rank IN (1, 2, 3)),
  UNIQUE (student_id, course_id, preference_rank),
  FOREIGN KEY (student_id) REFERENCES student(student_id),
  FOREIGN KEY (course_id) REFERENCES course(course_id)
);


-- inserting authentic asian, african and norwegian names, along with dropdown values

INSERT INTO teacher (teacher_name) VALUES 
('Lei Chang'), 
('Amina Mohammed'), 
('Erik Hagen');


INSERT INTO course (course_name) VALUES 
('Math'), 
('Language'), 
('Science'), 
('Art'), 
('Gym');



INSERT INTO class (class_name, teacher_id) VALUES 
('1A', 1), 
('1B', 2), 
('1C', 3);

INSERT INTO student (student_name, class_id) VALUES 
('Jin Soo Kim', 1), ('David Obi', 1), ('Magnus Lothe', 1), ('An Dang', 1), ('Nia Miriam', 1),
('Chen Wei', 1), ('Kamau Wanjiru', 1), ('Nora Espeland', 1), ('Hiroshi Yamamoto', 1), ('Chike Okonkwo', 1),
('Oskar Nilesen', 2), ('Ming Yue', 2), ('Zola Adeola', 2), ('Sigrid Soldberg', 2), ('Haruto Watanabe', 2),
('Femi Hassan', 2), ('Emil Iversen', 2), ('Hye Jin Lee', 2), ('Amara Chibuzo', 2), ('Lily Andersen', 2),
('Suki Moto', 3), ('Isioma Jelani', 3), ('Mathias Hovde', 3), ('Yuki Tanaka', 3), ('Makena Onyango', 3),
('Sade Folami', 3), ('Ella Halvorsen', 3), ('Mei Lin', 3), ('Thea Fosse', 3), ('Lucas Moe', 3);