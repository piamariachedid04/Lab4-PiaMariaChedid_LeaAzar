import json
import re
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QFormLayout, QComboBox, QTableWidget, QTableWidgetItem,QMessageBox
)
import csv
import sqlite3


# Part1
class Person:
    """
    A class to represent a person.

    Attributes:
        name (str): The name of the person.
        age (int): The age of the person.
        _email (str): The email of the person.
    """


    def __init__(self, name, age, email):
        """
        Initializes a new Person instance.

        Args:
            name (str): The name of the person.
            age (int): The age of the person.
            email (str): The email of the person.

        Raises:
            ValueError: If the age is negative or the email format is invalid.
        """
      
        self.name = name
        self.age = self.validate_age(age)
        self._email = self.validate_email(email)

    def introduce(self):
        """
        Prints an introduction message including the person's name and age.
        """
        print(f"Name is {self.name}, age is {self.age}")

    # Validation methods
    def validate_email(self, email):
        """
        Validates the provided email.

        Args:
            email (str): The email to validate.

        Returns:
            str: The validated email.

        Raises:
            ValueError: If the email format is invalid.
        """
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(email_regex, email):
            raise ValueError(f"Invalid email format: {email}")
        return email

    def validate_age(self, age):
        """
        Validates the provided age.

        Args:
            age (int): The age to validate.

        Returns:
            int: The validated age.

        Raises:
            ValueError: If the age is negative.
        """
        if age < 0:
            raise ValueError("Age cannot be negative.")
        return age

    # Serialization methods
    def save_to_file(self, filename):
        """
        Saves the person's data to a file in JSON format.

        Args:
            filename (str): The name of the file to save the data to.

        Returns:
            None
        """
        with open(filename, 'w') as f:
            json.dump(self.__dict__, f, indent=4)
        print(f"Data saved to {filename}")

    @classmethod
    def load_from_file(cls, filename):
        """
        Loads a person's data from a file in JSON format and returns a Person object.

        Args:
            filename (str): The name of the file to load the data from.

        Returns:
            Person: A new instance of Person created from the loaded data.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If there is an error decoding the JSON data.
            KeyError: If required keys are missing in the JSON data.
            ValueError: If the loaded data contains invalid values.
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        
            name = data.get('name', 'Unknown')
            age = data.get('age', 0)
            email = data.get('_email', 'unknown@example.com')

            # Optionally, validate loaded data
            if not isinstance(name, str) or not isinstance(email, str):
                raise ValueError("Invalid data type for name or email")
            return cls(name, age, email)

        except FileNotFoundError:
            print(f"File {filename} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {filename}.")
        except KeyError as e:
            print(f"Missing expected key: {e}")
        except ValueError as e:
            print(f"Value error: {e}")

class Student(Person):
    """
    A class to represent a student, inheriting from the Person class.

    Attributes:
        student_id (str): The ID of the student.
        registered_courses (list): A list of courses the student is registered in.
    """
    def __init__(self, name, age, email, student_id):
        """
        Initializes a new Student instance.

        Args:
            name (str): The name of the student.
            age (int): The age of the student.
            email (str): The email of the student.
            student_id (str): The ID of the student.
        """ 
        super().__init__(name, age, email)  # Call Person's __init__
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        """
        Registers the student for a course if not already registered.

        Args:
            course (Course): The course to register the student in.

        Returns:
            None

        Raises:
            ValueError: If the student is already registered for the course.
        """
        if course not in self.registered_courses:
            self.registered_courses.append(course)
            print("Registered for course")
        else:
            print("Course already registered")

    def save_to_file(self, filename):
        """
        Saves the student's data to a file in JSON format.

        Args:
            filename (str): The name of the file to save the data to.

        Returns:
            None
        """
        data = {
            "name": self.name,
            "age": self.age,
            "email": self._email,
            "student_id": self.student_id,
            "registered_courses": [course.course_id for course in self.registered_courses]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Student data saved to {filename}")

class Instructor(Person):
  
    """
    A class to represent an instructor, inheriting from the Person class.

    Attributes:
        instructor_id (str): The ID of the instructor.
        assigned_courses (list): A list of courses the instructor is assigned to teach.
    """

    def __init__(self, name, age, email, instructor_id):
        """
        Initializes a new Instructor instance.

        Args:
            name (str): The name of the instructor.
            age (int): The age of the instructor.
            email (str): The email of the instructor.
            instructor_id (str): The ID of the instructor.
        """
        super().__init__(name, age, email)  # Call Person's __init__
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        """
        Assigns the instructor to a course if not already assigned.

        Args:
            course (Course): The course to assign the instructor to.

        Returns:
            None

        Raises:
            ValueError: If the instructor is already assigned to the course.
        """
       
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
            print(f"Assigned to teach course: {course}")
        else:
            print(f"Already assigned to teach course: {course}")

    def save_to_file(self, filename):
        """
        Saves the instructor's data to a file in JSON format.

        Args:
            filename (str): The name of the file to save the data to.

        Returns:
            None
        """
        data = {
            "name": self.name,
            "age": self.age,
            "email": self._email,
            "instructor_id": self.instructor_id,
            "assigned_courses": [course.course_id for course in self.assigned_courses]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Instructor data saved to {filename}")

class Course:
    """
    A class to represent a course.

    Attributes:
        course_id (str): The ID of the course.
        course_name (str): The name of the course.
        instructor (Instructor): The instructor teaching the course.
        enrolled_students (list): A list of students enrolled in the course.
    """
    def __init__(self, course_id, course_name, instructor):
        """
        Initializes a new Course instance.

        Args:
            course_id (str): The ID of the course.
            course_name (str): The name of the course.
            instructor (Instructor): The instructor assigned to the course.
        """
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student):
        """
        Enrolls a student in the course if not already enrolled.

        Args:
            student (Student): The student to enroll in the course.

        Returns:
            None

        Raises:
            ValueError: If the student is already enrolled in the course.
        """
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)
            print(f"Student {student.name} enrolled in {self.course_name}")
        else:
            print("Student already enrolled")

    def save_to_file(self, filename):
        """
        Saves the course's data to a file in JSON format.

        Args:
            filename (str): The name of the file to save the data to.

        Returns:
            None
        """
        data = {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "instructor": self.instructor.name,
            "enrolled_students": [student.name for student in self.enrolled_students]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Course data saved to {filename}")

class SchoolManagementSystem(QMainWindow):

    def __init__(self):
        """
        Initializes the SchoolManagementSystem class by setting up the GUI layout
        and connecting buttons to their respective functionalities.
        """
        super().__init__()

        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.available_courses = [
            "Course 101: Introduction to Programming",
            "Course 102: Data Structures",
            "Course 201: Web Development",
            "Course 202: Database Management",
            "Course 301: Machine Learning"
        ]
        self.students = []
        self.instructors = []
        self.courses = []
        self.create_student_form()
        self.create_instructor_form()
        self.create_course_form()
        self.create_records_table()
        self.create_search_functionality()
        self.create_edit_delete_buttons()
        self.show()

    def create_student_form(self):
        """
        Creates the form for adding students, with input fields for name, age, email,
        student ID, and a course dropdown for course registration. Adds a button to 
        register the student.
        """
        student_form = QFormLayout()

        self.student_name_input = QLineEdit()
        self.student_age_input = QLineEdit()
        self.student_email_input = QLineEdit()
        self.student_id_input = QLineEdit()

        student_form.addRow(QLabel("Name:"), self.student_name_input)
        student_form.addRow(QLabel("Age:"), self.student_age_input)
        student_form.addRow(QLabel("Email:"), self.student_email_input)
        student_form.addRow(QLabel("Student ID:"), self.student_id_input)

        self.course_dropdown = QComboBox()
        self.course_dropdown.addItems(self.available_courses)
        student_form.addRow(QLabel("Select Course:"), self.course_dropdown)

  
        add_student_button = QPushButton("Add Student and Register Course")
        add_student_button.clicked.connect(self.add_student)
        student_form.addRow(add_student_button)

        self.layout.addLayout(student_form)

    def create_instructor_form(self):
        """
        Creates the form for adding instructors, with input fields for name, age, email,
        and instructor ID. Adds a dropdown for selecting a course to assign to the instructor
        and a button to assign the course.
        """
        instructor_form = QFormLayout()
        self.instructor_name_input = QLineEdit()
        self.instructor_age_input = QLineEdit()
        self.instructor_email_input = QLineEdit()
        self.instructor_id_input = QLineEdit()

        instructor_form.addRow(QLabel("Name:"), self.instructor_name_input)
        instructor_form.addRow(QLabel("Age:"), self.instructor_age_input)
        instructor_form.addRow(QLabel("Email:"), self.instructor_email_input)
        instructor_form.addRow(QLabel("Instructor ID:"), self.instructor_id_input)

        self.instructor_course_dropdown = QComboBox()
        self.instructor_course_dropdown.addItems(self.available_courses)
        instructor_form.addRow(QLabel("Select Course to Assign:"), self.instructor_course_dropdown)

        assign_course_button = QPushButton("Assign Course to Instructor")
        assign_course_button.clicked.connect(self.assign_course)
        instructor_form.addRow(assign_course_button)

        self.layout.addLayout(instructor_form)

    def create_course_form(self):
        """
        Creates the form for adding courses, with input fields for course ID, course name,
        and instructor. Adds a button to register the new course.
        """
        course_form = QFormLayout()

        self.course_id_input = QLineEdit()
        self.course_name_input = QLineEdit()
        self.course_instructor_input = QLineEdit()

        course_form.addRow(QLabel("Course ID:"), self.course_id_input)
        course_form.addRow(QLabel("Course Name:"), self.course_name_input)
        course_form.addRow(QLabel("Instructor Name:"), self.course_instructor_input)

        add_course_button = QPushButton("Add Course")
        add_course_button.clicked.connect(self.add_course)
        course_form.addRow(add_course_button)

        self.layout.addLayout(course_form)

    def create_records_table(self):
        """
        Creates a QTableWidget to display records of students, instructors, and courses
        in the system.
        """
     
        self.records_table = QTableWidget()
        self.records_table.setColumnCount(5)  
        self.records_table.setHorizontalHeaderLabels(["Type", "Name", "Details", "Email/ID", "Registered Courses"])

        self.layout.addWidget(self.records_table)

    def create_search_functionality(self):
        """
        Adds a search input and button to allow users to search through records
        by name, ID, or course.
        """
        search_form = QFormLayout()

        # Search input
        self.search_input = QLineEdit()
        search_form.addRow(QLabel("Search (by Name, ID, or Course):"), self.search_input)

        # Search button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_records)
        search_form.addRow(search_button)

        self.layout.addLayout(search_form)

    def create_edit_delete_buttons(self):
        """
        Adds buttons for editing and deleting selected records from the system.
        """
        edit_delete_form = QFormLayout()

        # Edit button
        edit_button = QPushButton("Edit Selected Record")
        edit_button.clicked.connect(self.edit_record)
        edit_delete_form.addRow(edit_button)

        # Delete button
        delete_button = QPushButton("Delete Selected Record")
        delete_button.clicked.connect(self.delete_record)
        edit_delete_form.addRow(delete_button)

        self.layout.addLayout(edit_delete_form)

    def add_student(self):
        """
        Adds a new student to the system by collecting data from the input fields
        and registering them for a selected course in the database.

        Raises:
        -------
        sqlite3.IntegrityError
            If there is an error inserting the student or registering the course.
        """
        name = self.student_name_input.text()
        age = int(self.student_age_input.text())
        email = self.student_email_input.text()
        student_id = self.student_id_input.text()
        selected_course = self.course_dropdown.currentText()

        
        conn = sqlite3.connect('school_management_system.db')
        cursor = conn.cursor()

        try:
            # Insert student into the database
            cursor.execute('''
            INSERT INTO Students (name, age, email, student_id) VALUES (?, ?, ?, ?)
            ''', (name, age, email, student_id))

           
            course_id = self.get_course_id_from_name(selected_course.split(":")[0].strip())

         
            student_db_id = cursor.lastrowid
            cursor.execute('''
            INSERT INTO Registrations (student_id, course_id) VALUES (?, ?)
            ''', (student_db_id, course_id))

            conn.commit()

            QMessageBox.information(self, "Success", f"Student {name} registered for {selected_course} successfully.")

        except sqlite3.IntegrityError as e:
            QMessageBox.critical(self, "Error", f"Error inserting student or registering course: {e}")
        finally:
            conn.close()

        self.student_name_input.clear()
        self.student_age_input.clear()
        self.student_email_input.clear()
        self.student_id_input.clear()
        self.update_records_table()
        
    def get_course_id_from_name(self, course_name):
        conn = sqlite3.connect('school_management_system.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM Courses WHERE course_name = ?', (course_name,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None
        
    def assign_course(self):
        """
        Assigns an instructor to a course by collecting data from the input fields
        and updating the course in the database with the assigned instructor.

        Raises:
        -------
        sqlite3.IntegrityError
            If there is an error assigning the course.
        """
        name = self.instructor_name_input.text()
        age = int(self.instructor_age_input.text())
        email = self.instructor_email_input.text()
        instructor_id = self.instructor_id_input.text()
        selected_course = self.instructor_course_dropdown.currentText()
        conn = sqlite3.connect('school_management_system.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
            INSERT INTO Instructors (name, age, email, instructor_id) VALUES (?, ?, ?, ?)
            ''', (name, age, email, instructor_id))

            course_id = self.get_course_id_from_name(selected_course.split(":")[0].strip())

            instructor_db_id = cursor.lastrowid

            cursor.execute('''
            UPDATE Courses SET instructor_id = ? WHERE id = ?
            ''', (instructor_db_id, course_id))

            conn.commit()
            QMessageBox.information(self, "Success", f"Instructor {name} assigned to {selected_course} successfully.")

        except sqlite3.IntegrityError as e:
            QMessageBox.critical(self, "Error", f"Error assigning course: {e}")
        finally:
            conn.close()
        self.instructor_name_input.clear()
        self.instructor_age_input.clear()
        self.instructor_email_input.clear()
        self.instructor_id_input.clear()


    def add_course(self):
        """
        Adds a new course to the system by collecting data from the input fields
        and inserting the course into the database.

        Raises:
        -------
        sqlite3.IntegrityError
            If there is an error adding the course.
        """
        course_id = self.course_id_input.text()
        course_name = self.course_name_input.text()
        instructor_id = self.course_instructor_input.text()  # Use instructor_id

        conn = sqlite3.connect('school_management_system.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO Courses (course_id, course_name, instructor_id)
                VALUES (?, ?, ?)
            ''', (course_id, course_name, instructor_id)) 
            conn.commit()

            QMessageBox.information(self, 'Success', 'Course added successfully!')

            self.update_records_table()

        except sqlite3.IntegrityError as e:
            QMessageBox.critical(self, "Error", f"Error adding course: {e}")
        finally:
            conn.close()

        # Clear the input fields so they are ready for the next entry
        self.course_id_input.clear()
        self.course_name_input.clear()
        self.course_instructor_input.clear()

    def update_records_table(self):
        """
        Updates the records table by fetching the latest student, instructor,
        and course data from the database and displaying it in the table.
        """
   
        self.records_table.setRowCount(0)

        conn = sqlite3.connect('school_management_system.db')
        cursor = conn.cursor()

        cursor.execute('SELECT name, student_id, email FROM Students')
        students = cursor.fetchall()
        for student in students:
            row_position = self.records_table.rowCount()
            self.records_table.insertRow(row_position)
            self.records_table.setItem(row_position, 0, QTableWidgetItem('Student'))
            self.records_table.setItem(row_position, 1, QTableWidgetItem(student[0]))  # name
            self.records_table.setItem(row_position, 2, QTableWidgetItem(f'ID: {student[1]}'))  # student ID
            self.records_table.setItem(row_position, 3, QTableWidgetItem(student[2]))  # email
            self.records_table.setItem(row_position, 4, QTableWidgetItem(''))  # empty for course

        cursor.execute('SELECT name, instructor_id, email FROM Instructors')
        instructors = cursor.fetchall()
        for instructor in instructors:
            row_position = self.records_table.rowCount()
            self.records_table.insertRow(row_position)
            self.records_table.setItem(row_position, 0, QTableWidgetItem('Instructor'))
            self.records_table.setItem(row_position, 1, QTableWidgetItem(instructor[0]))  # name
            self.records_table.setItem(row_position, 2, QTableWidgetItem(f'ID: {instructor[1]}'))  # instructor ID
            self.records_table.setItem(row_position, 3, QTableWidgetItem(instructor[2]))  # email
            self.records_table.setItem(row_position, 4, QTableWidgetItem(''))  # empty for course

        cursor.execute('SELECT course_name, course_id FROM Courses')
        courses = cursor.fetchall()
        for course in courses:
            row_position = self.records_table.rowCount()
            self.records_table.insertRow(row_position)
            self.records_table.setItem(row_position, 0, QTableWidgetItem('Course'))
            self.records_table.setItem(row_position, 1, QTableWidgetItem(course[0]))  # course name
            self.records_table.setItem(row_position, 2, QTableWidgetItem(f'ID: {course[1]}'))  # course ID
            self.records_table.setItem(row_position, 3, QTableWidgetItem(''))  # empty for instructor
            self.records_table.setItem(row_position, 4, QTableWidgetItem(''))  # empty for student registrations

        # Close the connection
        conn.close()

    def search_records(self):
            """
            Searches the student, instructor, and course records based on a query
            (name, ID, or course) entered in the search input field.
            """
            query = self.search_input.text().lower()

            # Clear the table before searching
            self.records_table.setRowCount(0)

            # Search students in the database
            self.cursor.execute("SELECT name, student_id, email, course FROM students WHERE LOWER(name) LIKE ? OR LOWER(student_id) LIKE ? OR LOWER(email) LIKE ?", 
                                (f"%{query}%", f"%{query}%", f"%{query}%"))
            students = self.cursor.fetchall()

            for student in students:
                row_position = self.records_table.rowCount()
                self.records_table.insertRow(row_position)
                self.records_table.setItem(row_position, 0, QTableWidgetItem('Student'))
                self.records_table.setItem(row_position, 1, QTableWidgetItem(student[0]))  # name
                self.records_table.setItem(row_position, 2, QTableWidgetItem(f'ID: {student[1]}'))  # student ID
                self.records_table.setItem(row_position, 3, QTableWidgetItem(student[2]))  # email
                self.records_table.setItem(row_position, 4, QTableWidgetItem(student[3]))  # course

            # Search instructors in the database
            self.cursor.execute("SELECT name, instructor_id, email, course FROM instructors WHERE LOWER(name) LIKE ? OR LOWER(instructor_id) LIKE ? OR LOWER(email) LIKE ?", 
                                (f"%{query}%", f"%{query}%", f"%{query}%"))
            instructors = self.cursor.fetchall()

            for instructor in instructors:
                row_position = self.records_table.rowCount()
                self.records_table.insertRow(row_position)
                self.records_table.setItem(row_position, 0, QTableWidgetItem('Instructor'))
                self.records_table.setItem(row_position, 1, QTableWidgetItem(instructor[0]))  # name
                self.records_table.setItem(row_position, 2, QTableWidgetItem(f'ID: {instructor[1]}'))  # instructor ID
                self.records_table.setItem(row_position, 3, QTableWidgetItem(instructor[2]))  # email
                self.records_table.setItem(row_position, 4, QTableWidgetItem(instructor[3]))  # course

            # Search courses in the database
            self.cursor.execute("SELECT course_name, course_id, instructor_name FROM courses WHERE LOWER(course_name) LIKE ? OR LOWER(course_id) LIKE ? OR LOWER(instructor_name) LIKE ?", 
                                (f"%{query}%", f"%{query}%", f"%{query}%"))
            courses = self.cursor.fetchall()

            for course in courses:
                row_position = self.records_table.rowCount()
                self.records_table.insertRow(row_position)
                self.records_table.setItem(row_position, 0, QTableWidgetItem('Course'))
                self.records_table.setItem(row_position, 1, QTableWidgetItem(course[0]))  # course name
                self.records_table.setItem(row_position, 2, QTableWidgetItem(f'ID: {course[1]}'))  # course ID
                self.records_table.setItem(row_position, 3, QTableWidgetItem(course[2]))  # instructor name
                self.records_table.setItem(row_position, 4, QTableWidgetItem(''))  # no registered courses for courses

    def edit_record(self):
        """
        Edits the selected record in the records table.

        Based on the selected row in the table, this method fetches the current data of the student, 
        instructor, or course and updates the corresponding record in the database.

        Raises:
        -------
        ValueError:
            If no row is selected.
        """
        selected_row = self.records_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Edit Error", "Please select a record to edit.")
            return

        # Get current data of the selected record
        record_type = self.records_table.item(selected_row, 0).text()
        name = self.records_table.item(selected_row, 1).text()
        details = self.records_table.item(selected_row, 2).text()
        email_id = self.records_table.item(selected_row, 3).text()
        registered_courses = self.records_table.item(selected_row, 4).text()

        # Edit fields based on type of record
        if record_type == "Student":
            # Get new data for student
            new_name = self.student_name_input.text()
            new_age = self.student_age_input.text()
            new_email = self.student_email_input.text()
            new_course = self.course_dropdown.currentText()

            # Update student record in the database
            student_id = details.split(": ")[1]  # Extract student ID
            self.cursor.execute('''
                UPDATE students 
                SET name = ?, email = ?, course = ? 
                WHERE student_id = ?''', (new_name, new_email, new_course, student_id))
            self.conn.commit()

        elif record_type == "Instructor":
            # Get new data for instructor
            new_name = self.instructor_name_input.text()
            new_age = self.instructor_age_input.text()
            new_email = self.instructor_email_input.text()
            new_course = self.instructor_course_dropdown.currentText()

            # Update instructor record in the database
            instructor_id = details.split(": ")[1]  # Extract instructor ID
            self.cursor.execute('''
                UPDATE instructors 
                SET name = ?, email = ?, course = ? 
                WHERE instructor_id = ?''', (new_name, new_email, new_course, instructor_id))
            self.conn.commit()

        elif record_type == "Course":
            # Get new data for course
            new_course_id = self.course_id_input.text()
            new_course_name = self.course_name_input.text()
            new_instructor_name = self.course_instructor_input.text()

            # Update course record in the database
            self.cursor.execute('''
                UPDATE courses 
                SET course_name = ?, instructor_name = ? 
                WHERE course_id = ?''', (new_course_name, new_instructor_name, new_course_id))
            self.conn.commit()

        # Refresh the table after editing
        self.update_records_table()

    def delete_record(self):
        """
        Deletes the selected record from the records table and database.

        Raises:
        -------
        ValueError:
            If no row is selected for deletion.
        sqlite3.Error:
            If an error occurs during the deletion in the database.
        """
        selected_row = self.records_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Delete Error", "Please select a record to delete.")
            return
        record_type = self.records_table.item(selected_row, 0).text()
        record_id = self.records_table.item(selected_row, 2).text() 

        record_id = record_id.split(': ')[-1]  

        conn = sqlite3.connect('school_management_system.db')
        cursor = conn.cursor()

        try:
            if record_type == "Student":
                cursor.execute("DELETE FROM Students WHERE student_id = ?", (record_id,))
                QMessageBox.information(self, "Success", f"Student with ID {record_id} deleted successfully.")

            elif record_type == "Instructor":
                cursor.execute("DELETE FROM Instructors WHERE instructor_id = ?", (record_id,))
                QMessageBox.information(self, "Success", f"Instructor with ID {record_id} deleted successfully.")

            elif record_type == "Course":
                cursor.execute("DELETE FROM Courses WHERE course_id = ?", (record_id,))
                QMessageBox.information(self, "Success", f"Course with ID {record_id} deleted successfully.")

            conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:

            conn.close()

       
        self.update_records_table()

    def save_data_to_file(self):
        """
        Saves all student, instructor, and course data to a JSON file.

        This method allows the user to save the current state of the school management system to a file,
        which can be reloaded later.

        Raises:
        -------
        IOError:
            If there is an error during file writing.
        """
        self.cursor.execute("SELECT * FROM students")
        students = self.cursor.fetchall()
        
        self.cursor.execute("SELECT * FROM instructors")
        instructors = self.cursor.fetchall()

        self.cursor.execute("SELECT * FROM courses")
        courses = self.cursor.fetchall()

        data = {
            "students": [
                {"student_id": student[0], "name": student[1], "age": student[2], "email": student[3], "course": student[4]}
                for student in students
            ],
            "instructors": [
                {"instructor_id": instructor[0], "name": instructor[1], "age": instructor[2], "email": instructor[3]}
                for instructor in instructors
            ],
            "courses": [
                {"course_id": course[0], "name": course[1], "instructor": course[2]}
                for course in courses
            ]
        }

        filename, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "JSON Files (*.json);;All Files (*)")
        if filename:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "Data Saved", "Data has been saved successfully.")

    def load_data_from_file(self):
        """
        Loads student, instructor, and course data from a JSON file.

        This method allows the user to load previously saved data back into the system.

        Raises:
        -------
        IOError:
            If there is an error during file reading.
        """
        filename, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "JSON Files (*.json);;All Files (*)")
        if filename:
            with open(filename, 'r') as f:
                data = json.load(f)
                
                # Load students
                self.students = [Student(**student_data) for student_data in data.get("students", [])]
                # Load instructors
                self.instructors = [Instructor(**instructor_data) for instructor_data in data.get("instructors", [])]
                # Load courses
                self.courses = [Course(**course_data) for course_data in data.get("courses", [])]
                
                # Update the records table
                self.update_records_table()
                QMessageBox.information(self, "Data Loaded", "Data has been loaded successfully.")

    def export_to_csv(self):
        """
        Exports all student, instructor, and course data to a CSV file.

        Raises:
        -------
        IOError:
            If there is an error during file writing.
        """
        filename, _ = QFileDialog.getSaveFileName(self, "Export Data", "", "CSV Files (*.csv);;All Files (*)")
        if filename:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write Students
                writer.writerow(['Students'])
                writer.writerow(['Name', 'Age', 'Email', 'Student ID', 'Registered Courses'])
                for student in self.students:
                    writer.writerow([student.name, student.age, student._email, student.student_id, ', '.join(student.registered_courses)])
                writer.writerow([])  # Blank line to separate sections
                
                # Write Instructors
                writer.writerow(['Instructors'])
                writer.writerow(['Name', 'Age', 'Email', 'Instructor ID', 'Assigned Courses'])
                for instructor in self.instructors:
                    writer.writerow([instructor.name, instructor.age, instructor._email, instructor.instructor_id, ', '.join(instructor.assigned_courses)])
                writer.writerow([])  # Blank line to separate sections
                
                # Write Courses
                writer.writerow(['Courses'])
                writer.writerow(['Course ID', 'Course Name', 'Instructor', 'Enrolled Students'])
                for course in self.courses:
                    writer.writerow([course.course_id, course.course_name, course.instructor.name, ', '.join(student.name for student in course.enrolled_students)])
            
            QMessageBox.information(self, "Data Exported", "Data has been exported successfully to CSV.")

    def create_menu(self):
        """
        Create the menu bar for the application with options for saving, loading, and exporting data.

        This method sets up a menu bar with a "File" menu that contains the following actions:
        
        - **Save Data**: Saves the current data to a file in JSON format.
        - **Load Data**: Loads data from a JSON file into the system.
        - **Export to CSV**: Exports the current data to a CSV file.

        The menu is added to the application's menu bar.
        """
        # Create menu bar
        menu_bar = self.menuBar()
        
        # Create File menu
        file_menu = menu_bar.addMenu("File")
        
        # Add Save Data action
        save_action = QAction("Save Data", self)
        save_action.triggered.connect(self.save_data_to_file)
        file_menu.addAction(save_action)

        # Add Load Data action
        load_action = QAction("Load Data", self)
        load_action.triggered.connect(self.load_data_from_file)
        file_menu.addAction(load_action)

        # Add Export to CSV action
        export_action = QAction("Export to CSV", self)
        export_action.triggered.connect(self.export_to_csv)
        file_menu.addAction(export_action)
    def validate_input(self, name, age, email, student_or_instructor_id):
        """
        Validate user input for adding or editing a record.

        :param name: The name of the student or instructor. Should contain only alphabetic characters and spaces.
        :type name: str
        :param age: The age of the student or instructor. Must be a number between 5 and 120.
        :type age: str
        :param email: The email address of the student or instructor. Must be a valid email format.
        :type email: str
        :param student_or_instructor_id: The unique ID of the student or instructor. Must be alphanumeric.
        :type student_or_instructor_id: str

        :returns: True if all validations pass, otherwise False.
        :rtype: bool

        This method validates the following:
        - The name contains only alphabetic characters and spaces.
        - The age is a valid number between 5 and 120.
        - The email is in a valid email format.
        - The student or instructor ID is alphanumeric.
        
        If any validation fails, a warning message is displayed and the function returns False.
        """
        if not name.replace(" ", "").isalpha():
            QMessageBox.warning(self, "Invalid Input", "Name should only contain alphabetic characters and spaces.")
            return False

        # Validate Age (between 5 and 120)
        if not age.isdigit() or not (5 <= int(age) <= 120):
            QMessageBox.warning(self, "Invalid Input", "Age should be a valid number between 5 and 120.")
            return False

        # Validate Email using regex
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(email_regex, email):
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid email address.")
            return False

        # Validate Student/Instructor ID (should be alphanumeric)
        if not student_or_instructor_id.isalnum():
            QMessageBox.warning(self, "Invalid Input", "ID should be alphanumeric.")
            return False

        # If all validations pass
        return True

    def add_instructor(self):
        """
        Add a new instructor to the system.

        This method collects the input fields for the instructor's name, age, email, and ID. 
        It then validates the input using `validate_input`. If validation passes, 
        it creates an Instructor object and appends it to the instructors list.

        :raises: A warning message if any of the inputs are invalid.

        :returns: None
        """
        name = self.name_input.text()
        age = self.age_input.text()
        email = self.email_input.text()
        instructor_id = self.instructor_id_input.text()

        if self.validate_input(name, age, email, instructor_id):
            # Proceed with adding the instructor
            instructor = Instructor(name, int(age), email, instructor_id)
            self.instructors.append(instructor)
            QMessageBox.information(self, "Success", "Instructor added successfully!")


def create_database():
    """
    Create the database schema for the school management system.

    This function creates four tables:
    
    - **Students**: Stores student details (id, name, age, email, student_id).
    - **Instructors**: Stores instructor details (id, name, age, email, instructor_id).
    - **Courses**: Stores course details (id, course_id, course_name, instructor_id).
    - **Registrations**: Stores registration details (id, student_id, course_id) with a unique constraint 
      ensuring that each student can only register for a course once.

    :raises sqlite3.Error: If there is any issue with executing SQL commands.
    """
    conn = sqlite3.connect('school_management_system.db')
    cursor = conn.cursor()

    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS Students ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL, 
        age INTEGER NOT NULL CHECK(age >= 5 AND age <= 120), 
        email TEXT NOT NULL UNIQUE, 
        student_id TEXT NOT NULL UNIQUE 
    ) 
    ''')

    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS Instructors ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL, 
        age INTEGER NOT NULL CHECK(age >= 5 AND age <= 120), 
        email TEXT NOT NULL UNIQUE, 
        instructor_id TEXT NOT NULL UNIQUE 
    ) 
    ''')

    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS Courses ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        course_id TEXT NOT NULL UNIQUE, 
        course_name TEXT NOT NULL, 
        instructor_id INTEGER, 
        FOREIGN KEY (instructor_id) REFERENCES Instructors(id) 
    ) 
    ''')

    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS Registrations ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        student_id INTEGER, 
        course_id INTEGER, 
        FOREIGN KEY (student_id) REFERENCES Students(id), 
        FOREIGN KEY (course_id) REFERENCES Courses(id), 
        UNIQUE (student_id, course_id) 
    ) 
    ''')

    conn.commit()
    conn.close()

def insert_student(name, age, email, student_id):
    """
    Insert a new student into the Students table.

    :param name: Name of the student.
    :type name: str
    :param age: Age of the student.
    :type age: int
    :param email: Email of the student.
    :type email: str
    :param student_id: Unique identifier for the student.
    :type student_id: str

    :raises sqlite3.Error: If there is any issue inserting the student into the database.
    """
    try:
        conn = sqlite3.connect('school_management_system.db')
        cursor = conn.cursor()
        cursor.execute(''' 
        INSERT INTO Students (name, age, email, student_id) VALUES (?, ?, ?, ?) 
        ''', (name, age, email, student_id))
        conn.commit()
    except sqlite3.Error as e:
        QMessageBox.warning(None, "Database Error", str(e))
    finally:
        conn.close()

def get_students():
    """
    Retrieve all students from the Students table.

    :return: A list of tuples, where each tuple represents a student (name, age, email, student_id).
    :rtype: list of tuple
    """
    conn = sqlite3.connect('school_management_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Students')
    students = cursor.fetchall()
    conn.close()
    return students

def update_student(student_id, name, age, email):
    """
    Update an existing student's information in the database.

    :param student_id: The student's unique identifier.
    :type student_id: str
    :param name: Updated name of the student.
    :type name: str
    :param age: Updated age of the student.
    :type age: int
    :param email: Updated email of the student.
    :type email: str

    :raises sqlite3.Error: If there is any issue updating the student's record.
    """
    try:
        conn = sqlite3.connect('school_management_system.db')
        cursor = conn.cursor()
        cursor.execute(''' 
        UPDATE Students SET name = ?, age = ?, email = ? WHERE student_id = ? 
        ''', (name, age, email, student_id))
        conn.commit()
    except sqlite3.Error as e:
        QMessageBox.warning(None, "Database Error", str(e))
    finally:
        conn.close()

def delete_student(student_id):
    """
    Delete a student from the Students table based on student ID.

    :param student_id: The unique identifier of the student to delete.
    :type student_id: str

    :raises sqlite3.Error: If there is any issue deleting the student's record.
    """
    try:
        conn = sqlite3.connect('school_management_system.db')
        cursor = conn.cursor()
        cursor.execute(''' 
        DELETE FROM Students WHERE student_id = ? 
        ''', (student_id,))
        conn.commit()
    except sqlite3.Error as e:
        QMessageBox.warning(None, "Database Error", str(e))
    finally:
        conn.close()

def create_records_table(self):
    """
    Create a table widget in the UI for displaying records.

    This method creates a QTableWidget that will be used to display records 
    such as students, instructors, and courses in the system's GUI.

    :return: None
    """
    self.records_table = QTableWidget()
    self.layout.addWidget(self.records_table)


def load_students_into_table(self):
    """
    Load all student data from the database and display it in the records table.

    This method retrieves all student data from the database and populates 
    the records table with it.

    :return: None
    """
    conn = sqlite3.connect('school_management_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, age, email, student_id FROM Students')
    students = cursor.fetchall()
    conn.close()

    # Set table headers
    self.records_table.setColumnCount(4)
    self.records_table.setHorizontalHeaderLabels(["Name", "Age", "Email", "Student ID"])
    self.records_table.setRowCount(len(students))

    # Insert data into table
    for row_idx, student in enumerate(students):
        for col_idx, data in enumerate(student):
            self.records_table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

def update_records_table(self):
    """
    Update the records table with the latest data from the database.

    This method clears the current contents of the table and reloads all 
    the data (students, instructors, and courses) from the database.

    :raises sqlite3.Error: If there is any issue retrieving data from the database.
    """
    self.records_table.clearContents()
    self.records_table.setRowCount(0)  

    try:
        conn = sqlite3.connect('school_management_system.db')
        cursor = conn.cursor()

        cursor.execute('SELECT course_id, course_name, instructor_id FROM Courses')
        courses = cursor.fetchall()

        cursor.execute('SELECT name, age, email, student_id FROM Students')
        students = cursor.fetchall()

        cursor.execute('SELECT name, age, email, instructor_id FROM Instructors')
        instructors = cursor.fetchall()

        for student in students:
            row_position = self.records_table.rowCount()
            self.records_table.insertRow(row_position)
            for col_num, data in enumerate(student):
                self.records_table.setItem(row_position, col_num, QTableWidgetItem(str(data)))

        for instructor in instructors:
            row_position = self.records_table.rowCount()
            self.records_table.insertRow(row_position)
            for col_num, data in enumerate(instructor):
                self.records_table.setItem(row_position, col_num, QTableWidgetItem(str(data)))

        for course in courses:
            row_position = self.records_table.rowCount()
            self.records_table.insertRow(row_position)
            for col_num, data in enumerate(course):
                self.records_table.setItem(row_position, col_num, QTableWidgetItem(str(data)))

    except sqlite3.Error as e:
        QMessageBox.warning(None, "Database Error", str(e))
    finally:
        conn.close()

if __name__ == "__main__":
   
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    sys.exit(app.exec_())
#pia