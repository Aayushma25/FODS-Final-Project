import pandas as pd
import matplotlib.pyplot as plt

class User:
    def __init__(self, username, role, user_id):
        self.username = username
        self.role = role
        self.user_id = user_id

class Student(User):
    def __init__(self, username, user_id):
        super().__init__(username, 'student', user_id)

class Admin(User):
    def __init__(self, username, user_id):
        super().__init__(username, 'admin', user_id)

class StudentProfileManagementSystem:
    def __init__(self):
        self.users = self.load_users()
        self.grades = self.load_grades()
        self.eca = self.load_eca()
        self.current_user = None

    def load_users(self):
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, role, user_id = line.strip().split(',')
                if role == 'admin':
                    users.append(Admin(username, user_id))
                else:
                    users.append(Student(username, user_id))
        return users

    def load_grades(self):
        grades = {}
        with open('grades.txt', 'r') as file:
            for line in file:
                data = line.strip().split(',')
                grades[data[0]] = list(map(int, data[1:]))
        return grades

    def load_eca(self):
        eca = {}
        with open('eca.txt', 'r') as file:
            for line in file:
                data = line.strip().split(',')
                eca[data[0]] = data[1:]
        return eca

    def load_passwords(self):
        passwords = {}
        with open('passwords.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                passwords[username] = password
        return passwords

    def login(self):
        passwords = self.load_passwords()
        while True:
            username = input("Enter username: ")
            password = input("Enter password: ")
            if username in passwords and passwords[username] == password:
                self.current_user = next(user for user in self.users if user.username == username)
                print(f"Welcome {self.current_user.username}!")
                break
            else:
                print("Invalid credentials. Please try again.")

    def admin_functions(self):
        while True:
            print("\nAdmin Functions:")
            print("1. Add User")
            print("2. Update Student Record")
            print("3. Delete Student Record")
            print("4. Generate Insights")
            print("5. Logout")
            choice = input("Choose an option: ")

            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.update_student_record()
            elif choice == '3':
                self.delete_student_record()
            elif choice == '4':
                self.generate_insights()
            elif choice == '5':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

   

    def add_user(self):
        username = input("Enter new username: ")
        role = input("Enter role (student/admin): ")
        user_id = input("Enter user ID: ")
        password = input("Enter password: ")

        with open('users.txt', 'a') as file:
            file.write(f"{username},{role},{user_id}\n")
        with open('passwords.txt', 'a') as file:
            file.write(f"{username},{password}\n")
        print("User  added successfully.")

    def update_student_record(self):
        user_id = input("Enter student ID to update: ")
        if user_id in self.grades:
            new_grades = input("Enter new grades for 5 subjects (comma-separated): ")
            self.grades[user_id] = list(map(int, new_grades.split(',')))
            self.save_grades()
            print("Student record updated successfully.")
        else:
            print("Student ID not found.")

    def delete_student_record(self):
        user_id = input("Enter student ID to delete: ")
        if user_id in self.grades:
            del self.grades[user_id]
            self.users = [user for user in self.users if user.user_id != user_id]
            self.save_users()
            print("Student record deleted successfully.")
        else:
            print("Student ID not found.")

    def generate_insights(self):
        subject_averages = [0] * 5
        student_count = len(self.grades)

        for grades in self.grades.values():
            for i in range(5):
                subject_averages[i] += grades[i]

        subject_averages = [avg / student_count for avg in subject_averages]
        print("Average grades per subject:", subject_averages)

        # Most active students in ECA
        eca_participation = {user.user_id: len(self.eca.get(user.user_id, [])) for user in self.users if isinstance(user, Student)}
        most_active_students = sorted(eca_participation.items(), key=lambda x: x[1], reverse=True)
        print("Most active students in ECA:", most_active_students)

    def view_profile(self):
        print(f"Username: {self.current_user.username}")
        print(f"Role: {self.current_user.role}")
        print(f"User  ID: {self.current_user.user_id}")

    def update_profile(self):
        new_username = input("Enter new username: ")
        for user in self.users:
            if user.username == self.current_user.username:
                user.username = new_username
                break
        self.save_users()
        print("Profile updated successfully.")

    def view_grades(self):
        user_id = self.current_user.user_id
        if user_id in self.grades:
            print("Grades:", self.grades[user_id])
        else:
            print("No grades found.")

    def view_eca(self):
        user_id = self.current_user.user_id
        if user_id in self.eca:
            print("ECA Participation:", self.eca[user_id])
        else:
            print("No ECA participation found.")

    def save_grades(self):
        with open('grades.txt', 'w') as file:
            for user_id, grades in self.grades.items():
                file.write(f"{user_id},{','.join(map(str, grades))}\n")

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username},{user.role},{user.user_id}\n")

    def run(self):
        self.login()
        if isinstance(self.current_user, Admin):
            self.admin_functions()
        else:
            print("Students do not have admin access.")

# Create an instance of the system and run it
if __name__ == "__main__":
    system = StudentProfileManagementSystem()
    system.run()
