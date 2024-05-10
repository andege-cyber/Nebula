from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLAlchemy to use MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/nebula'
db = SQLAlchemy(app)  

# Define the Student model
class Student(db.Model):
    __tablename__ = 'studentsss' # Specify the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"<Student {self.name}>"

# Create the database tables based on defined models
db.create_all()

@app.route('/api/health-check', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})


@app.route('/api/test-db-connection', methods=['POST'])
def test_db_connection():
    try:
        #db.session.execute('SELECT * FROM `studentsss` WHERE ID = 2')  # Execute a dummy query to test the connection
        db.session.execute('SELECT * FROM `studentsss` WHERE ID = 2')  # Execute a dummy query to test the connection
        db.session.commit()
        return jsonify({"status": "Connection successful"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/students', methods=['GET'])
def get_all_students():
    # Retrieve all students from the database
    students = Student.query.all()
    # Return the list of students as JSON
    return jsonify([{"id": student.id, "name": student.name, "email": student.email} for student in students])

@app.route('/api/student/<email>', methods=['GET'])
def get_student_details(email):
    # Retrieve a student by their email from the database
    student = Student.query.filter_by(email=email).first()
    if student:
        # Return student details as JSON if found
        return jsonify({"id": student.id, "name": student.name, "email": student.email})
    else:
        # Return an error message if student not found
        return jsonify({"error": "Student not found"}), 404


#double ## are codes while single ## are comments
# Add more routes for cohort stats and attendance...
##@app.route('/api/cohort/stats/<cohort_name>', methods=['GET'])
##def get_cohort_stats(cohort_name):
    # Implement logic to retrieve cohort stats
    # Return stats as JSON
  ##  return jsonify({"cohort_name": cohort_name, "stats": "some stats"})

##@app.route('/api/cohort/attendance/<cohort_name>', methods=['GET'])
##def get_cohort_attendance(cohort_name):
    # Implement logic to retrieve cohort attendance stats
    # Return attendance stats as JSON
   ## return jsonify({"cohort_name": cohort_name, "attendance": "some attendance stats"})
#double ## are codes while single ## are comments
#
#
#
#
if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
