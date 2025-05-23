from sqlalchemy.orm import Session
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.database.models import Admin


class AdminService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name, username, password, role):
        # Create a new Admin
        new_admin = Admin(
            name=name,
            username=username,
            role=role
        )
        new_admin.set_password(password)
        self.session.add(new_admin)
        self.session.commit()
        return new_admin

    def get(self, admin_id):
        return self.session.get(Admin, admin_id)

    def get_all(self):
        return self.session.query(Admin).all()

    def update(self, admin_id, name=None, username=None, password=None, role=None):
        admin = self.get(admin_id)
        if not admin:
            raise ValueError("الأدمن غير موجود.")

        # التحقق من تكرار username
        if username is not None and username != admin.username:
            existing_admin = self.get_by_username(username)
            if existing_admin:
                raise ValueError("اسم المستخدم موجود بالفعل.")
            admin.username = username

        if name is not None:
            admin.name = name
        if password is not None:
            admin.set_password(password)
        if role is not None:
            admin.role = role

        self.session.commit()
        return admin

    def delete(self, admin_id):
        admin = self.get(admin_id)
        if not admin:
            raise ValueError("الأدمن غير موجود.")
        self.session.delete(admin)
        self.session.commit()
        return admin

    def login(self, username, password):
        admin = self.session.query(Admin).filter_by(username=username).first()
        if admin and admin.check_password(password):
            return admin.role
        raise ValueError("اسم المستخدم أو كلمة المرور غير صحيحة.")

    def get_by_username(self, username: str):
        return self.session.query(Admin).filter(Admin.username == username).first()