import sqlite3
from datetime import datetime


def connect_db():
    return sqlite3.connect("students.db")


def calculate_grade(average):
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    else:
        return "Fail"


def add_student():
    conn = connect_db()
    cursor = conn.cursor()

    student_id = input("Enter Student ID: ")
    name = input("Enter Student Name: ")

    age = input("Enter Student Age: ")
    if not age.isdigit():
        print("Age must be a number!")
        conn.close()
        return

    course = input("Enter Student Course: ")

    email = input("Enter Student Email: ")
    if "@gmail.com" not in email:
        print("Please enter a valid Gmail address!")
        conn.close()
        return

    address = input("Enter Student Address: ")

    maths = int(input("Enter Maths Marks: "))
    science = int(input("Enter Science Marks: "))
    english = int(input("Enter English Marks: "))

    attendance = float(input("Enter Attendance Percentage: "))

    total = maths + science + english
    average = total / 3

    grade = calculate_grade(average)

    admission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("""
        INSERT INTO students
        (
            id,
            name,
            age,
            course,
            email,
            address,
            admission_date,
            maths_marks,
            science_marks,
            english_marks,
            total_marks,
            average_marks,
            grade,
            attendance
        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,

        (
            student_id,
            name,
            age,
            course,
            email,
            address,
            admission_date,
            maths,
            science,
            english,
            total,
            average,
            grade,
            attendance
        ))

        conn.commit()
        print("Student added successfully!")

    except sqlite3.IntegrityError:
        print("Student ID already exists!")

    conn.close()


def view_students():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        print("No students found.")
    else:
        print("\n========== STUDENT RECORDS ==========")

        for student in students:

            print(f"""
ID           : {student[0]}
Name         : {student[1]}
Age          : {student[2]}
Course       : {student[3]}
Email        : {student[4]}
Address      : {student[5]}

Maths        : {student[7]}
Science      : {student[8]}
English      : {student[9]}

Total        : {student[10]}
Average      : {student[11]:.2f}
Grade        : {student[12]}

Attendance   : {student[13]}%

Admission    : {student[6]}
------------------------------------------
""")

    conn.close()


def search_student():
    conn = connect_db()
    cursor = conn.cursor()

    student_id = input("Enter Student ID: ")

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student:

        print(f"""
ID           : {student[0]}
Name         : {student[1]}
Age          : {student[2]}
Course       : {student[3]}
Email        : {student[4]}
Address      : {student[5]}

Maths        : {student[7]}
Science      : {student[8]}
English      : {student[9]}

Total        : {student[10]}
Average      : {student[11]:.2f}
Grade        : {student[12]}

Attendance   : {student[13]}%
""")

    else:
        print("Student not found.")

    conn.close()


def update_student():
    conn = connect_db()
    cursor = conn.cursor()

    student_id = input("Enter Student ID to update: ")

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (student_id,)
    )

    student = cursor.fetchone()

    if not student:
        print("Student not found.")
        conn.close()
        return

    name = input("Enter New Name: ")

    age = input("Enter New Age: ")
    if not age.isdigit():
        print("Age must be numeric!")
        conn.close()
        return

    course = input("Enter New Course: ")

    email = input("Enter New Email: ")
    if "@gmail.com" not in email:
        print("Invalid Gmail address!")
        conn.close()
        return

    address = input("Enter New Address: ")

    maths = int(input("Enter Maths Marks: "))
    science = int(input("Enter Science Marks: "))
    english = int(input("Enter English Marks: "))

    attendance = float(input("Enter Attendance Percentage: "))

    total = maths + science + english
    average = total / 3

    grade = calculate_grade(average)

    cursor.execute("""
    UPDATE students
    SET
    name=?,
    age=?,
    course=?,
    email=?,
    address=?,
    maths_marks=?,
    science_marks=?,
    english_marks=?,
    total_marks=?,
    average_marks=?,
    grade=?,
    attendance=?

    WHERE id=?
    """,

    (
        name,
        age,
        course,
        email,
        address,
        maths,
        science,
        english,
        total,
        average,
        grade,
        attendance,
        student_id
    ))

    conn.commit()
    conn.close()

    print("Student updated successfully!")


def delete_student():
    conn = connect_db()
    cursor = conn.cursor()

    student_id = input("Enter Student ID: ")

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (student_id,)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Student deleted successfully!")
    else:
        print("Student not found.")

    conn.close()


def count_students():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")

    count = cursor.fetchone()[0]

    print(f"\nTotal Students: {count}")

    conn.close()


while True:

    print("\n========== STUDENT MANAGEMENT SYSTEM ==========")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Count Students")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        update_student()

    elif choice == "5":
        delete_student()

    elif choice == "6":
        count_students()

    elif choice == "7":
        print("Exiting program...")
        break

    else:
        print("Invalid choice!")