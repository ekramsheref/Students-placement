# services/faculty_service.py

from sqlalchemy.orm import Session

from backend.database.models import Faculty


class FacultyService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name):
        # create a sesion
        new_faculty = Faculty(name=name)
        self.session.add(new_faculty)
        self.session.commit()
        return new_faculty

    def get(self, faculty_id):
        return self.session.get(Faculty, faculty_id)  # or self.session.query(Faculty).get(faculty_id)

    def get_all(self):
        return self.session.query(Faculty).all()

    def update(self, faculty_id, name=None):
        faculty = self.get(faculty_id)
        if not faculty:
            print("Faculty not found.")
            return None

        updated = False

        if name is not None:
            faculty.name = name
            updated = True

        if updated:
            self.session.commit()
            print("Faculty updated successfully.")
        else:
            print("Nothing to update.")

        return faculty

    def delete(self, faculty_id):
        faculty = self.get(faculty_id)
        if not faculty:
            print("Faculty not found.")
            return

        if faculty:
            self.session.delete(faculty)
            self.session.commit()
        return faculty
