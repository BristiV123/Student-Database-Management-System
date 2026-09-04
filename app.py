import streamlit as st
import pandas as pd
import os

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Student Grade Management System",
    page_icon="🎓",
    layout="wide"
)

# =====================================================
# PROFESSIONAL UI STYLING
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

h1, h2, h3 {
    color: #0f172a;
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

        required_columns = [
            "Name",
            "Marks",
            "Grade"
        ]

        for column in required_columns:

            if column not in data.columns:
                data[column] = ""

        return data[required_columns]

    return pd.DataFrame(
        columns=[
            "Name",
            "Marks",
            "Grade"
        ]
    )


# =====================================================
# SAVE DATA
# =====================================================

def save_data(data):

    data.to_csv(
        CSV_FILE,
        index=False
    )


# Load student data
df = load_data()


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

st.sidebar.title("🎓 Student Management")

st.sidebar.write(
    "Academic Performance System"
)

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
# DASHBOARD
# =====================================================

if menu == "🏠 Dashboard":

    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#2563eb,#7c3aed);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
    ">

    <h1 style="color:white;">
    🎓 Student Grade Management System
    </h1>

    <p style="font-size:18px;">
    Professional Student Management & Academic Performance Dashboard
    </p>

    </div>
    """, unsafe_allow_html=True)


    # Statistics

    if not df.empty:

        total_students = len(df)

        average_marks = df["Marks"].mean()

        highest_marks = df["Marks"].max()

        lowest_marks = df["Marks"].min()

        passed_students = len(
            df[df["Marks"] >= 40]
        )

        failed_students = len(
            df[df["Marks"] < 40]
        )

    else:

        total_students = 0

        average_marks = 0

        highest_marks = 0

        lowest_marks = 0

        passed_students = 0

        failed_students = 0


    # Dashboard cards

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👨‍🎓 Total Students",
        total_students
    )

    col2.metric(
        "📈 Average Marks",
        f"{average_marks:.2f}"
    )

    col3.metric(
        "🏆 Highest Marks",
        highest_marks
    )

    col4.metric(
        "✅ Passed Students",
        passed_students
    )


    col5, col6 = st.columns(2)

    col5.metric(
        "📉 Lowest Marks",
        lowest_marks
    )

    col6.metric(
        "❌ Failed Students",
        failed_students
    )


    st.divider()


    # =================================================
    # TOP 5 STUDENTS
    # =================================================

    if not df.empty:

        st.subheader("🏆 Top 5 Students")

        top_students = (
            df.sort_values(
                by="Marks",
                ascending=False
            )
            .head(5)
        )

        st.dataframe(
            top_students,
            use_container_width=True,
            hide_index=True
        )


        # =================================================
        # GRADE DISTRIBUTION
        # =================================================

        st.subheader("📊 Grade Distribution")

        grade_distribution = (
            df["Grade"]
            .value_counts()
            .sort_index()
        )

        st.bar_chart(
            grade_distribution
        )


        # =================================================
        # PASS / FAIL ANALYSIS
        # =================================================

        st.subheader("✅ Pass / Fail Analysis")

        pass_fail = pd.Series({
            "Passed": passed_students,
            "Failed": failed_students
        })

        st.bar_chart(
            pass_fail
        )


        # =================================================
        # STUDENT MARKS
        # =================================================

        st.subheader("📈 Student Marks")

        marks_chart = (
            df[
                ["Name", "Marks"]
            ]
            .set_index("Name")
        )

        st.bar_chart(
            marks_chart
        )


    else:

        st.info(
            "No student records available."
        )


# =====================================================
# ADD STUDENT
# =====================================================

elif menu == "➕ Add Student":

    st.header("➕ Add New Student")

    name = st.text_input(
        "Student Name"
    )

    marks = st.number_input(
        "Marks",
        min_value=0,
        max_value=100,
        value=0,
        step=1
    )


    if st.button(
        "➕ Add Student",
        type="primary"
    ):

        name = name.strip()

        if name == "":

            st.error(
                "Please enter student name."
            )

        elif name.lower() in [
            str(x).lower()
            for x in df["Name"].values
        ]:

            st.warning(
                "This student already exists."
            )

        else:

            grade = calculate_grade(
                marks
            )

            new_student = pd.DataFrame({

                "Name": [name],

                "Marks": [marks],

                "Grade": [grade]

            })


            df = pd.concat(
                [
                    df,
                    new_student
                ],
                ignore_index=True
            )


            save_data(df)


            st.success(
                f"✅ {name} added successfully!"
            )

            st.info(
                f"Marks: {marks} | Grade: {grade}"
            )

            st.rerun()


# =====================================================
# UPDATE STUDENT
# =====================================================

elif menu == "✏️ Update Student":

    st.header("✏️ Update Student")

    if df.empty:

        st.info(
            "No students available."
        )

    else:

        name = st.selectbox(
            "Select Student",
            df["Name"].tolist()
        )


        current_marks = int(
            df.loc[
                df["Name"] == name,
                "Marks"
            ].iloc[0]
        )


        new_marks = st.number_input(
            "Enter New Marks",
            min_value=0,
            max_value=100,
            value=current_marks,
            step=1
        )


        if st.button(
            "✏️ Update Student",
            type="primary"
        ):

            grade = calculate_grade(
                new_marks
            )


            df.loc[
                df["Name"] == name,
                "Marks"
            ] = new_marks


            df.loc[
                df["Name"] == name,
                "Grade"
            ] = grade


            save_data(df)


            st.success(
                f"✅ {name} updated successfully!"
            )

            st.info(
                f"New Grade: {grade}"
            )

            st.rerun()


# =====================================================
# DELETE STUDENT
# =====================================================

elif menu == "🗑️ Delete Student":

    st.header("🗑️ Delete Student")

    if df.empty:

        st.info(
            "No students available."
        )

    else:

        name = st.selectbox(
            "Select Student",
            df["Name"].tolist()
        )


        confirm = st.checkbox(
            "I confirm that I want to delete this student."
        )


        if st.button(
            "🗑️ Delete Student",
            type="primary"
        ):

            if confirm:

                df = df[
                    df["Name"] != name
                ].reset_index(drop=True)


                save_data(df)


                st.success(
                    f"✅ {name} deleted successfully!"
                )

                st.rerun()

            else:

                st.warning(
                    "Please confirm deletion."
                )


# =====================================================
# SEARCH STUDENT
# =====================================================

elif menu == "🔍 Search Student":

    st.header("🔍 Search Student")

    search_name = st.text_input(
        "Enter Student Name"
    )


    if st.button(
        "🔍 Search",
        type="primary"
    ):

        if search_name.strip() == "":

            st.warning(
                "Please enter a student name."
            )

        else:

            result = df[
                df["Name"].str.contains(
                    search_name.strip(),
                    case=False,
                    na=False
                )
            ]


            if result.empty:

                st.error(
                    "❌ Student not found."
                )

            else:

                st.success(
                    f"✅ {len(result)} student(s) found."
                )

                st.dataframe(
                    result,
                    use_container_width=True,
                    hide_index=True
                )


# =====================================================
# ALL STUDENTS
# =====================================================

elif menu == "📋 All Students":

    st.header("📋 All Students")

    if df.empty:

        st.info(
            "No student records available."
        )

    else:

        st.success(
            f"Total Students: {len(df)}"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# =====================================================
# STATISTICS
# =====================================================

elif menu == "📊 Statistics":

    st.header("📊 Student Statistics")

    if df.empty:

        st.info(
            "No student data available."
        )

    else:

        average = df["Marks"].mean()

        highest = df["Marks"].max()

        lowest = df["Marks"].min()

        passed = len(
            df[df["Marks"] >= 40]
        )

        failed = len(
            df[df["Marks"] < 40]
        )


        col1, col2, col3 = st.columns(3)

        col1.metric(
            "📈 Average",
            f"{average:.2f}"
        )

        col2.metric(
            "🏆 Highest",
            highest
        )

        col3.metric(
            "📉 Lowest",
            lowest
        )


        col4, col5 = st.columns(2)

        col4.metric(
            "✅ Passed",
            passed
        )

        col5.metric(
            "❌ Failed",
            failed
        )


        st.divider()


        st.subheader(
            "📊 Marks Distribution"
        )

        chart_data = (
            df[
                ["Name", "Marks"]
            ]
            .set_index("Name")
        )

        st.bar_chart(
            chart_data
        )


# =====================================================
# RANKING
# =====================================================

elif menu == "🏆 Ranking":

    st.header("🏆 Student Ranking")

    if df.empty:

        st.info(
            "No students available."
        )

    else:

        ranking = (
            df.sort_values(
                by="Marks",
                ascending=False
            )
            .reset_index(drop=True)
        )


        ranking.insert(
            0,
            "Rank",
            range(
                1,
                len(ranking) + 1
            )
        )


        st.dataframe(
            ranking,
            use_container_width=True,
            hide_index=True
        )