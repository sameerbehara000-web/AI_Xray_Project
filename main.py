import pandas as pd
import os


# =========================
# FILE LOCATION
# =========================

FILE_NAME = r"C:\smart_campus_project\data\student.csv"


# =========================
# CSV COLUMNS
# =========================

COLUMNS = [
    "Student_ID",
    "Name",
    "Department",
    "Year",
    "Email",
    "Phone"
]


# =========================
# LOAD STUDENTS
# =========================

def load_students():

    if os.path.exists(FILE_NAME):

        return pd.read_csv(FILE_NAME)

    else:

        return pd.DataFrame(columns=COLUMNS)


# =========================
# SAVE STUDENTS
# =========================

def save_students(df):

    df.to_csv(
        FILE_NAME,
        index=False
    )


# =========================
# ADD STUDENT
# =========================

def add_student(data):

    df = load_students()

    # Check duplicate Student ID
    if str(data["Student_ID"]) in df["Student_ID"].astype(str).values:

        return False

    # Add new student
    df.loc[len(df)] = data

    # Save updated data
    save_students(df)

    return True


# =========================
# VIEW ALL STUDENTS
# =========================

def get_students():

    return load_students()


# =========================
# SEARCH STUDENT
# =========================

def search_student(student_id):

    df = load_students()

    result = df[
        df["Student_ID"].astype(str)
        ==
        str(student_id)
    ]

    return result


# =========================
# UPDATE STUDENT
# =========================

def update_student(student_id, updates):

    df = load_students()

    # Find student
    index = df[
        df["Student_ID"].astype(str)
        ==
        str(student_id)
    ].index

    # Student not found
    if len(index) == 0:

        return False

    # Update values
    for key, value in updates.items():

        if value != "":

            df.loc[index, key] = value

    # Save changes
    save_students(df)

    return True


# =========================
# DELETE STUDENT
# =========================

def delete_student(student_id):

    df = load_students()

    # Number of students before deletion
    old_count = len(df)

    # Remove student
    df = df[
        df["Student_ID"].astype(str)
        !=
        str(student_id)
    ]

    # Student not found
    if len(df) == old_count:

        return False

    # Save changes
    save_students(df)

    return True
