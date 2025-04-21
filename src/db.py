from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# your classes here

class Instructor(db.Model):
    """
    Instructor model
    One-to-many relationship with courses
    """

    __tablename__ = "instructors"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    net_id = db.Column(db.string, nullable=False)

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
            "name":self.name,
            "net_id": self.net_id
        }
    
class Courses(db.Model):
    """
    Course model
    Many-to-many realtionship with students 
    One-to many relationship with instructors
    """
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

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
            "code":self.code,
            "name":self.name
        }

