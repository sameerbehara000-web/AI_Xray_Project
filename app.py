import streamlit as st
import pandas as pd
import os


# =========================================================
# FILE LOCATION
# =========================================================

FILE_NAME = r"C:\Users\MSS44\Videos\gitam_projecrt\data\student.csv"


# =========================================================
# COLUMNS
# =========================================================

COLUMNS = [
    "Student_ID",
    "Name",
    "Department",
    "Year",
    "Email",
    "Phone"
]


# =========================================================
# LOAD STUDENTS
# =========================================================

def load_students():

    if os.path.exists(FILE_NAME):

        return pd.read_csv(FILE_NAME)

    else:

        return pd.DataFrame(columns=COLUMNS)


# =========================================================
# SAVE STUDENTS
# =========================================================

def save_students(df):

    # Make sure the data folder exists
    os.makedirs(os.path.dirname(FILE_NAME), exist_ok=True)

    df.to_csv(
        FILE_NAME,
        index=False
    )


# =========================================================
# ADD STUDENT
# =========================================================

def add_student(data):

    df = load_students()

    # Check duplicate Student ID
    if str(data["Student_ID"]) in df["Student_ID"].astype(str).values:

        return False

    # Add student
    df.loc[len(df)] = data

    # Save
    save_students(df)

    return True


# =========================================================
# SEARCH STUDENT
# =========================================================

def search_student(student_id):

    df = load_students()

    result = df[
        df["Student_ID"].astype(str)
        ==
        str(student_id)
    ]

    return result


# =========================================================
# UPDATE STUDENT
# =========================================================

def update_student(student_id, updates):

    df = load_students()

    index = df[
        df["Student_ID"].astype(str)
        ==
        str(student_id)
    ].index

    # Student not found
    if len(index) == 0:

        return False

    # Update fields
    for key, value in updates.items():

        if value != "":

            df.loc[index, key] = value

    save_students(df)

    return True


# =========================================================
# DELETE STUDENT
# =========================================================

def delete_student(student_id):

    df = load_students()

    old_count = len(df)

    df = df[
        df["Student_ID"].astype(str)
        !=
        str(student_id)
    ]

    # Student not found
    if len(df) == old_count:

        return False

    save_students(df)

    return True


# =========================================================
# STREAMLIT PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🎓 Student Management System")

st.write(
    "Manage student records using Streamlit and Pandas."
)


# =========================================================
# SIDEBAR MENU
# =========================================================

st.sidebar.title("Menu")

option = st.sidebar.selectbox(
    "Select Operation",
    [
        "Home",
        "Add Student",
        "View Students",
        "Search Student",
        "Update Student",
        "Delete Student"
    ]
)


# =========================================================
# HOME
# =========================================================

if option == "Home":

    st.header("Welcome!")

    st.write(
        "Use the menu on the left to manage student records."
    )

    df = load_students()

    st.metric(
        "Total Students",
        len(df)
    )

    if len(df) > 0:

        st.subheader("Student Records")

        st.dataframe(
            df,
            use_container_width=True
        )


# =========================================================
# ADD STUDENT
# =========================================================

elif option == "Add Student":

    st.header("➕ Add Student")

    student_id = st.text_input(
        "Student ID",
        placeholder="Example: STU102"
    )

    name = st.text_input(
        "Name",
        placeholder="Enter student name"
    )

    department = st.selectbox(
        "Department",
        [
            "CSE",
            "IT",
            "ECE",
            "EEE",
            "CE",
            "ME"
        ]
    )

    year = st.selectbox(
        "Year",
        [1, 2, 3, 4]
    )

    email = st.text_input(
        "Email",
        placeholder="student@campus.edu"
    )

    phone = st.text_input(
        "Phone",
        placeholder="Enter phone number"
    )

    if st.button("Add Student"):

        if (
            student_id == ""
            or name == ""
            or email == ""
            or phone == ""
        ):

            st.warning(
                "Please fill all required fields."
            )

        else:

            data = {
                "Student_ID": student_id,
                "Name": name,
                "Department": department,
                "Year": year,
                "Email": email,
                "Phone": phone
            }

            success = add_student(data)

            if success:

                st.success(
                    "Student added successfully!"
                )

            else:

                st.error(
                    "Student ID already exists!"
                )


# =========================================================
# VIEW STUDENTS
# =========================================================

elif option == "View Students":

    st.header("👨‍🎓 All Students")

    df = load_students()

    if len(df) == 0:

        st.info("No student records found.")

    else:

        st.write(
            f"Total Students: {len(df)}"
        )

        st.dataframe(
            df,
            use_container_width=True
        )


# =========================================================
# SEARCH STUDENT
# =========================================================

elif option == "Search Student":

    st.header("🔍 Search Student")

    student_id = st.text_input(
        "Enter Student ID",
        placeholder="Example: STU001"
    )

    if st.button("Search"):

        if student_id == "":

            st.warning(
                "Please enter a Student ID."
            )

        else:

            result = search_student(student_id)

            if len(result) == 0:

                st.error(
                    "Student not found."
                )

            else:

                st.success(
                    "Student found!"
                )

                st.dataframe(
                    result,
                    use_container_width=True
                )


# =========================================================
# UPDATE STUDENT
# =========================================================

elif option == "Update Student":

    st.header("✏️ Update Student")

    student_id = st.text_input(
        "Student ID",
        placeholder="Example: STU101"
    )

    st.subheader("Enter New Information")

    name = st.text_input(
        "New Name"
    )

    department = st.selectbox(
        "New Department",
        [
            "",
            "CSE",
            "IT",
            "ECE",
            "EEE",
            "CE",
            "ME"
        ]
    )

    year = st.selectbox(
        "New Year",
        ["", 1, 2, 3, 4]
    )

    email = st.text_input(
        "New Email"
    )

    phone = st.text_input(
        "New Phone"
    )

    if st.button("Update Student"):

        if student_id == "":

            st.warning(
                "Please enter Student ID."
            )

        else:

            updates = {
                "Name": name,
                "Department": department,
                "Year": year,
                "Email": email,
                "Phone": phone
            }

            success = update_student(
                student_id,
                updates
            )

            if success:

                st.success(
                    "Student updated successfully!"
                )

                # Show updated student
                result = search_student(
                    student_id
                )

                st.dataframe(
                    result,
                    use_container_width=True
                )

            else:

                st.error(
                    "Student not found."
                )


# =========================================================
# DELETE STUDENT
# =========================================================

elif option == "Delete Student":

    st.header("🗑️ Delete Student")

    student_id = st.text_input(
        "Enter Student ID",
        placeholder="Example: STU101"
    )

    if st.button("Delete Student"):

        if student_id == "":

            st.warning(
                "Please enter Student ID."
            )

        else:

            success = delete_student(
                student_id
            )

            if success:

                st.success(
                    "Student deleted successfully!"
                )

            else:

                st.error(
                    "Student not found."
                )
