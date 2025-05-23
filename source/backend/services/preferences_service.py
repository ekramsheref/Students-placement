from sqlalchemy.orm import Session
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.database.models import Preferences
from sqlalchemy import func


class PreferencesService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name, student_id, preference_order, department_id=None, program_id=None, specialization_id=None):
        new_preference = Preferences(
            name=name,
            student_id=student_id,
            # project_id=project_id,
            preference_order=preference_order,
            department_id=department_id,
            program_id=program_id,
            specialization_id=specialization_id
        )
        self.session.add(new_preference)
        self.session.commit()
        return new_preference

    def get(self, preference_id):
        return self.session.get(Preferences, preference_id)

    def get_all(self):
        return self.session.query(Preferences).all()

    def update(self, preference_id, name=None, student_id=None, project_id=None, preference_order=None, department_id=None, program_id=None, specialization_id=None):
        preference = self.get(preference_id)
        if not preference:
            print("Preference not found.")
            return None

        updated = False

        if name is not None:
            preference.name = name
            updated = True
        if student_id is not None:
            preference.student_id = student_id
            updated = True
        if project_id is not None:
            preference.project_id = project_id
            updated = True
        if preference_order is not None:
            preference.preference_order = preference_order
            updated = True
        if department_id is not None:
            preference.department_id = department_id
            updated = True
        if program_id is not None:
            preference.program_id = program_id
            updated = True
        if specialization_id is not None:
            preference.specialization_id = specialization_id
            updated = True

        if updated:
            self.session.commit()
            print("Preference updated successfully.")
        else:
            print("Nothing to update.")

        return preference

    def delete(self, preference_id):
        preference = self.get(preference_id)
        if not preference:
            print("Preference not found.")
            return

        self.session.delete(preference)
        self.session.commit()
        return preference

    def add_df(self, df):
        new_prefrences= []
        for _, row in df.iterrows():
            new_prefrence = Preferences(
                student_id_num=row["id"],
                name=row["preference"],
                preference_order=row["preference_order"],
            )
            new_prefrences.append(new_prefrence)
        self.session.add_all(new_prefrences)
        self.session.commit()

    def get_first_preference_percentages(self):
        # Get total number of distinct students
        total_students = self.session.query(func.count(Preferences.student_id_num.distinct())).scalar()

        # Query the preferences for the first preference counts grouped by project name
        first_preferences = self.session.query(
            Preferences.name,
            func.count(Preferences.student_id_num.distinct()).label('first_choice_count')
        ).filter(
            Preferences.preference_order == 1
        ).group_by(
            Preferences.name
        ).all()

        # Calculate percentages and build result dictionary
        percentages = {}
        for preference in first_preferences:
            if total_students > 0:
                percentages[preference.name] = (preference.first_choice_count / total_students) * 100
            else:
                percentages[preference.name] = 0.0

        return percentages
