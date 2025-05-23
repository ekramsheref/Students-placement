# services/department_service.py
from sqlalchemy.orm import Session
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.database.models import Department


class DepartmentService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name):
        new_department = Department(
            name=name,
           
        )
        self.session.add(new_department)
        self.session.commit()
        return new_department

    def get(self, department_id):
        return self.session.get(Department, department_id)

    def get_all(self):
        return self.session.query(Department).all()

    def update(self, department_id, name=None):
        department = self.get(department_id)
        if not department:
            print("Department not found.")
            return None

        updated = False

        if name is not None:
            department.name = name
            updated = True


        if updated:
            self.session.commit()
            print("Department updated successfully.")
        else:
            print("Nothing to update.")

        return department

    def delete(self, department_id):
        department = self.get(department_id)
        if not department:
            print("Department not found.")
            return

        self.session.delete(department)
        self.session.commit()
        print("Department deleted successfully.")
        return department

    def get_by_username(self, name: str):
        return self.session.query(Department).filter(Department.name == name).first()