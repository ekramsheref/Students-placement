# services/specialization_service.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from sqlalchemy.orm import Session

from backend.database.models import Specialization, RequiredSubject


class SpecializationService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name:str, department_id:int, program_id:int, gpa_threshold:float = None, student_capacity:int= None, subjects_required_dict:dict = None):
        new_specialization = Specialization(
            name=name,
            program_id=program_id,
            gpa_threshold=gpa_threshold,
            student_capacity=student_capacity,

        )
        if subjects_required_dict:
            for subject_code, min_grade in subjects_required_dict.items():
                new_subjects_required = RequiredSubject(
                    code=subject_code,
                    min_grade=min_grade,
                )
                new_specialization.subjects_required.append(new_subjects_required)

        self.session.add(new_specialization)
        self.session.commit()
        return new_specialization

    def get(self, specialization_id):
        return self.session.get(Specialization,
                                specialization_id)  # or self.session.query(Specialization).get(specialization_id)

    def get_all(self):
        return self.session.query(Specialization).all()

def update(self, specialization_id, name=None, subjects_required_dict=None, gpa_threshold=None, student_capacity=None,
           program_id=None, department_id=None):
    # Fetch the specialization using its ID
    specialization = self.get(specialization_id)
    if not specialization:
        print("Specialization not found.")
        return None

    updated = False

    # Update basic attributes if new values are provided
    if name is not None:
        specialization.name = name
        updated = True
    if gpa_threshold is not None:
        specialization.gpa_threshold = gpa_threshold
        updated = True
    if student_capacity is not None:
        specialization.student_capacity = student_capacity
        updated = True
    if program_id is not None:
        specialization.program_id = program_id
        updated = True

    # Update subjects_required if a new dictionary is provided
    if subjects_required_dict is not None:
        # Clear existing required subjects
        specialization.subjects_required.clear()

        # Add the subjects from the updated dictionary
        for subject_code, min_grade in subjects_required_dict.items():
            new_subjects_required = RequiredSubject(
                code=subject_code,
                min_grade=min_grade
            )
            specialization.subjects_required.append(new_subjects_required)

        updated = True

    # Commit changes only if there are updates
    if updated:
        self.session.commit()
        print("Specialization updated successfully.")
    else:
        print("Nothing to update.")

    return specialization

def delete(self, specialization_id):
    specialization = self.get(specialization_id)
    if not specialization:
        print("Specialization not found.")
        return

    self.session.delete(specialization)
    self.session.commit()
    return specialization

def get_by_name(self, name: str):
    return self.session.query(Specialization).filter(Specialization.name == name).first()
