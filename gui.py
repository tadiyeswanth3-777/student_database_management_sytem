import tkinter as tk
from tkinter import ttk
import sqlite3
import csv


# ==========================
# DATABASE CONNECTION
# ==========================

import os

from reportlab.pdfgen import canvas

def connect_db():

    print("Current Folder:", os.getcwd())
    print("Database Path:", os.path.abspath("students.db"))

    return sqlite3.connect("students.db")


def create_table():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        course TEXT,
        email TEXT,
        address TEXT,
        maths INTEGER,
        science INTEGER,
        english INTEGER,
        attendance REAL,
        grade TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Students table created")


# ==========================
# LOAD STUDENTS
# ==========================

def calculate_grade(avg):

    if avg >= 90:
        return "A+"

    elif avg >= 80:
        return "A"

    elif avg >= 70:
        return "B"

    elif avg >= 60:
        return "C"

    return "Fail"


def count_students():

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM students"
        )

        total = cursor.fetchone()[0]

        conn.close()

        total_students_label.config(
            text=f"Total Students: {total}"
        )

def load_students():

    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, name, age, course,
        email, address, maths, science, english, attendance, grade
    FROM students
    """)

    students = cursor.fetchall()

    for student in students:
        tree.insert("", "end", values=student)

    count_students()

    conn.close()


    #=======================
    # TOTAL STUDENTS COUNTER
    #=======================

    


# ==========================
# ADD STUDENT
# ==========================

def add_student():

    try:

        maths = int(maths_entry.get() or 0)
        science = int(science_entry.get() or 0)
        english = int(english_entry.get() or 0)
        attendance = float(attendance_entry.get() or 0)

        average = (maths + science + english) / 3
        grade = calculate_grade(average)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO students
        (id, name, age, course, email, address,
         maths, science, english, attendance, grade)

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            id_entry.get(),
            name_entry.get(),
            age_entry.get(),
            course_entry.get(),
            email_entry.get(),
            address_entry.get(),
            maths,
            science,
            english,
            attendance,
            grade
        ))

        conn.commit()
        conn.close()

        load_students()
        clear_fields()

        status_label.config(
            text="Student Added Successfully!"
        )

    except Exception as e:

        status_label.config(
            text=str(e)
        )



# ==========================
# SELECT STUDENT
# ==========================

def select_student(event):

    selected = tree.focus()

    if not selected:
        return

    values = tree.item(selected, "values")

    clear_fields()

    id_entry.insert(0, values[0])
    name_entry.insert(0, values[1])
    age_entry.insert(0, values[2])
    course_entry.insert(0, values[3])
    email_entry.insert(0, values[4])
    address_entry.insert(0, values[5])
    maths_entry.insert(0, values[6])
    science_entry.insert(0, values[7])
    english_entry.insert(0, values[8])
    attendance_entry.insert(0, values[9])


# ==========================
# UPDATE STUDENT
# ==========================

def update_student():

    try:

        maths = int(maths_entry.get() or 0)
        science = int(science_entry.get() or 0)
        english = int(english_entry.get() or 0)
        attendance = float(attendance_entry.get() or 0)

        average = (maths + science + english) / 3
        grade = calculate_grade(average)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE students
        SET
            name=?,
            age=?,
            course=?,
            email=?,
            address=?,
            maths=?,
            science=?,
            english=?,
            attendance=?,
            grade=?
        WHERE id=?
        """,
        (
            name_entry.get(),
            age_entry.get(),
            course_entry.get(),
            email_entry.get(),
            address_entry.get(),
            maths,
            science,
            english,
            attendance,
            grade,
            id_entry.get()
        ))

        conn.commit()
        conn.close()

        load_students()

        status_label.config(
            text="Student Updated Successfully!"
        )

    except Exception as e:

        status_label.config(
            text=str(e)
        )


# ==========================
# SEARCH STUDENT
# ==========================

def search_student():

    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM students
    WHERE id=?
    OR name LIKE ?
    """,
    (
        id_entry.get(),
        "%" + name_entry.get() + "%"
    ))

    results = cursor.fetchall()

    for row in results:
        tree.insert(
            "",
            "end",
            values=row
        )

    conn.close()



# ==========================
# DELETE STUDENT
# ==========================



def delete_student():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id_entry.get(),)
    )

    conn.commit()
    conn.close()

    load_students()

    clear_fields()

    status_label.config(
        text="Student Deleted Successfully!"
    )


def export_csv():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students"
    )

    data = cursor.fetchall()

    with open(
        "students_export.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Name",
            "Age",
            "Course",
            "Email",
            "Address",
            "Maths",
            "Science",
            "English",
            "Attendance",
            "Grade"
        ])

        writer.writerows(data)

    conn.close()

    status_label.config(
        text="CSV Exported Successfully"
    )


def generate_pdf():

    student_id = id_entry.get()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (student_id,)
    )

    student = cursor.fetchone()

    conn.close()

    if not student:
        status_label.config(
            text="Student Not Found"
        )
        return

    pdf = canvas.Canvas(
        f"report_{student_id}.pdf"
    )

    pdf.drawString(
        100,
        800,
        "Student Report"
    )

    pdf.drawString(100,760,f"ID: {student[0]}")
    pdf.drawString(100,740,f"Name: {student[1]}")
    pdf.drawString(100,720,f"Age: {student[2]}")
    pdf.drawString(100,700,f"Course: {student[3]}")
    pdf.drawString(100,680,f"Email: {student[4]}")
    pdf.drawString(100,660,f"Address: {student[5]}")
    pdf.drawString(100,640,f"Maths: {student[6]}")
    pdf.drawString(100,620,f"Science: {student[7]}")
    pdf.drawString(100,600,f"English: {student[8]}")
    pdf.drawString(100,580,f"Attendance: {student[9]}")
    pdf.drawString(100,560,f"Grade: {student[10]}")

    pdf.save()

    status_label.config(
        text="PDF Generated Successfully"
    )


# ==========================
# CLEAR FIELDS
# ==========================

def clear_fields():

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)

    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

    maths_entry.delete(0, tk.END)
    science_entry.delete(0, tk.END)
    english_entry.delete(0, tk.END)

    attendance_entry.delete(0, tk.END)

# ==========================
# GUI WINDOW
# ==========================

root = tk.Tk()

root.title("Student Management System")
root.geometry("1400x700")


# ==========================
# LABELS
# ==========================

tk.Label(root, text="Student ID").grid(row=0, column=0, padx=10, pady=5)

tk.Label(root, text="Name").grid(row=1, column=0, padx=10, pady=5)

tk.Label(root, text="Age").grid(row=2, column=0, padx=10, pady=5)

tk.Label(root, text="Course").grid(row=3, column=0, padx=10, pady=5)

tk.Label(root, text="Email").grid(row=4, column=0, padx=10, pady=5)
tk.Label(root, text="Address").grid(row=5, column=0, padx=10, pady=5)

tk.Label(root, text="Maths").grid(row=6, column=0, padx=10, pady=5)
tk.Label(root, text="Science").grid(row=7, column=0, padx=10, pady=5)
tk.Label(root, text="English").grid(row=8, column=0, padx=10, pady=5)

tk.Label(root, text="Attendance %").grid(row=9, column=0, padx=10, pady=5)


# ==========================
# ENTRY BOXES
# ==========================

id_entry = tk.Entry(root, width=30)
name_entry = tk.Entry(root, width=30)
age_entry = tk.Entry(root, width=30)
course_entry = tk.Entry(root, width=30)
email_entry = tk.Entry(root, width=30)
address_entry = tk.Entry(root, width=30)

maths_entry = tk.Entry(root, width=30)
science_entry = tk.Entry(root, width=30)
english_entry = tk.Entry(root, width=30)

attendance_entry = tk.Entry(root, width=30)

id_entry.grid(row=0, column=1)
name_entry.grid(row=1, column=1)
age_entry.grid(row=2, column=1)
course_entry.grid(row=3, column=1)
email_entry.grid(row=4, column=1)
address_entry.grid(row=5, column=1)

maths_entry.grid(row=6, column=1)
science_entry.grid(row=7, column=1)
english_entry.grid(row=8, column=1)

attendance_entry.grid(row=9, column=1)


# ==========================
# BUTTONS
# ==========================

add_btn = tk.Button(
    root,
    text="Add Student",
    command=add_student
)

add_btn.grid(row=10, column=0, pady=10)


update_btn = tk.Button(
    root,
    text="Update Student",
    command=update_student
)

update_btn.grid(row=10, column=1)


delete_btn = tk.Button(
    root,
    text="Delete Student",
    command=delete_student
)

delete_btn.grid(row=10, column=2)


search_btn = tk.Button(
    root,
    text="Search Student",
    command=search_student
)

search_btn.grid(row=10, column=3)


refresh_btn = tk.Button(
    root,
    text="Refresh",
    command=load_students
)

refresh_btn.grid(row=10, column=4)


export_btn = tk.Button(
    root,
    text="Export CSV",
    command=export_csv
)

export_btn.grid(row=10, column=5)


pdf_btn = tk.Button(
    root,
    text="Generate PDF",
    command=generate_pdf
)

pdf_btn.grid(row=10, column=6)


# ==========================
# STATUS LABEL
# ==========================

status_label = tk.Label(
    root,
    text="Ready",
    fg="green"
)

status_label.grid(row=11, column=0, columnspan=5)

total_students_label = tk.Label(
    root,
    text="Total Students: 0",
    font=("Arial", 12, "bold")
)

total_students_label.grid(
    row=11,
    column=3,
    columnspan=2
)


# ==========================
# TREEVIEW
# ==========================

tree = ttk.Treeview(
    root,
    columns=(
        "ID",
        "Name",
        "Age",
        "Course",
        "Email",
        "Address",
        "Maths",
        "Science",
        "English",
        "Attendance",
        "Grade"
    ),
    show="headings"
)

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Course", text="Course")
tree.heading("Email", text="Email")
tree.heading("Address", text="Address")
tree.heading("Maths", text="Maths")
tree.heading("Science", text="Science")
tree.heading("English", text="English")
tree.heading("Attendance", text="Attendance")
tree.heading("Grade", text="Grade")


tree.column("ID", width=80)
tree.column("Name", width=150)
tree.column("Age", width=60)
tree.column("Course", width=120)
tree.column("Email", width=180)
tree.column("Address", width=180)
tree.column("Maths", width=80)
tree.column("Science", width=80)
tree.column("English", width=80)
tree.column("Attendance", width=100)
tree.column("Grade", width=80)

tree.grid(
    row=12,
    column=0,
    columnspan=5,
    padx=10,
    pady=20
)

tree.bind(
    "<<TreeviewSelect>>",
    select_student
)

scroll_x = ttk.Scrollbar(
    root,
    orient="horizontal",
    command=tree.xview
)

tree.configure(
    xscrollcommand=scroll_x.set
)

scroll_x.grid(
    row=13,
    column=0,
    columnspan=8,
    sticky="ew"
)


# ==========================
# STARTUP
# ==========================

create_table()

load_students()

root.mainloop()