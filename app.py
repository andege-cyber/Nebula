import mysql.connector
from flask import Flask, request, jsonify
import random
import string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connect to MySQL server
mydb = mysql.connector.connect(
    host="nebudatabase.cx6moumuokg2.us-east-1.rds.amazonaws.com",     #RDS endpoint
    user="admin",
    password="xyzkidsTV1",  #RDS password
    database="nebudatabase"
)

# Create a cursor object
mycursor = mydb.cursor()

# Drop the table if it exists
mycursor.execute("DROP TABLE IF EXISTS students")

# Create a table
mycursor = mydb.cursor()
mycursor.execute("""
    CREATE TABLE students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        cohort VARCHAR(50),
        attendance VARCHAR(50)
    )
""")

#Generate random student data
def generate_random_name():
    return ''.join(random.choices(string.ascii_uppercase, k=5))

def generate_random_age():
    return random.randint(18, 25)

def generate_random_email():
    name = generate_random_name().lower()
    domain = "@azubi.com"
    return f"{name}{domain}"

#Insert random names and emails into the table
records = 15
cohorts = ["CE2", "DA1", "FE3"]
attendance_options = ["Present", "Absent"]
for _ in range(records):
    random_name = generate_random_name()
    random_email = generate_random_email()
    random_cohort = random.choice(cohorts)
    random_attendance = random.choice(attendance_options)

    sql = "INSERT INTO students (name, email, cohort, attendance) VALUES (%s, %s, %s, %s)"
    mycursor = mydb.cursor()
    mycursor.execute(sql, (random_name, random_email, random_cohort, random_attendance))
    mydb.commit()

print("Student data inserted successfully!")

 #testing for health check
@app.route('/api/health-check', methods=['GET'])
def health_check():
    return jsonify({'message': 'Backend is healthy!'}), 200

#testing database connection
@app.route('/api/test-db-connection', methods=['POST'])
def test_db_connection():
    try:
        mydb.ping(reconnect=True)
        return jsonify({'message': 'Database connection successful!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#getting all students
@app.route('/api/students', methods=['GET'])
def get_all_students():
    try:
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM students")
        students = mycursor.fetchall()
        return jsonify(students), 200
    except Exception as e:
        return {'error': str(e)}, 500

#getting a student's details by email
@app.route('/api/student/<string:email>', methods=['POST'])
def get_student_details(email):
    try:
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM students WHERE email = %s", (email,))
        student = mycursor.fetchone()
        if student:
            return jsonify(student), 200
        else:
            return {'message': 'Student not found'}, 404
    except Exception as e:
        return {'error': str(e)}, 500

#getting cohort stats
@app.route('/api/cohort/stats/<string:cohort_name>', methods=['GET'])
def get_cohort_stats(cohort_name):
    try:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT COUNT(*) FROM students WHERE cohort = %s", (cohort_name,))
        total_students = mycursor.fetchone()[0]
        return {'total_students': total_students}, 200
    except Exception as e:
        return {'error': str(e)}, 500

#getting cohort attendance statistics
#
#
#
#

# Close the database connection
mycursor.close()
mydb.close()

if __name__ == '__main__':
    app.run(debug=True)

##########
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=5000)