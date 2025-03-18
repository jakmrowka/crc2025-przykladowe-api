from flask import Flask, jsonify, request
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s"
)

app = Flask(__name__)

students = [
    {"id": 1, "name": "Jan", "age": 22},
    {"id": 2, "name": "Anna", "age": 23},
]


@app.route("/students", methods=["GET"])
def get_students():
    logging.info("GET request - all students")
    return jsonify(students)


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    logging.info(f"GET request - student ID: {student_id}")
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student)

    logging.warning(f"Student ID {student_id} not found")
    return jsonify({"message": "Student not found"}), 404


@app.route("/students", methods=["POST"])
def create_student():
    data = request.get_json()
    new_student = {
        "id": students[-1]["id"] + 1 if students else 1,
        "name": data["name"],
        "age": data["age"],
    }
    students.append(new_student)
    logging.info(f"POST request - student created: {new_student}")
    return jsonify(new_student), 201


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        data = request.get_json()
        student.update(
            {
                "name": data.get("name", student["name"]),
                "age": data.get("age", student["age"]),
            }
        )
        logging.info(f"PUT request - student updated: {student}")
        return jsonify(student)

    logging.warning(f"PUT request - student ID {student_id} not found")
    return jsonify({"message": "Student not found"}), 404


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    logging.info(f"DELETE request - student ID {student_id} deleted")
    return jsonify({"message": "Student deleted"}), 200


@app.route("/info", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route("/info/<path:param>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def request_info(param=None):
    response_data = {
        "method": request.method,
        "headers": dict(request.headers),
        "args": request.args,
        "json": request.get_json(silent=True),
        "param": param,
    }
    logging.info(f"INFO request - param: {param}")
    return jsonify(response_data), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000) #http://127.0.0.1:5000