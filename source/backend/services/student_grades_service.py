# services/student_grades_service.py

from sqlalchemy.orm import Session
from backend.database.models import StudentGrades

class StudentGradesService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, subject_code, semester, points, credit_hours, student_id):
        new_grade = StudentGrades(
            subject_code=subject_code,
            semester=semester,
            points=points,
            credit_hours=credit_hours,
            student_id=student_id
        )
        self.session.add(new_grade)
        self.session.commit()
        return new_grade

    def get(self, grade_id):
        return self.session.get(StudentGrades, grade_id)

    def get_all_by_student(self, student_id):
        return self.session.query(StudentGrades).filter_by(student_id=student_id).all()

    def update(self, grade_id, subject_code=None, semester=None, points=None, credit_hours=None):
        grade = self.get(grade_id)
        if not grade:
            print("Grade not found.")
            return None

        updated = False

        if subject_code is not None:
            grade.subject_code = subject_code
            updated = True
        if semester is not None:
            grade.semester = semester
            updated = True
        if points is not None:
            grade.points = points
            updated = True
        if credit_hours is not None:
            grade.credit_hours = credit_hours
            updated = True

        if updated:
            self.session.commit()
            print("Grade updated successfully.")
        else:
            print("Nothing to update.")

        return grade

    def delete(self, grade_id):
        grade = self.get(grade_id)
        if not grade:
            print("Grade not found.")
            return None

        self.session.delete(grade)
        self.session.commit()
        return grade

    def add_df(self, df):
        new_grades= []
        for _, row in df.iterrows():
            new_grade = StudentGrades(
                student_id_num=row["id"],
                subject_code=row["subject_code"],
                points=row["gpa"],
                credit_hours=row["cridet_hours"],
            )
            new_grades.append(new_grade)
        self.session.add_all(new_grades)
        self.session.commit()
