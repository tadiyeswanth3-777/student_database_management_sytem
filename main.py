import sqlite3
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

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


def connect_db():
    return sqlite3.connect("students.db")


def add_student():
    conn = connect_db()
    cursor = conn.cursor()

    student_id = input("Enter Student ID: ")
    name = input("Enter Student Name: ")
    age = input("Enter Student Age: ")
    course = input("Enter Student Course: ")
    email = input("Enter Student Email: ")
    address = input("Enter Student Address: ")

    admission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("""
        INSERT INTO students
        (id, name, age, course, email, address, admission_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (student_id, name, age, course, email, address, admission_date))

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
        print("\n===== Student Records =====")
        for student in students:
            print(f"""
ID             : {student[0]}
Name           : {student[1]}
Age            : {student[2]}
Course         : {student[3]}
Email          : {student[4]}
Address        : {student[5]}
Admission Date : {student[6]}
-----------------------------------
""")

    conn.close()


def search_student():
    conn = connect_db()
    cursor = conn.cursor()

    student_id = input("Enter Student ID to search: ")

    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student:
        print(f"""
ID             : {student[0]}
Name           : {student[1]}
Age            : {student[2]}
Course         : {student[3]}
Email          : {student[4]}
Address        : {student[5]}
Admission Date : {student[6]}
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

    new_name = input("Enter New Name: ")
    new_age = input("Enter New Age: ")
    new_course = input("Enter New Course: ")
    new_email = input("Enter New Email: ")
    new_address = input("Enter New Address: ")

    cursor.execute("""
    UPDATE students
    SET name=?, age=?, course=?, email=?, address=?
    WHERE id=?
    """, (
        new_name,
        new_age,
        new_course,
        new_email,
        new_address,
        student_id
    ))

    conn.commit()
    conn.close()

    print("Student updated successfully!")


def delete_student():
    conn = connect_db()
    cursor = conn.cursor()

    student_id = input("Enter Student ID to delete: ")

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

    print(f"Total Students: {count}")

    conn.close()

def generate_pdf_report():

    conn = connect_db()
    cursor = conn.cursor()

    student_id = input("Enter Student ID: ")

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (student_id,)
    )

    student = cursor.fetchone()

    if not student:
        print("Student not found.")
        conn.close()
        return

    pdf_file = f"report_{student_id}.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "Student Report Card",
        styles["Title"]
    )

    content.append(title)
    content.append(Spacer(1, 12))

    content.append(
        Paragraph(f"<b>ID:</b> {student[0]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"<b>Name:</b> {student[1]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"<b>Age:</b> {student[2]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"<b>Course:</b> {student[3]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"<b>Email:</b> {student[4]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"<b>Address:</b> {student[5]}", styles["Normal"])
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(f"<b>Maths:</b> {student[7]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"<b>Science:</b> {student[8]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"<b>English:</b> {student[9]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"<b>Total:</b> {student[10]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"<b>Average:</b> {student[11]:.2f}", styles["Normal"])
    )

    content.append(
        Paragraph(f"<b>Grade:</b> {student[12]}", styles["Normal"])
    )

    content.append(
        Paragraph(f"<b>Attendance:</b> {student[13]}%", styles["Normal"])
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            f"<b>Admission Date:</b> {student[6]}",
            styles["Normal"]
        )
    )

    doc.build(content)

    conn.close()

    print(f"PDF Report Generated: {pdf_file}")


while True:
    print("\n========== Student Management System ==========")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Count Students")
    print("7. Generate PDF Reports")
    print("8. Exit")

    choice = input("Enter your choice (1-8): ")

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
        generate_pdf_report()
        
    elif choice == "8":
        print("Exiting program...")
        break

    else:
        print("Invalid choice!")