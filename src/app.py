from flask import Flask, jsonify, request

app = Flask(__name__)

# Przykładowa baza danych w pamięci
students = [
    {"id": 1, "name": "Jan", "age": 22},
    {"id": 2, "name": "Anna", "age": 23},
]

# READ - Pobierz wszystkich studentów
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

# READ - Pobierz konkretnego studenta po ID
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((student for student in students if student["id"] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"message": "Student not found"}), 404

# CREATE - Dodaj nowego studenta
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    new_student = {
        "id": students[-1]["id"] + 1 if students else 1,
        "name": data["name"],
        "age": data["age"]
    }
    students.append(new_student)
    return jsonify(new_student), 201

# UPDATE - Aktualizuj dane studenta po ID
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = next((student for student in students if student["id"] == student_id), None)
    if student:
        data = request.get_json()
        student.update({
            "name": data.get("name", student["name"]),
            "age": data.get("age", student["age"])
        })
        return jsonify(student)
    return jsonify({"message": "Student not found"}), 404

# DELETE - Usuń studenta po ID
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    students = [student for student in students if student["id"] != student_id]
    return jsonify({"message": "Student deleted"}), 200

# Metoda zwracająca szczegóły żądania
@app.route('/info', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def request_info():
    response_data = {
        "method": request.method,
        "headers": dict(request.headers),
        "args": request.args,
        "json": request.get_json(silent=True)
    }
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(debug=True)
