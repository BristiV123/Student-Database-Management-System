import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Student Grade Management System",
    page_icon="🎓",
    layout="wide"
)

# =====================================================
# ADMIN LOGIN
# =====================================================

def login():
    st.title("🔐 Admin Login")

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# LOGIN CHECK
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

st.sidebar.markdown("---")

if st.sidebar.button("🚪 Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

# =====================================================
# PROFESSIONAL UI
# =====================================================

st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
[data-testid="stSidebar"] {
    background-color: #0f172a;
}
[data-testid="stSidebar"] * {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# CSV FILE
# =====================================================

CSV_FILE = "student_grades.csv"

# =====================================================
# CALCULATE GRADE
# =====================================================

def calculate_grade(marks):
    if marks >= 90:
        return "A"
    elif marks >= 80:
        return "B"
    elif marks >= 70:
        return "C"
    elif marks >= 60:
        return "D"
    else:
        return "F"

# =====================================================
# LOAD DATA
# =====================================================

def load_data():
    if os.path.exists(CSV_FILE):
        data = pd.read_csv(CSV_FILE)

        required_columns = ["Roll No", "Name", "Marks", "Grade"]

        for column in required_columns:
            if column not in data.columns:
                data[column] = ""

        data = data[required_columns]

        data["Roll No"] = pd.to_numeric(data["Roll No"], errors="coerce")
        data["Marks"] = pd.to_numeric(data["Marks"], errors="coerce")

        return data

    return pd.DataFrame(columns=["Roll No", "Name", "Marks", "Grade"])

# =====================================================
# SAVE DATA
# =====================================================

def save_data(data):
    data.to_csv(CSV_FILE, index=False)

df = load_data()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🎓 Student Management")
st.sidebar.write("Academic Performance System")
st.sidebar.divider()

menu = st.sidebar.selectbox(
    "Select Option",
    [
        "🏠 Dashboard",
        "➕ Add Student",
        "✏️ Update Student",
        "🗑️ Delete Student",
        "🔍 Search Student",
        "📋 All Students",
        "📊 Statistics",
        "🏆 Ranking"
    ]
)

# =====================================================
# MAIN MENU LOGIC
# =====================================================

if menu == "🏠 Dashboard":
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        padding: 30px;
        border-radius: 18px;
        margin-bottom: 25px;
    ">
    <h1 style="color: white; margin-bottom: 5px;">🎓 Student Grade Management System</h1>
    <p style="color: white; font-size: 18px;">Academic Performance & Student Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    if not df.empty:
        total_students = len(df)
        average_marks = df["Marks"].mean()
        highest_marks = df["Marks"].max()
        lowest_marks = df["Marks"].min()
        passed_students = len(df[df["Marks"] >= 40])
        failed_students = len(df[df["Marks"] < 40])
    else:
        total_students = 0
        average_marks = 0
        highest_marks = 0
        lowest_marks = 0
        passed_students = 0
        failed_students = 0

    st.subheader("📊 Overall Performance")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👨‍🎓 Total Students", total_students)
    col2.metric("📈 Average Marks", f"{average_marks:.2f}")
    col3.metric("🏆 Highest Marks", highest_marks)
    col4.metric("📉 Lowest Marks", lowest_marks)

    col5, col6 = st.columns(2)
    col5.metric("✅ Passed Students", passed_students)
    col6.metric("❌ Failed Students", failed_students)

    st.divider()

    if not df.empty:
        st.subheader("🏆 Top 5 Students")
        top_students = df.sort_values(by="Marks", ascending=False).head(5).reset_index(drop=True)
        top_students.insert(0, "Rank", range(1, len(top_students) + 1))
        st.dataframe(top_students, use_container_width=True, hide_index=True)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Grade Distribution")
            grade_distribution = df["Grade"].value_counts().sort_index()
            st.bar_chart(grade_distribution)

        with col2:
            st.subheader("✅ Pass / Fail Analysis")
            pass_fail = pd.Series({"Passed": passed_students, "Failed": failed_students})
            st.bar_chart(pass_fail)

        st.divider()

        st.subheader("📈 Student Marks Analysis")
        marks_chart = df[["Name", "Marks"]].set_index("Name")
        st.bar_chart(marks_chart)

        st.divider()

        st.subheader("💡 Quick Insights")
        best_student = df.loc[df["Marks"].idxmax()]

        if average_marks >= 80:
            performance_message = "Excellent overall class performance! 🎉"
        elif average_marks >= 60:
            performance_message = "Good overall class performance. 👍"
        else:
            performance_message = "Students need more academic improvement. 📚"

        st.info(f"""
        🏆 **Top Student:** {best_student['Name']}

        📈 **Top Marks:** {best_student['Marks']}

        📊 **Class Average:** {average_marks:.2f}

        👨‍🎓 **Total Students:** {total_students}

        💡 **Performance:** {performance_message}
        """)

    else:
        st.info("📋 No student records available. Please add students first.")

elif menu == "➕ Add Student":
    st.header("➕ Add New Student")

    col1, col2 = st.columns(2)

    with col1:
        roll_no = st.number_input("Roll Number", min_value=1, step=1)

    with col2:
        name = st.text_input("Student Name")

    marks = st.number_input("Marks", min_value=0, max_value=100, value=0, step=1)

    if st.button("➕ Add Student", type="primary"):
        name = name.strip()

        if name == "":
            st.error("Please enter student name.")
        elif roll_no in df["Roll No"].values:
            st.error("❌ This Roll Number already exists.")
        elif name.lower() in [str(x).lower() for x in df["Name"].values]:
            st.warning("⚠️ This student name already exists.")
        else:
            grade = calculate_grade(marks)

            new_student = pd.DataFrame({
                "Roll No": [roll_no],
                "Name": [name],
                "Marks": [marks],
                "Grade": [grade]
            })

            df = pd.concat([df, new_student], ignore_index=True)
            save_data(df)

            st.success(f"✅ {name} added successfully!")
            st.info(f"Roll No: {roll_no} | Marks: {marks} | Grade: {grade}")
            st.rerun()

elif menu == "✏️ Update Student":
    st.header("✏️ Update Student")

    if df.empty:
        st.info("No students available.")
    else:
        selected_roll = st.selectbox("Select Roll Number", df["Roll No"].tolist())
        selected_student = df[df["Roll No"] == selected_roll].iloc[0]

        st.write(f"**Student Name:** {selected_student['Name']}")
        new_marks = st.number_input("New Marks", min_value=0, max_value=100, value=int(selected_student["Marks"]), step=1)

        if st.button("✏️ Update Student", type="primary"):
            new_grade = calculate_grade(new_marks)

            df.loc[df["Roll No"] == selected_roll, "Marks"] = new_marks
            df.loc[df["Roll No"] == selected_roll, "Grade"] = new_grade

            save_data(df)
            st.success("✅ Student updated successfully!")
            st.rerun()

elif menu == "🗑️ Delete Student":
    st.header("🗑️ Delete Student")

    if df.empty:
        st.info("No students available.")
    else:
        selected_roll = st.selectbox("Select Roll Number", df["Roll No"].tolist())
        selected_student = df[df["Roll No"] == selected_roll].iloc[0]

        st.write(f"Student: **{selected_student['Name']}**")
        confirm = st.checkbox("I confirm that I want to delete this student.")

        if st.button("🗑️ Delete Student", type="primary"):
            if confirm:
                df = df[df["Roll No"] != selected_roll].reset_index(drop=True)
                save_data(df)
                st.success("✅ Student deleted successfully!")
                st.rerun()
            else:
                st.warning("Please confirm deletion.")

elif menu == "🔍 Search Student":
    st.header("🔍 Search Student")
    search_type = st.radio("Search By", ["Roll Number", "Name"], horizontal=True)

    if search_type == "Roll Number":
        search_roll = st.number_input("Enter Roll Number", min_value=1, step=1)

        if st.button("🔍 Search", type="primary"):
            result = df[df["Roll No"] == search_roll]

            if result.empty:
                st.error("❌ Student not found.")
            else:
                st.dataframe(result, use_container_width=True, hide_index=True)

    else:
        search_name = st.text_input("Enter Student Name")

        if st.button("🔍 Search", type="primary"):
            result = df[df["Name"].str.contains(search_name.strip(), case=False, na=False)]

            if result.empty:
                st.error("❌ Student not found.")
            else:
                st.dataframe(result, use_container_width=True, hide_index=True)

elif menu == "📋 All Students":
    st.header("📋 All Students")

    if df.empty:
        st.info("No student records available.")
    else:
        st.success(f"Total Students: {len(df)}")
        st.dataframe(df, use_container_width=True, hide_index=True)

elif menu == "📊 Statistics":
    st.header("📊 Student Statistics")

    if df.empty:
        st.info("No student data available.")
    else:
        average = df["Marks"].mean()
        highest = df["Marks"].max()
        lowest = df["Marks"].min()
        passed = len(df[df["Marks"] >= 40])
        failed = len(df[df["Marks"] < 40])

        col1, col2, col3 = st.columns(3)
        col1.metric("📈 Average", f"{average:.2f}")
        col2.metric("🏆 Highest", highest)
        col3.metric("📉 Lowest", lowest)

        col4, col5 = st.columns(2)
        col4.metric("✅ Passed", passed)
        col5.metric("❌ Failed", failed)

        st.divider()
        st.subheader("📊 Marks Distribution")
        chart_data = df[["Name", "Marks"]].set_index("Name")
        st.bar_chart(chart_data)

elif menu == "🏆 Ranking":
    st.header("🏆 Student Ranking")

    if df.empty:
        st.info("No students available.")
    else:
        ranking = df.sort_values(by="Marks", ascending=False).reset_index(drop=True)
        ranking.insert(0, "Rank", range(1, len(ranking) + 1))
        st.dataframe(ranking, use_container_width=True, hide_index=True)

else:
    st.info("Please select a menu option.")

# =====================================================
# DOWNLOAD STUDENT REPORT
# =====================================================

st.subheader("📥 Download Report")
csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Student Report",
    data=csv_data,
    file_name="student_grade_report.csv",
    mime="text/csv"
)