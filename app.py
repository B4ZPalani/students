from flask import Flask, jsonify, request, render_template, redirect, url_for  # type: ignore

app = Flask(__name__)

# In-memory database for student records
students = []

# Routes for rendering HTML pages
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/add')
def add_student_page():
    return render_template('add.html')

@app.route('/delete')
def delete_student_page():
    return render_template('delete.html')

# API Routes

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json

    # Validate input
    if not data.get('name') or not data.get('class') or not (0 <= data['mark1'] <= 100) or not (0 <= data['mark2'] <= 100) or not (0 <= data['mark3'] <= 100):
        return jsonify({'error': 'Invalid input data. Make sure marks are between 0 and 100 and class is valid.'}), 400

    # Add student
    student = {
        'id': len(students) + 1,
        'name': data['name'],
        'class': data['class'],
        'mark1': data['mark1'],
        'mark2': data['mark2'],
        'mark3': data['mark3'],
    }
    students.append(student)
    return jsonify({'message': 'Student added successfully!', 'student': student})

@app.route('/delete_student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    # Find student and delete if exists
    student_to_delete = next((student for student in students if student['id'] == student_id), None)
    if student_to_delete is None:
        return jsonify({'error': 'Student not found!'}), 404
    
    students.remove(student_to_delete)
    return jsonify({'message': 'Student deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
