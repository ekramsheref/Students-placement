# services/program_service.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from sqlalchemy.orm import Session
from backend.services.student_assignment_service import StudentAssignmentService
from backend.database.models import Program, RequiredSubject

class ProgramService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, department_id: int, gpa_threshold: float = None, student_capacity: int = None,
               subjects_required_dict: dict = None):
        new_program = Program(
            name=name,
            department_id=department_id,
            gpa_threshold=gpa_threshold,
            student_capacity=student_capacity
        )
        # -> example of how to add subjects
        # subjects_required_dict = {
        #     "math101": 60,
        #     "phy101": 70,
        #     "chem101": 75
        # } -> example of how to add subjects

        if subjects_required_dict:
            for subject_code, min_grade in subjects_required_dict.items():
                new_subjects_required = RequiredSubject(
                    code=subject_code,
                    min_grade=min_grade
                )
                new_program.subjects_required.append(new_subjects_required)

        self.session.add(new_program)
        self.session.commit()
        return new_program

    def get(self, program_id):
        return self.session.get(Program, program_id)  # or self.session.query(Program).get(program_id)

    def get_all(self):
        return self.session.query(Program).all()

    def update(self, program_id, name=None, department_id=None, subjects_required=None, gpa_threshold=None,
               student_capacity=None):
        program = self.get(program_id)
        if not program:
            print("Program not found.")
            return None

        updated = False

        if name is not None:
            program.name = name
            updated = True
        if department_id is not None:
            program.department_id = department_id
            updated = True
        if gpa_threshold is not None:
            program.gpa_threshold = gpa_threshold
            updated = True
        if student_capacity is not None:
            program.student_capacity = student_capacity
            updated = True

        if subjects_required is not None:
            # Clear existing subjects
            program.subjects_required.clear()
            # Add new subjects
            for subject_code, min_grade in subjects_required.items():
                new_subjects_required = RequiredSubject(
                    code=subject_code,
                    min_grade=min_grade
                )
                program.subjects_required.append(new_subjects_required)

            updated = True

        if updated:
            self.session.commit()
            print("Program updated successfully.")
        else:
            print("Nothing to update.")

        return program

    def delete(self, program_id):
        program = self.get(program_id)
        if not program:
            print("Program not found.")
            return

        self.session.delete(program)
        self.session.commit()
        return program

    def get_by_name(self, name: str):
        return self.session.query(Program).filter(Program.name == name).first()

    def get_all_and_capacity(self):
        programs = self.session.query(Program).all()
        program_capacity = {program.name: program.student_capacity for program in programs}
        return program_capacity



    def get_filled_percentage(self):
        student_assignment_service = StudentAssignmentService(self.session)
        result_count = student_assignment_service.get_result_frequencies()

        programs = self.session.query(Program).all()

        filled_percentage = {}
        for program in programs:
            filled_percentage[program.name] = (result_count[program.name] / program.student_capacity) * 100 if program.student_capacity and program.name in result_count else 0
        return filled_percentage

# example usage of how to add a program
# create a program
# program_service = ProgramService(session)
# program_service.create(
#     name="Computer Science",
#     department_id=1,
#     gpa_threshold=3.0,
#     student_capacity=100,
#     subjects_required_dict={
#         "math101": 60,
#         "phy101": 70
#     }
# )
# و نفس الطريقة في التخصص اشطا