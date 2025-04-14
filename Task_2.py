
import pandas as pd
import matplotlib.pyplot as plt
from Task_1 import StudentProfileManagementSystem, Student, Admin

class PerformanceAnalyticsDashboard(StudentProfileManagementSystem):
    def admin_functions(self):
        while True:
            print("\nAdmin Functions:")
            print("1. Add User")
            print("2. Update Student Record")
            print("3. Delete Student Record")
            print("4. Generate Insights")
            print("5. Performance Analytics Dashboard")
            print("6. Logout")
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
                self.performance_analytics_dashboard()
            elif choice == '6':
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def performance_analytics_dashboard(self):
        print("\nPerformance Analytics Dashboard")
        self.grade_trends()
        self.eca_impact()
        self.performance_alerts()

    def grade_trends(self):
        df = pd.DataFrame(self.grades).T
        df.columns = ['FODS', 'FOM', 'IT', 'ITF', 'AE & EC']
        df.index.name = 'Student ID'

        df.plot(kind='line', marker='o')
        plt.title('Grade Trends for Students')
        plt.xlabel('Student ID')
        plt.ylabel('Grades')
        plt.ylim(0, 100)
        plt.grid()
        plt.legend(title='Subjects')
        plt.show()

    def eca_impact(self):
        eca_participation = {user.user_id: len(self.eca.get(user.user_id, [])) for user in self.users if isinstance(user, Student)}
        eca_df = pd.DataFrame(list(eca_participation.items()), columns=['Student ID', 'ECA Count'])
        
        grades_df = pd.DataFrame(self.grades).T
        grades_df.columns = ['FODS', 'FOM', 'IT', 'ITF', 'AE & EC']
        grades_df['Average'] = grades_df.mean(axis=1)
        grades_df.index.name = 'Student ID'

        # Merge ECA participation with grades
        merged_df = pd.merge(eca_df, grades_df[['Average']], on='Student ID')

        # Plotting ECA impact on average grades
        plt.scatter(merged_df['ECA Count'], merged_df['Average'], color='blue')
        plt.title('ECA Participation vs Average Grades')
        plt.xlabel('ECA Count')
        plt.ylabel('Average Grades')
        plt.grid()
        plt.show()

    def performance_alerts(self):
        threshold = 60  # Define a threshold for performance alerts
        underperforming_students = {user_id: grades for user_id, grades in self.grades.items() if any(grade < threshold for grade in grades)}

        if underperforming_students:
            print("Performance Alerts: Students performing below the threshold:")
            for user_id, grades in underperforming_students.items():
                print(f"Student ID: {user_id}, Grades: {grades}")
        else:
            print("No students are performing below the threshold.")

# Create an instance of the Performance Analytics Dashboard and run it
if __name__ == "__main__":
    system = PerformanceAnalyticsDashboard()
    system.run()
