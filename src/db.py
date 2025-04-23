from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# your classes here

#association table for many-to-many between users and courses(students)
students_table = db.Table(
    "students",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id"), primary_key=True),
)

#association table for many-to-many between users and courses(instructors)
instructors_table = db.Table(
    "instructors",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id"), primary_key=True),
)


class User(db.Model):
    """
    User model for both students and instructors
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    net_id = db.Column(db.String, nullable=False)

    #courses this instructor teaches
    instructor_courses = db.relationship(
        "Course", secondary=instructors_table, back_populates="instructors"
    )

    #courses this user student is in
    student_courses = db.relationship(
        "Course", secondary=students_table, back_populates="students"
    )

    def __init__(self, **kwargs):
        """
        Initialize instructor object
        """
        self.name = kwargs.get("name", "")
        self.net_id = kwargs.get("net_id", "")

    def serialize(self):
        """
        Serializing instructor object to be returned
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.net_id,
            "courses": [c.simple_serialize() for c in self.student_courses + self.instructor_courses]
        }
    
    def serialize_no_courses(self):
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.net_id
        }

    
class Course(db.Model):
    """
    Course model
    """
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    assignments = db.relationship("Assignment", cascade="delete")

    instructors = db.relationship(
        "User", secondary=instructors_table, back_populates="instructor_courses"
    )

    students = db.relationship(
        "User", secondary=instructors_table, back_populates="student_courses"
    )

    def __init__(self, **kwargs):
        """
        Initialize course object
        """
        self.code = kwargs.get("code", "")
        self.name = kwargs.get("name", "")


    def serialize(self):
        """
        Serializing a course object to be returned
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [a.serialize_no_course() for a in self.assignments],
            "instructors": [i.serialize_no_courses() for i in self.instructors],
            "students": [s.serialize_no_courses() for s in self.students]
        }
    

class Assignment(db.Model):
    """
    Assignment model
    """
    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)


    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    course = db.relationship("Course", backref="assignment_course")


    def __init__(self, **kwargs):
        """
        Initializes Assignment object
        """
        self.title = kwargs.get("title", "")
        self.due_date = kwargs.get("due_date", "")
        self.course_id = kwargs.get("course_id")


    def serialize(self):
        """
        Serializing assignment object to be returned
        """
        return {
            "id":self.id,
            "title": self.title,
            "due_date": self.due_date,
            "course":{
                "id":self.course.id,
                "code": self.course.code,
                "name": self.course.name
            },
        }
    
    def serialize_no_course(self):
        """
        Serializing without a course
        """
        return {
            "id":self.id,
            "title": self.title,
            "due_date": self.due_date
        }


