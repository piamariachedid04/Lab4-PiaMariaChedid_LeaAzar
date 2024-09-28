import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json

class Student:
    """
    Represents a student with personal and academic details.

    :param name: The name of the student.
    :type name: str
    :param age: The age of the student.
    :type age: int
    :param email: The email address of the student.
    :type email: str
    :param student_id: The unique ID assigned to the student.
    :type student_id: str
    :param courses: A list of courses the student is enrolled in.
    :type courses: list
    """
    
    def __init__(self, name, age, email, student_id, courses):
        """
        Constructor method to initialize a student object.
        """
        self.name = name
        self.age = age
        self.email = email
        self.student_id = student_id
        self.courses = courses

class Instructor:
    """
    Represents an instructor with personal and academic details.

    :param name: The name of the instructor.
    :type name: str
    :param age: The age of the instructor.
    :type age: int
    :param email: The email address of the instructor.
    :type email: str
    :param instructor_id: The unique ID assigned to the instructor.
    :type instructor_id: str
    :param courses: A list of courses the instructor is teaching.
    :type courses: list
    """
    
    def __init__(self, name, age, email, instructor_id, courses):
        """
        Constructor method to initialize an instructor object.
        """
        self.name = name
        self.age = age
        self.email = email
        self.instructor_id = instructor_id
        self.courses = courses


class Course:
    """
    Represents a course with its ID, name, instructor, and enrolled students.

    :param course_id: The unique ID of the course.
    :type course_id: str
    :param course_name: The name of the course.
    :type course_name: str
    :param instructor: The instructor assigned to the course, defaults to None.
    :type instructor: :class:`Instructor`, optional
    :param students: A list of students enrolled in the course, defaults to an empty list.
    :type students: list, optional
    """
    
    def __init__(self, course_id, course_name, instructor=None, students=None):
        """
        Constructor method to initialize a course object.
        """
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.students = students if students else []

    def add_student(self, student):
        """
        Adds a student to the course.

        :param student: The student to add to the course.
        :type student: :class:`Student`
        """
        self.students.append(student)
class ManagementApp(tk.Tk):
    """
    Represents a school management system application built using Tkinter.

    This class is a subclass of :class:`tk.Tk` and provides an interface to manage
    courses and student data within the application.

    :ivar course_list: A list of available courses in the system.
    :vartype course_list: list of :class:`Course`
    :ivar data_records: A list to store student data records.
    :vartype data_records: list
    """
    
    def __init__(self):
        """
        Constructor method to initialize the management application.

        Initializes the main window with title, size, and background color, and sets up
        initial courses and student records.
        """
        super().__init__()
        self.title("School Management System")
        self.geometry("800x600")
        self.configure(bg="pink")

        self.course_list = [
            Course("Id1", "Math 101"),
            Course("id2", "Physics 201"),
            Course("id3", "Chemistry 301")
        ]

        self.data_records = []

        self.setupUI()


    def setupUI(self):
        """
        Sets up the user interface (UI) components for the School Management System application.

        This method creates the following UI elements:
        
        - A tree view table for displaying data records with columns for ID, Name, Type, Email, Age, and Courses/Instructor/Students.
        - A search bar for querying records.
        - Multiple buttons for adding, editing, saving, loading, exporting data, and assigning courses.

        The layout and styles are configured for better visual appearance and functionality.

        The components created include:

        - **Treeview table**: Displays records in a table format.
        - **Search field**: An entry widget for searching records.
        - **Buttons**: Various buttons for interacting with the data (e.g., Add Student, Add Instructor, Save Data, Export to CSV, etc.).

        :ivar data_table: A table widget to display student, instructor, or course data.
        :vartype data_table: :class:`ttk.Treeview`
        :ivar search_field: An entry widget for inputting search queries.
        :vartype search_field: :class:`tk.Entry`
        """
        bg_color = "pink"
        border_color = "#FF1493"

        # Create a frame for the table
        tree_frame = tk.Frame(self, bg=border_color, bd=2)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Define columns for the table
        columns = ("ID", "Name", "Type", "Email", "Age", "Courses/Instructor/Students")
        self.data_table = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Set up headings and column widths
        for col in columns:
            self.data_table.heading(col, text=col)
            self.data_table.column(col, width=120)
        self.data_table.pack(fill=tk.BOTH, expand=True)

        # Style the table
        style = ttk.Style()
        style.configure("Treeview", borderwidth=0, relief='flat', background="white", foreground="black", fieldbackground="white")

        # Create a search frame
        search_frame = tk.Frame(self, bg=bg_color)
        search_frame.pack(pady=10, fill=tk.X)

        # Create a search field and button
        self.search_field = tk.Entry(search_frame)
        self.search_field.grid(row=0, column=0, padx=5, sticky='ew')

        search_btn = tk.Button(search_frame, text="Search", command=self.search_records)
        search_btn.grid(row=0, column=1, padx=5, sticky='ew')

        search_frame.columnconfigure(0, weight=1)
        search_frame.columnconfigure(1, weight=1)

        # Create a frame for buttons
        button_frame = tk.Frame(self, bg=bg_color)
        button_frame.pack(pady=10, fill=tk.X)

        button_width = 20  # Standard width for buttons

        # Add buttons to the UI
        add_student_btn = tk.Button(button_frame, text="Add Student", command=self.show_student_form, width=button_width)
        add_student_btn.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        add_course_btn = tk.Button(button_frame, text="Add Course", command=self.show_course_form, width=button_width)
        add_course_btn.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        save_btn = tk.Button(button_frame, text="Save Data", command=self.save_records, width=button_width)
        save_btn.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')

        edit_btn = tk.Button(button_frame, text="Edit Data", command=self.edit_records, width=button_width)
        edit_btn.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')

        assigncourse_btn = tk.Button(button_frame, text="Assign Course to Instructor", command=self.assign, width=button_width)
        assigncourse_btn.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')

        # Add buttons for the second column
        add_instructor_btn = tk.Button(button_frame, text="Add Instructor", command=self.show_instructor_form, width=button_width)
        add_instructor_btn.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        load_btn = tk.Button(button_frame, text="Load Data", command=self.load_records, width=button_width)
        load_btn.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

        export_csv_btn = tk.Button(button_frame, text="Export to CSV", command=self.export_csv, width=button_width)
        export_csv_btn.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')

        register_btn = tk.Button(button_frame, text="Register a Course", command=self.register_course, width=button_width)
        register_btn.grid(row=3, column=1, padx=5, pady=5, sticky='nsew')

        delete_btn = tk.Button(button_frame, text="Delete Data", command=self.delete, width=button_width)
        delete_btn.grid(row=4, column=1, padx=5, pady=5, sticky='nsew')

        # Configure column weights to make the columns equal in width
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

    def refresh_data_table(self):
        """
        Refreshes the data displayed in the Treeview table.

        This method clears the current data from the table and repopulates it with updated
        information from `self.data_records`. The records may be of different types (e.g., Course or other types), 
        and the method formats the data accordingly before inserting it into the table.

        For courses, it combines the instructor and students information. For other types, 
        it lists the associated courses.

        :ivar data_table: The table widget displaying the records.
        :vartype data_table: :class:`ttk.Treeview`
        :ivar data_records: A list of dictionaries containing student, course, or instructor records.
        :vartype data_records: list of dict
        """
        # Clear existing data
        for item in self.data_table.get_children():
            self.data_table.delete(item)

        # Insert new data
        for record in self.data_records:
            if record['type'] == 'Course':
                combined_info = f"Instructor: {record.get('instructor', '')}; Students: {', '.join(record.get('students', []))}"
            else:
                combined_info = ', '.join(record.get('courses', []))
            values = (
                record['id'],
                record['name'],
                record['type'],
                record.get('email', ''),
                str(record.get('age', '')),
                combined_info
            )
            self.data_table.insert('', 'end', values=values)

    def show_student_form(self):
        """
        Opens the student entry form.

        This method creates and displays a new instance of the :class:`StudentEntryForm` for
        adding or editing student information.
        """
        StudentEntryForm(self)

    def show_instructor_form(self):
        """
        Opens the instructor entry form.

        This method creates and displays a new instance of the :class:`InstructorEntryForm` for
        adding or editing instructor information.
        """
        InstructorEntryForm(self)

    def show_course_form(self):
        """
        Opens the course entry form.

        This method creates and displays a new instance of the :class:`CourseEntryForm` for
        adding or editing course information.
        """
        CourseEntryForm(self)

    def search_records(self):
        """
        Searches for records in the data table based on the user's query.

        This method retrieves the search query from the `search_field`, converts it to lowercase,
        and filters the records in `data_records` by matching the query with the record's name, ID,
        or courses. It then updates the data table with the filtered results.

        The filtering checks for the following:
        - Whether the search query is found in the record's name or ID.
        - Whether the search query matches any of the courses the student or instructor is associated with.

        After filtering, the table is refreshed to only show the matching records.

        :ivar search_field: The entry widget where the user inputs their search query.
        :vartype search_field: :class:`tk.Entry`
        :ivar data_records: A list of dictionaries containing student, course, or instructor records.
        :vartype data_records: list of dict
        :ivar data_table: The table widget displaying the filtered records.
        :vartype data_table: :class:`ttk.Treeview`
        """
        search_query = self.search_field.get().lower()
        filtered_data = [
            record for record in self.data_records if
            search_query in record['name'].lower() or
            search_query in record['id'].lower() or
            any(search_query in course.lower() for course in record.get('courses', []))
        ]

        # Update table with filtered data
        for item in self.data_table.get_children():
            self.data_table.delete(item)

        for record in filtered_data:
            if record['type'] == 'Course':
                combined_info = f"Instructor: {record.get('instructor', '')}; Students: {', '.join(record.get('students', []))}"
            else:
                combined_info = ', '.join(record.get('courses', []))
            
            values = (
                record['id'],
                record['name'],
                record['type'],
                record.get('email', ''),
                str(record.get('age', '')),
                combined_info
            )
            self.data_table.insert('', 'end', values=values)

    def edit_records(self):
        """
        Allows the user to edit a record of a specific type (Student, Instructor, or Course).

        This method prompts the user to input the type of record they want to edit 
        (Student, Instructor, or Course) and the name of the record to search for. 
        If the record is found, it opens the appropriate form to edit the record details.
        
        If the record is not found, a warning message is shown.

        :ivar data_records: A list of dictionaries containing student, instructor, or course records.
        :vartype data_records: list of dict
        :raises messagebox.showwarning: If the specified record is not found.
        """
        record_type = simpledialog.askstring("Edit Record", "Enter the type to edit (Student, Instructor, Course):")
        if record_type:
            record_name = simpledialog.askstring("Edit Record", f"Enter {record_type} name:")
            if record_name:
                record = next((r for r in self.data_records if r['name'] == record_name and r['type'].lower() == record_type.lower()), None)
                if record:
                    EditRecordForm(self, record)
                else:
                    messagebox.showwarning("Error", f"{record_type} not found.")

    def register_course(self):
        """
        Registers a student to a course.

        This method prompts the user to input a student ID and a course name. 
        It then checks if both the student and the course exist in `data_records`. 
        If found, the student is added to the course's student list, and the course is added to the student's list of courses.
        
        After registration, the data table is refreshed, and a success message is shown.
        If the student ID or course name is incorrect, a warning message is displayed.

        :ivar data_records: A list of dictionaries containing student, instructor, or course records.
        :vartype data_records: list of dict
        :raises messagebox.showinfo: If the student is successfully registered to the course.
        :raises messagebox.showwarning: If the student ID or course name is incorrect.
        """
        student_id = simpledialog.askstring("Register Course", "Enter Student ID:")
        course_name = simpledialog.askstring("Register Course", "Enter Course Name:")
        if student_id and course_name:
            student_record = next((r for r in self.data_records if r['id'] == student_id and r['type'] == 'Student'), None)
            course_record = next((c for c in self.data_records if c['name'] == course_name and c['type'] == 'Course'), None)
            if student_record and course_record:
                if student_record['name'] not in course_record['students']:
                    course_record['students'].append(student_record['name'])
                if course_name not in student_record['courses']:
                    student_record['courses'].append(course_name)
                self.refresh_data_table()
                messagebox.showinfo("Success", f"Student {student_record['name']} registered to {course_name}.")
            else:
                messagebox.showwarning("Error", "Student ID or Course Name is incorrect.")

    def delete(self):
        """
        Deletes a record from the system.

        This method prompts the user to input the name of the record they wish to delete.
        If a matching record is found in `data_records`, the record is removed, the table is refreshed,
        and a success message is displayed. If no matching record is found, a warning is shown.

        :ivar data_records: A list of dictionaries containing student, instructor, or course records.
        :vartype data_records: list of dict
        :raises messagebox.showinfo: If the record is successfully deleted.
        :raises messagebox.showwarning: If the record is not found.
        """
        record_name = simpledialog.askstring("Delete Record", "Enter Record name:")
        if record_name:
            record = next((r for r in self.data_records if r['name'] == record_name), None)
            if record:
                self.data_records.remove(record)
                self.refresh_data_table()
                messagebox.showinfo("Success", "Record deleted successfully!")
            else:
                messagebox.showwarning("Error", "Record not found.")

    def assign(self):
        """
        Assigns a course to an instructor.

        This method prompts the user to input an instructor's ID or name and the name of a course.
        If both the instructor and the course are found in `data_records`, the course is assigned to the
        instructor, and the course record is updated to include the instructor. The table is then refreshed,
        and a success message is displayed.

        If either the instructor or course is not found, a warning message is shown.

        :ivar data_records: A list of dictionaries containing student, instructor, or course records.
        :vartype data_records: list of dict
        :raises messagebox.showinfo: If the course is successfully assigned to the instructor.
        :raises messagebox.showwarning: If the instructor or course is not found.
        """
        instructor_id = simpledialog.askstring("Assign Course", "Enter Instructor ID or Name:")
        course_name = simpledialog.askstring("Assign Course", "Enter Course Name:")
        if instructor_id and course_name:
            instructor_record = next((r for r in self.data_records if (r['id'] == instructor_id or r['name'] == instructor_id) and r['type'] == 'Instructor'), None)
            course_record = next((c for c in self.data_records if c['name'] == course_name and c['type'] == 'Course'), None)
            if instructor_record and course_record:
                course_record['instructor'] = instructor_record['name']
                if course_name not in instructor_record['courses']:
                    instructor_record['courses'].append(course_name)
                self.refresh_data_table()
                messagebox.showinfo("Success", f"Course {course_name} assigned to Instructor {instructor_record['name']}.")
            else:
                messagebox.showwarning("Error", "Instructor ID or Course Name is incorrect.")

    def save_records(self):
        """
        Saves the current records to a JSON file.

        This method opens a file dialog for the user to specify the location and filename
        to save the data. It then writes the content of `data_records` to a JSON file.
        
        If the file is saved successfully, an info message is displayed. If an error occurs
        during the saving process, an error message is shown.

        :ivar data_records: A list of dictionaries containing student, instructor, or course records.
        :vartype data_records: list of dict
        :raises messagebox.showinfo: If the data is saved successfully.
        :raises messagebox.showerror: If an error occurs during the save process.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    json.dump(self.data_records, file, indent=4)
                messagebox.showinfo("Success", "Data saved successfully!")
            except Exception as error:
                messagebox.showerror("Error", f"Error saving data: {error}")

    def load_records(self):
        """
        Loads records from a JSON file.

        This method opens a file dialog for the user to select a JSON file containing
        records. It then reads the file and updates `data_records` with the loaded data.
        
        The table is refreshed to display the loaded data. If the data is loaded successfully,
        an info message is displayed. If an error occurs during the loading process, an error
        message is shown.

        :ivar data_records: A list of dictionaries containing student, instructor, or course records.
        :vartype data_records: list of dict
        :raises messagebox.showinfo: If the data is loaded successfully.
        :raises messagebox.showerror: If an error occurs during the load process.
        """
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.data_records = json.load(file)
                self.refresh_data_table()
                messagebox.showinfo("Success", "Data loaded successfully!")
            except Exception as error:
                messagebox.showerror("Error", f"Error loading data: {error}")

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    headers = ["ID", "Name", "Type", "Email", "Age", "Courses/Instructor/Students"]
                    file.write(','.join(headers) + '\n')
                    for record in self.data_records:
                        id = record['id']
                        name = record['name']
                        type = record['type']
                        email = record.get('email', '')
                        age = str(record.get('age', ''))
                        if type == 'Course':
                            combined_info = f"Instructor: {record.get('instructor', '')}; Students: {', '.join(record.get('students', []))}"
                        else:
                            combined_info = ', '.join(record.get('courses', []))
                        file.write(f"{id},{name},{type},{email},{age},{combined_info}\n")
                messagebox.showinfo("Success", "Data exported to CSV successfully!")
            except Exception as error:
                messagebox.showerror("Error", f"Error exporting data: {error}")

class StudentEntryForm(tk.Toplevel):
    """
    A form for adding a new student to the system.

    This class opens a modal window with fields to input student details such as name, age, email, and student ID.
    Additionally, a list of available courses is provided for the user to select multiple courses for the student.

    :param parent: The parent window (typically the main management app).
    :type parent: :class:`tk.Tk`
    """

    def __init__(self, parent):
        """
        Initializes the Student Entry Form.

        Creates a form with input fields for student details (name, age, email, student ID) and a 
        multi-selection listbox for selecting courses the student will enroll in. 

        A "Submit" button is included to add the new student and update the parent data table.

        :param parent: The parent window (the management app that invokes this form).
        :type parent: :class:`tk.Tk`
        """
        super().__init__(parent)
        self.title("Add Student")
        self.geometry("400x400")
        self.parent = parent

        layout = tk.Frame(self)
        layout.pack(pady=10, padx=10)

        # Name input
        tk.Label(layout, text="Name").grid(row=0, column=0, sticky=tk.W)
        self.student_name_input = tk.Entry(layout)
        self.student_name_input.grid(row=0, column=1)

        # Age input
        tk.Label(layout, text="Age").grid(row=1, column=0, sticky=tk.W)
        self.student_age_input = tk.Entry(layout)
        self.student_age_input.grid(row=1, column=1)

        # Email input
        tk.Label(layout, text="Email").grid(row=2, column=0, sticky=tk.W)
        self.student_email_input = tk.Entry(layout)
        self.student_email_input.grid(row=2, column=1)

        # Student ID input
        tk.Label(layout, text="Student ID").grid(row=3, column=0, sticky=tk.W)
        self.student_id_input = tk.Entry(layout)
        self.student_id_input.grid(row=3, column=1)

        # Courses input (Listbox)
        tk.Label(layout, text="Courses").grid(row=4, column=0, sticky=tk.W)
        courses = [course.course_name for course in self.parent.course_list]
        self.course_listbox = tk.Listbox(layout, selectmode=tk.MULTIPLE)
        for course in courses:
            self.course_listbox.insert(tk.END, course)
        self.course_listbox.grid(row=4, column=1)

        # Submit button
        submit_btn = tk.Button(layout, text="Submit", command=self.submit_student)
        submit_btn.grid(row=5, column=0, columnspan=2, pady=10)

    def submit_student(self):
        """
        Handles the submission of the student form.

        This method collects data from the form fields, validates the input, and adds the student record to the parent's `data_records`.
        The selected courses are also updated in both the student record and the course records. 
        The data table in the parent window is refreshed after a successful submission.

        If any required fields are missing, an error message is displayed. If any error occurs during the process,
        an exception is caught and an error message is shown.

        :raises messagebox.showerror: If any required fields are empty or an error occurs while saving the student.
        """
        name = self.student_name_input.get().strip()
        age = self.student_age_input.get().strip()
        email = self.student_email_input.get().strip()
        student_id = self.student_id_input.get().strip()
        selected_courses_indices = self.course_listbox.curselection()
        selected_courses = [self.course_listbox.get(i) for i in selected_courses_indices]

        # Check if all fields are filled
        if not name or not age or not email or not student_id:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        try:
            # Add student to data records
            self.parent.data_records.append({
                'id': student_id,
                'name': name,
                'type': 'Student',
                'age': age,
                'email': email,
                'courses': selected_courses
            })

            # Update the course records with the new student
            for course_name in selected_courses:
                course_record = next((c for c in self.parent.data_records if c['name'] == course_name and c['type'] == 'Course'), None)
                if course_record:
                    if name not in course_record['students']:
                        course_record['students'].append(name)
                else:
                    # Add new course record if it doesn't exist in data_records
                    course_obj = next((c for c in self.parent.course_list if c.course_name == course_name), None)
                    if course_obj:
                        new_course_record = {
                            'id': course_obj.course_id,
                            'name': course_obj.course_name,
                            'type': 'Course',
                            'instructor': '',
                            'students': [name]
                        }
                        self.parent.data_records.append(new_course_record)

            # Refresh data table in the parent window
            self.parent.refresh_data_table()
            self.destroy()
        except Exception as error:
            messagebox.showerror("Error", f"Error saving student: {error}")

class InstructorEntryForm(tk.Toplevel):
    """
    A form for adding a new instructor to the system.

    This class opens a modal window with fields to input instructor details such as name, age, email, and instructor ID.
    Additionally, a list of available courses is provided for the user to select multiple courses that the instructor will teach.

    :param parent: The parent window (typically the main management app).
    :type parent: :class:`tk.Tk`
    """

    def __init__(self, parent):
        """
        Initializes the Instructor Entry Form.

        Creates a form with input fields for instructor details (name, age, email, instructor ID) and a
        multi-selection listbox for selecting courses the instructor will teach.

        A "Submit" button is included to add the new instructor and update the parent data table.

        :param parent: The parent window (the management app that invokes this form).
        :type parent: :class:`tk.Tk`
        """
        super().__init__(parent)
        self.title("Add Instructor")
        self.geometry("400x400")
        self.parent = parent

        layout = tk.Frame(self)
        layout.pack(pady=10, padx=10)

        # Name input
        tk.Label(layout, text="Name").grid(row=0, column=0, sticky=tk.W)
        self.instructor_name_input = tk.Entry(layout)
        self.instructor_name_input.grid(row=0, column=1)

        # Age input
        tk.Label(layout, text="Age").grid(row=1, column=0, sticky=tk.W)
        self.instructor_age_input = tk.Entry(layout)
        self.instructor_age_input.grid(row=1, column=1)

        # Email input
        tk.Label(layout, text="Email").grid(row=2, column=0, sticky=tk.W)
        self.instructor_email_input = tk.Entry(layout)
        self.instructor_email_input.grid(row=2, column=1)

        # Instructor ID input
        tk.Label(layout, text="Instructor ID").grid(row=3, column=0, sticky=tk.W)
        self.instructor_id_input = tk.Entry(layout)
        self.instructor_id_input.grid(row=3, column=1)

        # Courses input (Listbox)
        tk.Label(layout, text="Courses").grid(row=4, column=0, sticky=tk.W)
        courses = [course.course_name for course in self.parent.course_list]
        self.course_listbox = tk.Listbox(layout, selectmode=tk.MULTIPLE)
        for course in courses:
            self.course_listbox.insert(tk.END, course)
        self.course_listbox.grid(row=4, column=1)

        # Submit button
        submit_btn = tk.Button(layout, text="Submit", command=self.submit_instructor)
        submit_btn.grid(row=5, column=0, columnspan=2, pady=10)

    def submit_instructor(self):
        """
        Handles the submission of the instructor form.

        This method collects data from the form fields, validates the input, and adds the instructor record to the parent's `data_records`.
        The selected courses are also updated in both the instructor record and the course records.
        The data table in the parent window is refreshed after a successful submission.

        If any required fields are missing, an error message is displayed. If any error occurs during the process,
        an exception is caught and an error message is shown.

        :raises messagebox.showerror: If any required fields are empty or an error occurs while saving the instructor.
        """
        name = self.instructor_name_input.get().strip()
        age = self.instructor_age_input.get().strip()
        email = self.instructor_email_input.get().strip()
        instructor_id = self.instructor_id_input.get().strip()
        selected_courses_indices = self.course_listbox.curselection()
        selected_courses = [self.course_listbox.get(i) for i in selected_courses_indices]

        # Check if all fields are filled
        if not name or not age or not email or not instructor_id:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        try:
            # Add instructor to data records
            self.parent.data_records.append({
                'id': instructor_id,
                'name': name,
                'type': 'Instructor',
                'age': age,
                'email': email,
                'courses': selected_courses
            })

            # Update the course records with the new instructor
            for course_name in selected_courses:
                course_record = next((c for c in self.parent.data_records if c['name'] == course_name and c['type'] == 'Course'), None)
                if course_record:
                    course_record['instructor'] = name
                else:
                    # Add new course record if it doesn't exist in data_records
                    course_obj = next((c for c in self.parent.course_list if c.course_name == course_name), None)
                    if course_obj:
                        new_course_record = {
                            'id': course_obj.course_id,
                            'name': course_obj.course_name,
                            'type': 'Course',
                            'instructor': name,
                            'students': []
                        }
                        self.parent.data_records.append(new_course_record)

            # Refresh data table in the parent window
            self.parent.refresh_data_table()
            self.destroy()
        except Exception as error:
            messagebox.showerror("Error", f"Error saving instructor: {error}")
class CourseEntryForm(tk.Toplevel):
    """
    A form for adding a new course to the system.

    This class opens a modal window with fields to input course details such as course name, course ID, instructor, and students.
    The user can select an instructor from a dropdown list and enroll multiple students using a multi-selection listbox.

    :param parent: The parent window (typically the main management app).
    :type parent: :class:`tk.Tk`
    """

    def __init__(self, parent):
        """
        Initializes the Course Entry Form.

        Creates a form with input fields for course details (course name, course ID), a dropdown to select an instructor,
        and a multi-selection listbox for enrolling students.

        A "Submit" button is included to add the new course and update the parent data table.

        :param parent: The parent window (the management app that invokes this form).
        :type parent: :class:`tk.Tk`
        """
        super().__init__(parent)
        self.title("Add Course")
        self.geometry("400x500")
        self.parent = parent

        layout = tk.Frame(self)
        layout.pack(pady=10, padx=10)

        # Course name input
        tk.Label(layout, text="Course Name").grid(row=0, column=0, sticky=tk.W)
        self.course_name_input = tk.Entry(layout)
        self.course_name_input.grid(row=0, column=1)

        # Course ID input
        tk.Label(layout, text="Course ID").grid(row=1, column=0, sticky=tk.W)
        self.course_id_input = tk.Entry(layout)
        self.course_id_input.grid(row=1, column=1)

        # Instructor dropdown
        tk.Label(layout, text="Instructor").grid(row=2, column=0, sticky=tk.W)
        instructors = [record['name'] for record in self.parent.data_records if record['type'] == 'Instructor']
        self.instructor_combobox = ttk.Combobox(layout, values=["None"] + instructors)
        self.instructor_combobox.current(0)
        self.instructor_combobox.grid(row=2, column=1)

        # Students listbox
        tk.Label(layout, text="Enroll Students").grid(row=3, column=0, sticky=tk.W)
        students = [record['name'] for record in self.parent.data_records if record['type'] == 'Student']
        self.student_listbox = tk.Listbox(layout, selectmode=tk.MULTIPLE)
        for student in students:
            self.student_listbox.insert(tk.END, student)
        self.student_listbox.grid(row=3, column=1)

        # Submit button
        submit_btn = tk.Button(layout, text="Submit", command=self.submit_course)
        submit_btn.grid(row=4, column=0, columnspan=2, pady=10)

    def submit_course(self):
        """
        Handles the submission of the course form.

        This method collects data from the form fields, validates the input, and adds the course record to the parent's `data_records`.
        It also updates the selected instructor's courses and the students' enrolled courses. The data table in the parent window is
        refreshed after a successful submission.

        If any required fields are missing, an error message is displayed. If any error occurs during the process,
        an exception is caught and an error message is shown.

        :raises messagebox.showerror: If any required fields are empty or an error occurs while saving the course.
        """
        course_name = self.course_name_input.get().strip()
        course_id = self.course_id_input.get().strip()
        selected_instructor_name = self.instructor_combobox.get()
        selected_students_indices = self.student_listbox.curselection()
        selected_students = [self.student_listbox.get(i) for i in selected_students_indices]

        if not course_name or not course_id:
            messagebox.showerror("Error", "Course Name and Course ID must be filled.")
            return

        try:
            instructor_name = selected_instructor_name if selected_instructor_name != 'None' else ''

            self.parent.data_records.append({
                'id': course_id,
                'name': course_name,
                'type': 'Course',
                'instructor': instructor_name,
                'students': selected_students
            })

            # Update instructor's courses
            if instructor_name:
                instructor_record = next((i for i in self.parent.data_records if i['name'] == instructor_name and i['type'] == 'Instructor'), None)
                if instructor_record:
                    if course_name not in instructor_record['courses']:
                        instructor_record['courses'].append(course_name)

            # Update students' courses
            for student_name in selected_students:
                student_record = next((s for s in self.parent.data_records if s['name'] == student_name and s['type'] == 'Student'), None)
                if student_record:
                    if course_name not in student_record['courses']:
                        student_record['courses'].append(course_name)

            self.parent.refresh_data_table()
            self.destroy()

        except Exception as error:
            messagebox.showerror("Error", f"Error saving course: {error}")

class EditRecordForm(tk.Toplevel):
    """
    A form for editing an existing record (Student, Instructor, or Course).

    This class opens a modal window that allows the user to edit the details of an existing record. Depending on the type of record
    (Student, Instructor, or Course), the appropriate fields (e.g., name, ID, email, age, instructor, students, or courses) are shown.

    :param parent: The parent window (typically the main management app).
    :type parent: :class:`tk.Tk`
    :param record: The record to be edited.
    :type record: dict
    """

    def __init__(self, parent, record):
        """
        Initializes the Edit Record Form.

        The form is populated with the existing details of the selected record. The form includes input fields
        for name, ID, email, and age. If the record is of type 'Course', fields for instructor and students are also provided.

        A "Save Changes" button is included to save the modifications and update the parent data table.

        :param parent: The parent window (the management app that invokes this form).
        :type parent: :class:`tk.Tk`
        :param record: The record to be edited.
        :type record: dict
        """
        super().__init__(parent)
        self.title(f"Edit {record['type']}")
        self.geometry("400x400")
        self.parent = parent
        self.record = record

        layout = tk.Frame(self)
        layout.pack(pady=10, padx=10)

        # Name input
        tk.Label(layout, text="Name").grid(row=0, column=0, sticky=tk.W)
        self.name_input = tk.Entry(layout)
        self.name_input.insert(0, record['name'])
        self.name_input.grid(row=0, column=1)

        # ID input
        tk.Label(layout, text="ID").grid(row=1, column=0, sticky=tk.W)
        self.id_input = tk.Entry(layout)
        self.id_input.insert(0, record['id'])
        self.id_input.grid(row=1, column=1)

        # Email input
        tk.Label(layout, text="Email").grid(row=2, column=0, sticky=tk.W)
        self.email_input = tk.Entry(layout)
        self.email_input.insert(0, record.get('email', ''))
        self.email_input.grid(row=2, column=1)

        # Age input
        tk.Label(layout, text="Age").grid(row=3, column=0, sticky=tk.W)
        self.age_input = tk.Entry(layout)
        self.age_input.insert(0, str(record.get('age', '')))
        self.age_input.grid(row=3, column=1)

        if record['type'] == "Course":
            # Instructor input for Course records
            tk.Label(layout, text="Instructor").grid(row=4, column=0, sticky=tk.W)
            instructors = ["None"] + [rec['name'] for rec in self.parent.data_records if rec['type'] == 'Instructor']
            self.instructor_combobox = ttk.Combobox(layout, values=instructors)
            self.instructor_combobox.set(record.get('instructor', 'None'))
            self.instructor_combobox.grid(row=4, column=1)

            # Students input for Course records
            tk.Label(layout, text="Students (comma-separated)").grid(row=5, column=0, sticky=tk.W)
            self.students_input = tk.Entry(layout)
            self.students_input.insert(0, ", ".join(record.get('students', [])))
            self.students_input.grid(row=5, column=1)
        else:
            # Courses input for Student or Instructor records
            tk.Label(layout, text="Courses (comma-separated)").grid(row=4, column=0, sticky=tk.W)
            self.courses_input = tk.Entry(layout)
            self.courses_input.insert(0, ", ".join(record.get('courses', [])))
            self.courses_input.grid(row=4, column=1)

        # Save button
        save_btn = tk.Button(layout, text="Save Changes", command=self.save_edit)
        save_btn.grid(row=6, column=0, columnspan=2, pady=10)

    def save_edit(self):
        """
        Saves the edited details to the record and updates the parent data table.

        This method retrieves the updated values from the form fields and modifies the record accordingly.
        After saving the changes, the parent data table is refreshed, and a success message is displayed.

        :raises messagebox.showinfo: If the record is updated successfully.
        """
        self.record['name'] = self.name_input.get()
        self.record['id'] = self.id_input.get()
        self.record['email'] = self.email_input.get()
        self.record['age'] = self.age_input.get()

        if self.record['type'] == "Course":
            self.record['instructor'] = self.instructor_combobox.get()
            students = self.students_input.get()
            self.record['students'] = [s.strip() for s in students.split(',') if s.strip()]
        else:
            courses = self.courses_input.get()
            self.record['courses'] = [c.strip() for c in courses.split(',') if c.strip()]

        self.parent.refresh_data_table()
        self.destroy()
        messagebox.showinfo("Success", "Record updated successfully!")

if __name__ == '__main__':
    app = ManagementApp()
    app.mainloop()
