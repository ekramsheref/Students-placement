# services/department_head_service.py

from sqlalchemy.orm import Session
from backend.database.models import DepartmentHead, Person

class DepartmentHeadService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, first_name, last_name, ssn, email, phone_number, department_id):
        # Create a new Person
        new_person = Person(
            first_name=first_name,
            last_name=last_name,
            ssn=ssn,
            email=email,
            phone_number=phone_number
        )
        self.session.add(new_person)
        self.session.flush()  # Flush to get the new_person.id

        # Create a new DepartmentHead linked to the Person
        new_department_head = DepartmentHead(
            person_id=new_person.id,
            department_id=department_id
        )
        self.session.add(new_department_head)
        self.session.commit()
        return new_department_head

    def get(self, department_head_id):
        return self.session.get(DepartmentHead, department_head_id)

    def get_all(self):
        return self.session.query(DepartmentHead).all()

    def update(self, department_head_id, first_name=None, last_name=None, ssn=None, email=None, phone_number=None, department_id=None):
        department_head = self.get(department_head_id)
        if not department_head:
            print("Department Head not found.")
            return None

        updated = False

        # Update Person details
        if first_name is not None:
            department_head.person.first_name = first_name
            updated = True
        if last_name is not None:
            department_head.person.last_name = last_name
            updated = True
        if ssn is not None:
            department_head.person.ssn = ssn
            updated = True
        if email is not None:
            department_head.person.email = email
            updated = True
        if phone_number is not None:
            department_head.person.phone_number = phone_number
            updated = True

        # Update DepartmentHead details
        if department_id is not None:
            department_head.department_id = department_id
            updated = True

        if updated:
            self.session.commit()
            print("Department Head updated successfully.")
        else:
            print("Nothing to update.")

        return department_head

    def delete(self, department_head_id):
        department_head = self.get(department_head_id)
        if not department_head:
            print("Department Head not found.")
            return

        # Deleting the department head will also delete the associated person due to cascade settings
        self.session.delete(department_head)
        self.session.commit()
        return department_head
