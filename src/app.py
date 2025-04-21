from db import db
from flask import Flask

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


# your routes here
@app.route("/api/courses/", methods=["GET"])
def get_all_courses():
    """
    Getting all the courses
    """
    pass


@app.route("/api/courses/", methods=["POST"])
def create_course():
    """
    Creating a course
    """
    pass


@app.route("/api/courses/", methods=["GET"])
def get_specific_course():
    """
    Getting a course 
    """
    pass


@app.route("/api/courses/<int:id>/", methods=["GET"])
def get_specific_course(course_id):
    """
    Getting a specific course using course id
    """
    pass


@app.route("/api/courses/<int:id>/", methods=["DELETE"])
def delete_course(id):
    """
    Deleting a specific course using course id
    """
    pass


@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Creating a user
    """
    pass


@app.route("/api/users/<int:id>/", methods=["GET"])
def get_specific_user(id):
    """
    Getting a specific user
    """
    pass

@app.route("/api/courses/<int:id>/add/", methods=["POST"])
def add_course():
    """
    Adding a course to a user
    """
    pass


@app.route("/api/courses/<int:id>/assignment/", methods=["POST"])
def create_assignment_to_course():
    """
    Creates ans assignment for a course
    """
    pass



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
