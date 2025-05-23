from sqlalchemy.orm import Session
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.database.models import StudentAssignment
import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import Session
from pathlib import Path


class StudentAssignmentService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, project_id, student_id, assignment_date, status,
               department_id=None, program_id=None, specialization_id=None):
        new_assignment = StudentAssignment(
            project_id=project_id,
            student_id=student_id,
            assignment_date=assignment_date,
            status=status,
            department_id=department_id,
            program_id=program_id,
            specialization_id=specialization_id
        )
        self.session.add(new_assignment)
        self.session.commit()
        return new_assignment

    def get(self, assignment_id):
        return self.session.get(StudentAssignment, assignment_id)

    def get_all(self):
        return self.session.query(StudentAssignment).all()

    def update(self, assignment_id, project_id=None, student_id=None, assignment_date=None,
               status=None, department_id=None, program_id=None, specialization_id=None):
        assignment = self.get(assignment_id)
        if not assignment:
            print("Assignment not found.")
            return None

        updated = False

        if project_id is not None:
            assignment.project_id = project_id
            updated = True
        if student_id is not None:
            assignment.student_id = student_id
            updated = True
        if assignment_date is not None:
            assignment.assignment_date = assignment_date
            updated = True
        if status is not None:
            assignment.status = status
            updated = True
        if department_id is not None:
            assignment.department_id = department_id
            updated = True
        if program_id is not None:
            assignment.program_id = program_id
            updated = True
        if specialization_id is not None:
            assignment.specialization_id = specialization_id
            updated = True

        if updated:
            self.session.commit()
            print("Assignment updated successfully.")
        else:
            print("Nothing to update.")

        return assignment

    def delete(self, assignment_id):
        assignment = self.get(assignment_id)
        if not assignment:
            print("Assignment not found.")
            return

        self.session.delete(assignment)
        self.session.commit()
        return assignment


    def save_to_csv(self, directory):
        # Fetch all assignments
        assignments = self.get_all()

        # Convert to DataFrame
        data = [{
            'student_id': assignment.student_id_num,
            'student_name': assignment.student.name,
            'result': assignment.result
        } for assignment in assignments]

        df = pd.DataFrame(data)

        print(df)
        # Save to CSV
        file_path = Path(directory) / "results.csv"
        df.to_csv(file_path, index=False, encoding='utf-8-sig')


    # read how many has been assigned to each program
    def get_result_frequencies(self):
        """
        Returns a dictionary of result counts, excluding None values.
        """
        result_counts = (
            self.session.query(StudentAssignment.result, func.count(StudentAssignment.result))
            .filter(StudentAssignment.result.isnot(None))  # Exclude NULLs
            .group_by(StudentAssignment.result)
            .all()
        )
        return {result: count for result, count in result_counts}