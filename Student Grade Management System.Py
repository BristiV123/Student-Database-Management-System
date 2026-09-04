
# Initialization dictionary
import csv


# Initialization dictionary
student_grades = {}

def get_valid_marks():
    while True:
        try:
            marks = int(input("Enter student marks (0-100) = "))

            if 0 <= marks <= 100:
                return marks
            else:
                print("Marks must be between 0 and 100!")

        except ValueError:
            print("Please enter a valid number!")
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



# Add a new student
def add_student(name, marks):
    if name in student_grades:
        print(f"{name} already exists!")
        print("Please use the Update option to change the marks.")
        return

    grade = calculate_grade(marks)

    student_grades[name] = {
        "marks": marks,
        "grade": grade
    }

    print(f"Added {name} with marks {marks} and grade {grade}")

    print(f"Added {name} with marks {marks} and grade {grade}")

# Update a student
def update_student(name, marks):
    if name in student_grades:
        grade = calculate_grade(marks)

        student_grades[name] = {
            "marks": marks,
            "grade": grade
        }

        print(f"{name}'s marks have been updated to {marks}")
        print(f"New grade: {grade}")
    else:
        print(f"{name} is not found!")

# Delete a student
def delete_student(name):
    if name in student_grades:
        confirm = input(
            f"Are you sure you want to delete {name}? (y/n): "
        ).lower()

        if confirm == "y":
            del student_grades[name]
            print(f"{name} has been successfully deleted")
        else:
            print("Delete operation cancelled.")

    else:
        print(f"{name} is not found!")

     # Search student
def search_student(name):
    if name in student_grades:
        data = student_grades[name]

        print("\n----- Student Found -----")
        print(f"Name  : {name}")
        print(f"Marks : {data['marks']}")
        print(f"Grade : {data['grade']}")
    else:
        print(f"{name} is not found!")

  # Show statistics
def show_statistics():
    if not student_grades:
        print("No students found/added")
        return

    marks_list = []

    for data in student_grades.values():
        marks_list.append(data["marks"])

    average = sum(marks_list) / len(marks_list)
    highest = max(marks_list)
    lowest = min(marks_list)

    passed = 0
    failed = 0

    for data in student_grades.values():
        if data["marks"] >= 40:
            passed += 1
        else:
            failed += 1

    print("\n----- Student Statistics -----")
    print(f"Total Students : {len(student_grades)}")
    print(f"Average Marks  : {average:.2f}")
    print(f"Highest Marks  : {highest}")
    print(f"Lowest Marks   : {lowest}")
    print(f"Passed Students: {passed}")
    print(f"Failed Students: {failed}")         

# View all students
def display_all_students():
    if student_grades:
        for name, data in student_grades.items():
            print(
                f"{name} : Marks = {data['marks']}, "
                f"Grade = {data['grade']}"
            )


            def show_statistics():
              if not student_grades:
                 print("No students found/added")
        return

    marks_list = []

    for data in student_grades.values():
        marks_list.append(data["marks"])

    average = sum(marks_list) / len(marks_list)
    highest = max(marks_list)
    lowest = min(marks_list)

    passed = 0
    failed = 0

    for data in student_grades.values():
        if data["marks"] >= 40:
            passed += 1
        else:
            failed += 1

    print("\n----- Student Statistics -----")
    print(f"Total Students : {len(student_grades)}")
    print(f"Average Marks  : {average:.2f}")
    print(f"Highest Marks  : {highest}")
    print(f"Lowest Marks   : {lowest}")
    print(f"Passed Students: {passed}")
    print(f"Failed Students: {failed}")


    def search_student(name):
     if name in student_grades:
        data = student_grades[name]

        print("\n----- Student Found -----")
        print(f"Name  : {name}")
        print(f"Marks : {data['marks']}")
        print(f"Grade : {data['grade']}")
     else:
        print(f"{name} is not found!")


def load_from_csv():
    try:
        with open("student_grades.csv", "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row["Name"]
                marks = int(row["Marks"])
                grade = row["Grade"]

                student_grades[name] = {
                    "marks": marks,
                    "grade": grade
                }

        print("Student data loaded successfully!")

    except FileNotFoundError:
        print("No previous student data found. Starting fresh.")   
    with open("student_grades.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Name", "Marks", "Grade"])

        for name, data in student_grades.items():
            writer.writerow([
                name,
                data["marks"],
                data["grade"]
            ])

    print("Student data saved successfully!")
def show_rankings():
    if not student_grades:
        print("No students found/added")
        return

    sorted_students = sorted(
        student_grades.items(),
        key=lambda item: item[1]["marks"],
        reverse=True
    )

    print("\n----- Student Rankings -----")

    rank = 1

    for name, data in sorted_students:
        print(
            f"{rank}. {name} - "
            f"Marks: {data['marks']} - "
            f"Grade: {data['grade']}"
        )
        rank += 1 

def load_from_csv():
    try:
        with open("student_grades.csv", "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row["Name"]
                marks = int(row["Marks"])
                grade = row["Grade"]

                student_grades[name] = {
                    "marks": marks,
                    "grade": grade
                }

        print("Student data loaded successfully!")

    except FileNotFoundError:
        print("No previous student data found. Starting fresh.")      

# Main function
def main():
    while True:
        print("\nStudent Grades Management System")
        print("1. Add a new student")
        print("2. Update a student")
        print("3. Delete a student")
        print("4. View all students")
        print("5. Show statistics")
        print("6. Search student")
        print("7. Show ranking")
        print("8.Exit")

        while True:
            try:
                choice = int(input("Enter your choice = "))

                if 1 <= choice <= 8:
                    break
                else:
                    print("Please enter a number between 1 and 8.")

            except ValueError:
                print("Invalid input! Please enter a number.")
        if choice == 1:
            name = input("Enter student name = ")
            marks =  get_valid_marks()
            add_student(name, marks)

        elif choice == 2:
            name = input("Enter student name = ")
            marks = get_valid_marks()
            update_student(name, marks)

        elif choice == 3:
            name = input("Enter student name = ")
            delete_student(name)

        elif choice == 4:
            display_all_students()

        elif choice == 5:
            show_statistics()

        elif choice == 6:
            name = input("Enter student name to search = ")
            search_student(name)
        elif choice == 7:
            show_rankings()

        elif choice == 8:
             save_to_csv()
             print("Closing the program...")
             break

        

        else:
            print("Invalid choice")


# Run the program
if __name__ == "__main__":
    load_from_csv()
    main()