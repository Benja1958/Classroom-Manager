from db import db
from db import db, Course, User, Assignment
import json
from flask import Flask, request, jsonify


app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


# your routes here
def failure_response(message, code=404):
    return jsonify({'error': message}), code


def success_response(body, code=200):
    return jsonify(body), code


@app.route("/api/courses/", methods=["POST"])
def create_course():
    """
    Creates a course
    """
    body = json.loads(request.data)
    code = body.get("code")
    name = body.get("name")
    if code is None or name is None:
        return failure_response("Missing code or name", 400)
    
    new_course = Course(code = body.get("code"), name = body.get("name"))
    db.session.add(new_course)
    db.session.commit()
    return success_response(new_course.serialize(), 201)

@app.route("/api/courses/", methods=["GET"])
def get_all_courses():
    """
    Getting all the courses
    """
    return success_response({"courses": [c.serialize() for c in Course.query.all()]})
    

@app.route("/api/courses/<int:id>/", methods=["GET"])
def get_specific_course(id):
    """
    Getting a specific course using course id
    """
    course = Course.query.filter_by(id=id).first()
    if course is None:
        return failure_response("Course not found")
    return success_response(course.serialize())


@app.route("/api/courses/<int:id>/", methods=["DELETE"])
def delete_course(id):
    """
    Deleting a specific course using course id
    """
    course = Course.query.filter_by(id=id).first()
    if course is None:
        return failure_response("Course not found")
    db.session.delete(course)
    db.session.commit()
    return success_response(course.serialize())


@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Creating a user
    """
    body = json.loads(request.data)
    name = body.get("name")
    net_id = body.get("netid")

    if not name or not net_id:
        return failure_response("Missing name or netid", 400)

    new_user = User(name=name, net_id=net_id)
    db.session.add(new_user)
    db.session.commit()

    return success_response(new_user.serialize(), 201)


@app.route("/api/users/<int:id>/", methods=["GET"])
def get_specific_user(id):
    """
    Getting a specific user
    """
    user = User.query.get(id)
    if user is None:
        return failure_response("User not found", 404)

    all_courses = list(set(user.instructor_courses + user.student_courses))

    return success_response({
        "id": user.id,
        "name": user.name,
        "netid": user.net_id,
        "courses": [
            {
                "id": c.id,
                "code": c.code,
                "name": c.name
            } for c in all_courses
        ]
    })


@app.route("/api/courses/<int:id>/add/", methods=["POST"])
def add_user_to_course(id):
    """
    Adding a user to a course as a student or instructor
    """
    body = json.loads(request.data)
    user_id = body.get("user_id")
    role_type = body.get("type")

    if user_id is None or role_type not in ["student", "instructor"]:
        return failure_response("Missing or invalid user_id/type", 400)

    course = Course.query.get(id)
    user = User.query.get(user_id)

    if course is None or user is None:
        return failure_response("Course or user not found", 404)

    if role_type == "student":
        course.students.append(user)
    elif role_type == "instructor":
        course.instructors.append(user)

    db.session.commit()
    return success_response(course.serialize(), 200)


@app.route("/api/courses/<int:id>/assignment/", methods=["POST"])
def create_assignment_to_course(id):
    """
    Creates ans assignment for a course
    """
    body = json.loads(request.data)
    title = body.get("title")
    due_date = body.get("due_date")

    if title is None or due_date is None:
        return failure_response("Missing title or due_date", 400)
    
    course = Course.query.get(id)
    if course is None:
        return failure_response("Course not found", 404)
    
    new_assignment = Assignment(
        title = title,
        due_date = due_date,
        course_id = id
    )

    db.session.add(new_assignment)
    db.session.commit()

    return success_response(new_assignment.serialize(), 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
