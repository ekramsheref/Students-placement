#main_f.py
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QProgressBar, QLineEdit, QMessageBox, QInputDialog, QDialog, 
    QComboBox, QSizePolicy, QFileDialog, QSpinBox, QFormLayout, QDoubleSpinBox
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.services.student_service import StudentService
from backend.services.admin_service import AdminService
from backend.services.department_service import DepartmentService
from backend.services.program_service import ProgramService
from backend.services.specialization_service import SpecializationService
from backend.services.preferences_service import PreferencesService
from backend.database.database_config import get_session
from backend.services.project_service import ProjectInfoService, ProjectManager
from backend.process.assignment_process import AssignmentProcess
from backend.services.student_assignment_service import StudentAssignmentService
import bcrypt
from frontend.login import LoginWindow
from backend.database.models import Admin
import pandas as pd
from pathlib import Path
def resource_path(relative_path):
    """
    ترجع المسار الصحيح للملف سواء داخل .exe أو خلال التطوير
    """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)
def set_password(password):
    """
    دالة لتشفير كلمة المرور باستخدام bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

class SelectAdminDialog(QDialog):
    def __init__(self, session, title, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle(title)
        self.setStyleSheet("background-color: #00234E; color: white;")
        self.resize(400, 200)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        label = QLabel("اختر الأدمن:")
        label.setFont(QFont("Arial", 14))
        layout.addWidget(label)

        self.admin_combo = QComboBox()
        self.admin_combo.setStyleSheet("font-size: 16px; padding: 8px; background-color:white ; color: #1E1E1E; border-radius: 10px;")
        self.admin_combo.setFixedWidth(300)
        layout.addWidget(self.admin_combo)

        select_button = QPushButton("تحديد")
        select_button.setStyleSheet("""
            background-color: #FDC400;
            color: black;
            font-size: 18px;
            padding: 10px;
            border-radius: 20px;
        """)
        select_button.clicked.connect(self.accept)
        layout.addWidget(select_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.load_admins()

    def load_admins(self):
        try:
            admin_service = AdminService(self.session)
            admins = admin_service.get_all()
            if admins:
                self.admin_combo.addItems([admin.username for admin in admins])
            else:
                QMessageBox.warning(self, "تنبيه", "لا يوجد أدمن متاحون.")
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء تحميل قائمة الأدمن:\n{e}")
            self.close()

    def get_selected_admin(self):
        return self.admin_combo.currentText()

class EditSelectionWindow(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("اختيار عنصر للتعديل")
        self.setStyleSheet("background-color: #00234E; color: white;")
        self.resize(500, 350)

        self.department_service = DepartmentService(self.session)
        self.program_service = ProgramService(self.session)
        self.specialization_service = SpecializationService(self.session)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["قسم", "برنامج", "تخصص"])
        self.type_combo.setStyleSheet("font-size: 16px; padding: 8px; background-color:white ; color:#1E1E1E ; border-radius: 10px;")
        self.type_combo.setFixedWidth(300)
        self.type_combo.currentIndexChanged.connect(self.update_item_combo)
        layout.addWidget(QLabel("اختر النوع:"))
        layout.addWidget(self.type_combo)

        self.item_combo = QComboBox()
        self.item_combo.setStyleSheet("font-size: 16px; padding: 8px; background-color:white ; color:#1E1E1E ; border-radius: 10px;")
        self.item_combo.setFixedWidth(300)
        layout.addWidget(QLabel("اختر العنصر:"))
        layout.addWidget(self.item_combo)

        select_button = QPushButton("تحديد")
        select_button.setStyleSheet("background-color: #FDC400; color: black; font-size: 18px; padding: 10px; border-radius: 20px;")
        select_button.clicked.connect(self.open_edit_form)
        layout.addWidget(select_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.update_item_combo()

    def update_item_combo(self):
        self.item_combo.clear()
        selected_type = self.type_combo.currentText()
        
        if selected_type == "قسم":
            items = self.department_service.get_all()
            self.item_combo.addItems([item.name for item in items])
            self.item_combo.setProperty("items", [(item.id, item.name) for item in items])
        elif selected_type == "برنامج":
            items = self.program_service.get_all()
            self.item_combo.addItems([item.name for item in items])
            self.item_combo.setProperty("items", [(item.id, item.name) for item in items])
        elif selected_type == "تخصص":
            items = self.specialization_service.get_all()
            self.item_combo.addItems([item.name for item in items])
            self.item_combo.setProperty("items", [(item.id, item.name) for item in items])

    def open_edit_form(self):
        selected_type = self.type_combo.currentText()
        selected_item_name = self.item_combo.currentText()
        
        if not selected_item_name:
            QMessageBox.warning(self, "خطأ", "يرجى اختيار عنصر للتعديل.")
            return

        items = self.item_combo.property("items")
        selected_item_id = next((item[0] for item in items if item[1] == selected_item_name), None)

        if selected_item_id is None:
            QMessageBox.critical(self, "خطأ", "لم يتم العثور على العنصر المحدد.")
            return

        if selected_type == "قسم":
            self.edit_form = DepartmentEditForm(self.session, selected_item_id, self)
        elif selected_type == "برنامج":
            self.edit_form = ProgramEditForm(self.session, selected_item_id, self)
        elif selected_type == "تخصص":
            self.edit_form = SpecializationEditForm(self.session, selected_item_id, self)
        
        self.edit_form.exec()

class DepartmentEditForm(QDialog):
    def __init__(self, session, department_id, parent=None):
        super().__init__(parent)
        self.session = session
        self.department_id = department_id
        self.department_service = DepartmentService(self.session)
        self.setWindowTitle("تعديل بيانات القسم")
        self.setStyleSheet("background-color: #00234E; color: white;")
        self.resize(400, 200)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        form_frame = QFrame()
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        name_label = QLabel("اسم القسم:")
        name_label.setFont(QFont("Arial", 14))
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)

        save_button = QPushButton("حفظ التعديلات")
        save_button.setStyleSheet("""
            background-color: #FDC400;
            color: black;
            font-size: 18px;
            padding: 10px;
            border-radius: 20px;
        """)
        save_button.clicked.connect(self.save_department)
        form_layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        self.setLayout(layout)

        self.load_department_data()

    def load_department_data(self):
        department = self.department_service.get(self.department_id)
        if department:
            self.name_input.setText(department.name)
        else:
            QMessageBox.warning(self, "خطأ", "القسم غير موجود.")
            self.close()

    def save_department(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم القسم.")
            return

        try:
            self.department_service.update(self.department_id, name=name)
            QMessageBox.information(self, "تم", "تم تعديل بيانات القسم بنجاح.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل تعديل بيانات القسم:\n{e}")

class ProgramEditForm(QDialog):
    def __init__(self, session, program_id, parent=None):
        super().__init__(parent)
        self.session = session
        self.program_id = program_id
        self.program_service = ProgramService(self.session)
        self.department_service = DepartmentService(self.session)
        self.setWindowTitle("تعديل بيانات البرنامج")
        self.setStyleSheet("background-color: #00234E; color: white;")
        self.resize(500, 400)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        form_frame = QFrame()
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        name_label = QLabel("اسم البرنامج:")
        name_label.setFont(QFont("Arial", 14))
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)

        dept_label = QLabel("القسم:")
        dept_label.setFont(QFont("Arial", 14))
        self.department_combo = QComboBox()
        self.department_combo.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        departments = self.department_service.get_all()
        self.department_combo.addItems([dept.name for dept in departments])
        self.department_combo.setProperty("departments", [(dept.id, dept.name) for dept in departments])
        form_layout.addWidget(dept_label)
        form_layout.addWidget(self.department_combo)

        gpa_label = QLabel("الحد الأدنى للمعدل:")
        gpa_label.setFont(QFont("Arial", 14))
        self.gpa_input = QDoubleSpinBox()
        self.gpa_input.setRange(0.0, 4.0)
        self.gpa_input.setDecimals(2)
        self.gpa_input.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        form_layout.addWidget(gpa_label)
        form_layout.addWidget(self.gpa_input)

        capacity_label = QLabel("السعة الطلابية:")
        capacity_label.setFont(QFont("Arial", 14))
        self.capacity_input = QSpinBox()
        self.capacity_input.setRange(1, 1000)
        self.capacity_input.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        form_layout.addWidget(capacity_label)
        form_layout.addWidget(self.capacity_input)

        subject1_label = QLabel("المادة الأولى (اختياري) - الكود ودرجة الحد الأدنى:")
        subject1_label.setFont(QFont("Arial", 14))
        self.subject1_code = QLineEdit()
        self.subject1_code.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        self.subject1_grade = QSpinBox()
        self.subject1_grade.setRange(0, 100)
        self.subject1_grade.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        subject1_layout = QHBoxLayout()
        subject1_layout.addWidget(self.subject1_code)
        subject1_layout.addWidget(self.subject1_grade)
        form_layout.addWidget(subject1_label)
        form_layout.addLayout(subject1_layout)

        subject2_label = QLabel("المادة الثانية (اختياري) - الكود ودرجة الحد الأدنى:")
        subject2_label.setFont(QFont("Arial", 14))
        self.subject2_code = QLineEdit()
        self.subject2_code.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        self.subject2_grade = QSpinBox()
        self.subject2_grade.setRange(0, 100)
        self.subject2_grade.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        subject2_layout = QHBoxLayout()
        subject2_layout.addWidget(self.subject2_code)
        subject2_layout.addWidget(self.subject2_grade)
        form_layout.addWidget(subject2_label)
        form_layout.addLayout(subject2_layout)

        save_button = QPushButton("حفظ التعديلات")
        save_button.setStyleSheet("""
            background-color: #FDC400;
            color: black;
            font-size: 18px;
            padding: 10px;
            border-radius: 20px;
        """)
        save_button.clicked.connect(self.save_program)
        form_layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        self.setLayout(layout)

        self.load_program_data()

    def load_program_data(self):
        program = self.program_service.get(self.program_id)
        if program:
            self.name_input.setText(program.name)
            departments = self.department_combo.property("departments")
            for dept_id, dept_name in departments:
                if dept_id == program.department_id:
                    self.department_combo.setCurrentText(dept_name)
                    break
            self.gpa_input.setValue(float(program.gpa_threshold) if program.gpa_threshold else 0.0)
            self.capacity_input.setValue(int(program.student_capacity) if program.student_capacity else 1)
            subjects = {subject.code: subject.min_grade for subject in program.subjects_required}
            subject_list = list(subjects.items())
            if len(subject_list) > 0:
                self.subject1_code.setText(subject_list[0][0])
                self.subject1_grade.setValue(subject_list[0][1])
            if len(subject_list) > 1:
                self.subject2_code.setText(subject_list[1][0])
                self.subject2_grade.setValue(subject_list[1][1])
        else:
            QMessageBox.warning(self, "خطأ", "البرنامج غير موجود.")
            self.close()

    def save_program(self):
        name = self.name_input.text().strip()
        department_name = self.department_combo.currentText()
        gpa = self.gpa_input.value()
        capacity = self.capacity_input.value()
        subject1_code = self.subject1_code.text().strip()
        subject1_grade = self.subject1_grade.value()
        subject2_code = self.subject2_code.text().strip()
        subject2_grade = self.subject2_grade.value()

        if not name or not department_name:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم البرنامج واختيار قسم.")
            return

        departments = self.department_combo.property("departments")
        department_id = next((dept[0] for dept in departments if dept[1] == department_name), None)
        if not department_id:
            QMessageBox.warning(self, "خطأ", "القسم المحدد غير موجود.")
            return

        gpa_value = float(gpa) if gpa > 0 else None
        capacity_value = int(capacity) if capacity > 0 else None

        subjects_dict = {}
        if subject1_code:
            subjects_dict[subject1_code] = subject1_grade
        if subject2_code:
            subjects_dict[subject2_code] = subject2_grade

        try:
            self.program_service.update(
                self.program_id,
                name=name,
                department_id=department_id,
                gpa_threshold=gpa_value,
                student_capacity=capacity_value,
                subjects_required=subjects_dict if subjects_dict else None
            )
            QMessageBox.information(self, "تم", "تم تعديل بيانات البرنامج بنجاح.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل تعديل بيانات البرنامج:\n{e}")

class SpecializationEditForm(QDialog):
    def __init__(self, session, specialization_id, parent=None):
        super().__init__(parent)
        self.session = session
        self.specialization_id = specialization_id
        self.specialization_service = SpecializationService(self.session)
        self.program_service = ProgramService(self.session)
        self.setWindowTitle("تعديل بيانات التخصص")
        self.setStyleSheet("background-color: #00234E; color: white;")
        self.resize(500, 400)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        form_frame = QFrame()
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        name_label = QLabel("اسم التخصص:")
        name_label.setFont(QFont("Arial", 14))
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)

        program_label = QLabel("البرنامج:")
        program_label.setFont(QFont("Arial", 14))
        self.program_combo = QComboBox()
        self.program_combo.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        programs = self.program_service.get_all()
        self.program_combo.addItems([prog.name for prog in programs])
        self.program_combo.setProperty("programs", [(prog.id, prog.name) for prog in programs])
        form_layout.addWidget(program_label)
        form_layout.addWidget(self.program_combo)

        gpa_label = QLabel("الحد الأدنى للمعدل:")
        gpa_label.setFont(QFont("Arial", 14))
        self.gpa_input = QDoubleSpinBox()
        self.gpa_input.setRange(0.0, 4.0)
        self.gpa_input.setDecimals(2)
        self.gpa_input.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        form_layout.addWidget(gpa_label)
        form_layout.addWidget(self.gpa_input)

        capacity_label = QLabel("السعة الطلابية:")
        capacity_label.setFont(QFont("Arial", 14))
        self.capacity_input = QSpinBox()
        self.capacity_input.setRange(1, 1000)
        self.capacity_input.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        form_layout.addWidget(capacity_label)
        form_layout.addWidget(self.capacity_input)

        subject1_label = QLabel("المادة الأولى (اختياري) - الكود ودرجة الحد الأدنى:")
        subject1_label.setFont(QFont("Arial", 14))
        self.subject1_code = QLineEdit()
        self.subject1_code.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        self.subject1_grade = QSpinBox()
        self.subject1_grade.setRange(0, 100)
        self.subject1_grade.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        subject1_layout = QHBoxLayout()
        subject1_layout.addWidget(self.subject1_code)
        subject1_layout.addWidget(self.subject1_grade)
        form_layout.addWidget(subject1_label)
        form_layout.addLayout(subject1_layout)

        subject2_label = QLabel("المادة الثانية (اختياري) - الكود ودرجة الحد الأدنى:")
        subject2_label.setFont(QFont("Arial", 14))
        self.subject2_code = QLineEdit()
        self.subject2_code.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        self.subject2_grade = QSpinBox()
        self.subject2_grade.setRange(0, 100)
        self.subject2_grade.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        subject2_layout = QHBoxLayout()
        subject2_layout.addWidget(self.subject2_code)
        subject2_layout.addWidget(self.subject2_grade)
        form_layout.addWidget(subject2_label)
        form_layout.addLayout(subject2_layout)

        save_button = QPushButton("حفظ التعديلات")
        save_button.setStyleSheet("""
            background-color: #FDC400;
            color: black;
            font-size: 18px;
            padding: 10px;
            border-radius: 20px;
        """)
        save_button.clicked.connect(self.save_specialization)
        form_layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        self.setLayout(layout)

        self.load_specialization_data()

    def load_specialization_data(self):
        specialization = self.specialization_service.get(self.specialization_id)
        if specialization:
            self.name_input.setText(specialization.name)
            programs = self.program_combo.property("programs")
            for prog_id, prog_name in programs:
                if prog_id == specialization.program_id:
                    self.program_combo.setCurrentText(prog_name)
                    break
            self.gpa_input.setValue(float(specialization.gpa_threshold) if specialization.gpa_threshold else 0.0)
            self.capacity_input.setValue(int(specialization.student_capacity) if specialization.student_capacity else 1)
            subjects = {subject.code: subject.min_grade for subject in specialization.subjects_required}
            subject_list = list(subjects.items())
            if len(subject_list) > 0:
                self.subject1_code.setText(subject_list[0][0])
                self.subject1_grade.setValue(subject_list[0][1])
            if len(subject_list) > 1:
                self.subject2_code.setText(subject_list[1][0])
                self.subject2_grade.setValue(subject_list[1][1])
        else:
            QMessageBox.warning(self, "خطأ", "التخصص غير موجود.")
            self.close()

    def save_specialization(self):
        name = self.name_input.text().strip()
        program_name = self.program_combo.currentText()
        gpa = self.gpa_input.value()
        capacity = self.capacity_input.value()
        subject1_code = self.subject1_code.text().strip()
        subject1_grade = self.subject1_grade.value()
        subject2_code = self.subject2_code.text().strip()
        subject2_grade = self.subject2_grade.value()

        if not name or not program_name:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم التخصص واختيار برنامج.")
            return

        programs = self.program_combo.property("programs")
        program_id = next((prog[0] for prog in programs if prog[1] == program_name), None)
        if not program_id:
            QMessageBox.warning(self, "خطأ", "البرنامج المحدد غير موجود.")
            return

        gpa_value = float(gpa) if gpa > 0 else None
        capacity_value = int(capacity) if capacity > 0 else None

        subjects_dict = {}
        if subject1_code:
            subjects_dict[subject1_code] = subject1_grade
        if subject2_code:
            subjects_dict[subject2_code] = subject2_grade

        try:
            self.specialization_service.update(
                self.specialization_id,
                name=name,
                program_id=program_id,
                gpa_threshold=gpa_value,
                student_capacity=capacity_value,
                subjects_required_dict=subjects_dict if subjects_dict else None
            )
            QMessageBox.information(self, "تم", "تم تعديل بيانات التخصص بنجاح.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل تعديل بيانات التخصص:\n{e}")

class StudentEditPage(QWidget):
    def __init__(self, student_id, session, parent=None):
        super().__init__(parent)
        self.student_id = student_id
        self.session = session
        self.setWindowTitle("تعديل بيانات طالب")
        self.setStyleSheet("background-color: #00234E; color: white;")
        self.resize(600, 500)

        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        outer_layout.setContentsMargins(0, 40, 0, 20)
        outer_layout.setSpacing(20)

        form_frame = QFrame()
        form_frame.setFixedWidth(500)
        center_layout = QHBoxLayout()
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(18)

        self.id_num_input = QLineEdit()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.gpa_input = QLineEdit()
        self.preferences_input = QLineEdit()

        inputs = [
            ("رقم الطالب:", self.id_num_input),
            ("الاسم:", self.name_input),
            ("الإيميل:", self.email_input),
            (":GPA          ", self.gpa_input),
            ("التفضيلات:", self.preferences_input),
        ]

        for label_text, field in inputs:
            row = QHBoxLayout()
            row.setSpacing(10)
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 14))
            label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            label.setFixedWidth(100)
            field.setAlignment(Qt.AlignmentFlag.AlignRight)
            field.setStyleSheet("font-size: 16px; padding: 6px;")
            field.setFixedWidth(280)
            row.addWidget(field)
            row.addWidget(label)
            form_layout.addLayout(row)

        save_button = QPushButton("تحديث البيانات")
        save_button.setStyleSheet("background-color: #FDC400; color: black; font-size: 18px; padding: 10px; border-radius: 20px;")
        save_button.clicked.connect(self.update_student)
        form_layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        form_frame.setLayout(form_layout)
        center_layout.addWidget(form_frame)
        outer_layout.addLayout(center_layout)
        self.setLayout(outer_layout)
        self.load_student_data()

    def load_student_data(self):
        try:
            student_service = StudentService(self.session)
            db_path = self.session.bind.url if self.session.bind else "Unknown"
            print(f"Debug: Loading student data from database {db_path}")
            self.student = student_service.get(self.student_id)
            if self.student:
                self.id_num_input.setText(str(self.student.id_num))
                self.name_input.setText(self.student.name)
                self.email_input.setText(self.student.email)
                self.gpa_input.setText(str(self.student.gpa))
                try:
                    preferences = [pref.name for pref in getattr(self.student, 'preferences', [])]
                    self.preferences_input.setText(",".join(preferences) if preferences else "")
                except Exception as pref_error:
                    print(f"Debug: Error loading preferences: {pref_error}")
                    self.preferences_input.setText("")
            else:
                QMessageBox.warning(self, "تنبيه", f"الطالب برقم {self.student_id} غير موجود.")
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء تحميل بيانات الطالب:\n{e}\nتأكد من أن قاعدة البيانات تحتوي على جدول 'student' وأن المشروع محمل بشكل صحيح.")
            self.close()

    def update_student(self):
        id_num = self.id_num_input.text().strip()
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        gpa = self.gpa_input.text().strip()
        preferences = self.preferences_input.text().strip()

        if not id_num or not name or not email or not gpa:
            QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول (رقم الطالب، الاسم، الإيميل، GPA).")
            return

        if not gpa.replace('.', '', 1).isdigit():
            QMessageBox.warning(self, "خطأ", "الـ GPA يجب أن يكون رقمًا.")
            return

        preference_names = [pref.strip() for pref in preferences.split(",") if pref.strip()] if preferences else None

        try:
            student_service = StudentService(self.session)
            db_path = self.session.bind.url if self.session.bind else "Unknown"
            print(f"Debug: Updating student data in database {db_path}")
            student_service.update(
                student_id=self.student_id,
                id_num=id_num,
                name=name,
                email=email,
                gpa=float(gpa),
                preference_names=preference_names
            )
            QMessageBox.information(self, "تم التحديث", "✅ تم تعديل بيانات الطالب بنجاح.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء تحديث البيانات:\n{e}\nتأكد من أن قاعدة البيانات تحتوي على جدول 'student' وأن المشروع محمل بشكل صحيح.")
            self.close()

class AddAdminForm(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("إضافة أدمن")
        self.setStyleSheet("background-color: #00234E; color: white;")
        self.resize(500, 400)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("اسم")
        self.name_input.setStyleSheet("font-size: 16px; padding: 8px; background-color:white ; color:#1E1E1E ; border-radius: 10px;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")
        self.username_input.setStyleSheet("font-size: 16px; padding: 8px; background-color:white ; color:#1E1E1E ; border-radius: 10px;")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("كلمة المرور")
        self.password_input.setStyleSheet("font-size: 16px; padding: 8px; background-color: white; color: #1E1E1E; border-radius: 10px;")

        self.role_input = QComboBox()
        self.role_input.addItems(["admin", "system admin"])
        self.role_input.setStyleSheet("font-size: 16px; padding: 8px; background-color:white ; color:#1E1E1E ; border-radius: 10px;")

        add_button = QPushButton("إضافة أدمن")
        add_button.setStyleSheet("""
            background-color: #FDC400;
            color: black;
            font-size: 18px;
            padding: 12px;
            border-radius: 10px;
        """)
        add_button.clicked.connect(self.add_admin)

        layout.addWidget(self.name_input)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.role_input)
        layout.addWidget(add_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def add_admin(self):
        name = self.name_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_input.currentText()

        if not username or not password:
            QMessageBox.warning(self, "خطأ", "من فضلك أكمل جميع الحقول.")
            return

        try:
            with get_session(source="user") as session:
                admin_service = AdminService(session)
                admin_service.create(name=name, username=username, password=password, role=role)
                session.commit()
                QMessageBox.information(self, "تم الإضافة", "تم إضافة الأدمن بنجاح.")
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء إضافة الأدمن:\n{e}")

class EditAdminForm(QDialog):
    def __init__(self, session, admin_id, parent=None):
        super().__init__(parent)
        self.session = session
        self.admin_id = admin_id  # تغيير من username إلى admin_id
        self.setWindowTitle("تعديل بيانات الأدمن")
        self.setStyleSheet("background-color: #00234E; color: white;")
        self.resize(500, 400)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("اسم الأدمن")
        self.name_input.setStyleSheet("font-size: 16px; padding: 8px; background-color:white ; color:#1E1E1E ; border-radius: 10px;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")
        self.username_input.setStyleSheet("font-size: 16px; padding: 8px; background-color:white ; color:#1E1E1E ; border-radius: 10px;")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("كلمة المرور (اتركها فارغة لعدم التغيير)")
        self.password_input.setStyleSheet("font-size: 16px; padding: 8px; background-color:white ; color:#1E1E1E ; border-radius: 10px;")

        self.role_input = QComboBox()
        self.role_input.addItems(["admin", "system admin"])
        self.role_input.setStyleSheet("font-size: 16px; padding: 8px; background-color:white ; color:#1E1E1E ; border-radius: 10px;")

        save_button = QPushButton("حفظ التعديلات")
        save_button.setStyleSheet("""
            background-color: #FDC400;
            color: black;
            font-size: 18px;
            padding: 12px;
            border-radius: 10px;
        """)
        save_button.clicked.connect(self.save_admin)

        layout.addWidget(self.name_input)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.role_input)
        layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

        if admin_id:
            self.load_admin_data(admin_id)

    def load_admin_data(self, admin_id):
        try:
            admin_service = AdminService(self.session)
            admin = admin_service.get(admin_id)
            if admin:
                self.name_input.setText(admin.name or "")
                self.username_input.setText(admin.username or "")
                self.role_input.setCurrentText(admin.role or "admin")
            else:
                QMessageBox.warning(self, "خطأ", "الأدمن غير موجود.")
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء تحميل بيانات الأدمن:\n{e}")
            self.close()

    def save_admin(self):
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_input.currentText()

        if not username or not name:
            QMessageBox.warning(self, "خطأ", "من فضلك أكمل جميع الحقول.")
            return

        try:
            admin_service = AdminService(self.session)
            admin_service.update(
                admin_id=self.admin_id,
                name=name,
                username=username,
                password=password if password else None,
                role=role
            )
            self.session.commit()
            QMessageBox.information(self, "تم التحديث", "تم تعديل بيانات الأدمن بنجاح.")
            self.close()
        except ValueError as ve:
            QMessageBox.warning(self, "خطأ", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء تعديل الأدمن:\n{e}")

class StudentPlacement(QWidget):
    def __init__(self, user_name="Dr.Eman", role="system admin", session=None):
        super().__init__()
        self.user_name = user_name
        self.role = role  # إضافة الدور
        self.session = session
        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        self.setWindowTitle("Student Placement")
        main_layout = QHBoxLayout()
        content_layout = QVBoxLayout()

        header = self.create_header()
        content_background = QFrame()
        content_background.setStyleSheet("background-color: #D3D3D3; padding: 10px; border-radius: 10px;")
        content_background_layout = QHBoxLayout(content_background)

        stats_section = self.create_stats_section()
        middle_col = self.create_middle_col()
        right_col = self.create_right_col()

        content_background_layout.addWidget(stats_section, 1)
        content_background_layout.addWidget(middle_col, 1)
        content_background_layout.addWidget(right_col, 1)

        content_layout.addWidget(header)
        content_background.setLayout(content_background_layout)
        content_layout.addWidget(content_background)

        sidebar = self.create_sidebar()
        main_layout.addLayout(content_layout)
        main_layout.addWidget(sidebar)

        self.setLayout(main_layout)

    def run_assignment_process(self):
        try:
            print("Debug: Attempting to run AssignmentProcess")
            pm = ProjectManager()
            path = pm.get_project_path()
            print(f"Debug: Project path retrieved: {path}")
            with get_session(source="database", project_path=str(path)) as session:
                print("Debug: Database session created")
                student_service = StudentService(session)
                program_service = ProgramService(session)
                specialization_service = SpecializationService(session)
                department_service = DepartmentService(session)
                project_service = ProjectInfoService(session)

                assignment_process = AssignmentProcess(
                    student_service=student_service,
                    program_service=program_service,
                    specialization_service=specialization_service,
                    department_service=department_service,
                    project_service=project_service
                )
                print("Debug: AssignmentProcess instance created")
                assignment_process.assign_students()
                print("Debug: assign_students completed")
                QMessageBox.information(self, "تم", "تم تشعيب الطلاب بنجاح.")
        except Exception as e:
            print(f"Debug: Exception occurred: {e}")
            QMessageBox.critical(self, "خطأ", f"فشل تشعيب الطلاب:\n{e}")

    def open_edit_student_dialog(self):
        student_id, ok = QInputDialog.getText(self, "تعديل طالب", "ادخل رقم الطالب:")
        if ok and student_id.isdigit():
            try:
                self.edit_window = StudentEditPage(int(student_id), self.session)
                self.edit_window.show()
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"فشل فتح نافذة تعديل الطالب:\n{e}\nتأكد من أن قاعدة البيانات تحتوي على جدول 'student' وأن المشروع محمل بشكل صحيح.")
        elif ok:
            QMessageBox.warning(self, "خطأ", "من فضلك ادخل رقم صحيح للطالب.")

    def open_edit_selection_window(self):
        try:
            self.edit_selection_window = EditSelectionWindow(self.session, self)
            self.edit_selection_window.exec()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل فتح نافذة اختيار التعديل:\n{e}")

    def open_add_delete_page(self):
        try:
            print("Debug: Attempting to open AddDeletePage")
            from frontend.ae import AddDeletePage
            print("Debug: Successfully imported AddDeletePage")
            pm = ProjectManager()
            path = pm.get_project_path()
            print(f"Debug: Project path retrieved: {path}")
            with get_session(source="database", project_path=str(path)) as session:
                print("Debug: Database session created")
                project_service = ProjectInfoService(session)
                try:
                    project_info = project_service.get_project_info()
                    ptype = project_info.ptype if project_info else "department"
                except AttributeError as ae:
                    print(f"Debug: AttributeError in get_project_info: {ae}")
                    ptype = "department"
                print(f"Debug: ptype determined: {ptype}")
                self.add_delete_window = AddDeletePage(user_name=self.user_name, session=session, ptype=ptype)
                print("Debug: AddDeletePage instance created")
                self.add_delete_window.show()
                print("Debug: AddDeletePage show() called")
                self.close()
                print("Debug: StudentPlacement window closed")
        except Exception as e:
            print(f"Debug: Exception occurred: {e}")
            QMessageBox.critical(self, "خطأ", f"فشل فتح نافذة الإضافة/الحذف:\n{e}")

    def open_add_delete_student_page(self):
        try:
            print("Debug: Attempting to open AddDeleteStudentPage")
            from frontend.ae_student import AddDeleteStudentPage
            print("Debug: Successfully imported AddDeleteStudentPage")
            pm = ProjectManager()
            path = pm.get_project_path()
            print(f"Debug: Project path retrieved: {path}")
            with get_session(source="database", project_path=str(path)) as session:
                print("Debug: Database session created")
                self.add_delete_student_window = AddDeleteStudentPage(user_name=self.user_name, role=self.role, session=session)
                print("Debug: AddDeleteStudentPage instance created")
                self.add_delete_student_window.show()
                print("Debug: AddDeleteStudentPage show() called")
                self.close()
                print("Debug: StudentPlacement window closed")
        except Exception as e:
            print(f"Debug: Exception occurred: {e}")
            QMessageBox.critical(self, "خطأ", f"فشل فتح نافذة الإضافة/الحذف للطلاب:\n{e}")

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: #00234E; color: white;")
        sidebar.setFixedWidth(320)
        sidebar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(10, 20, 10, 20)

        profile_pic = QLabel()
        profile_pic.setPixmap(QPixmap(resource_path("frontend/images/image2_no_bg.png")).scaled(182, 182, Qt.AspectRatioMode.KeepAspectRatio))
        profile_pic.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(profile_pic)

        profile_label = QLabel(self.user_name)
        profile_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        profile_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(profile_label)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFixedHeight(2)
        line.setStyleSheet("background-color: #CFC996; border: none; margin-left: 20px; margin-right: 20px;")
        sidebar_layout.addWidget(line)

        buttons = [
            ("إضافة أدمن", resource_path("frontend/images/l2.png"), self.add_admin),
            ("تعديل أدمن", resource_path("frontend/images/l3.png"), self.edit_admin),
            ("حذف أدمن", resource_path("frontend/images/l1.png"), self.delete_admin)
        ]

        for text, icon_path, handler in buttons:
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(40, 40))
            btn.setStyleSheet(""" 
            QPushButton {
                color: white;
                font-size: 24px;
                background: none;
                border: none;
                padding-right: 100px;
                padding-top: 20px;
            }
            QPushButton:hover {
                color: yellow;
                font-size: 26px;
            }
        """)

            btn.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            btn.clicked.connect(handler)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        logout_btn = QPushButton("تسجيل الخروج")
        logout_btn.setIcon(QIcon(resource_path("frontend/images/icon3_new_no_bg.png")))
        logout_btn.setIconSize(QSize(64, 64))
        logout_btn.setStyleSheet("""
    QPushButton {
        color: white;
        font-size: 26px;
        background: none;
        border: none;
        text-align: right;
        padding-right: 100px;
    }
    QPushButton:hover {
        color: red;
    }
""")
        logout_btn.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        logout_btn.clicked.connect(self.logout)
        sidebar_layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignBottom)

        sidebar.setLayout(sidebar_layout)
        return sidebar

    def logout(self):
        if hasattr(self, 'session') and self.session:
            self.session.close()
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()

    def add_admin(self):
        self.add_admin_dialog = AddAdminForm(self.session, self)
        self.add_admin_dialog.exec()

    def edit_admin(self):
        with get_session(source="user") as session:
            dialog = SelectAdminDialog(session, "تعديل أدمن", self)
            if dialog.exec():
                username = dialog.get_selected_admin()
                if username:
                    admin_service = AdminService(session)
                    admin = admin_service.get_by_username(username)
                    if admin:
                        self.edit_admin_form = EditAdminForm(session, admin.id)  # تمرير admin.id
                        self.edit_admin_form.exec()
    def delete_admin(self):
        with get_session(source="user") as session:
            dialog = SelectAdminDialog(session, "حذف أدمن", self)
            if dialog.exec():
                username = dialog.get_selected_admin()
                if username:
                    admin_service = AdminService(session)
                    try:
                        admin = admin_service.get_by_username(username)
                        if admin:
                            admin_service.delete(admin.id)
                            QMessageBox.information(self, "تم الحذف", f"تم حذف الأدمن {username} بنجاح.")
                        else:
                            QMessageBox.warning(self, "خطأ", f"لم يتم العثور على أدمن باسم المستخدم {username}.")
                    except ValueError as e:
                        QMessageBox.warning(self, "خطأ", str(e))

    def create_header(self):
        header = QFrame()
        header.setStyleSheet("background-color: white;")
        header.setFixedHeight(100)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 0, 10, 0)

        title = QLabel("Student Placement")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #FDC400;")

        logo1 = QLabel()
        logo1.setPixmap(QPixmap(resource_path("frontend/images/1.png")).scaledToHeight(100, Qt.TransformationMode.SmoothTransformation))
        logo2 = QLabel()
        logo2.setPixmap(QPixmap(resource_path("frontend/images/2.png")).scaledToHeight(100, Qt.TransformationMode.SmoothTransformation))

        logo_container = QHBoxLayout()
        logo_container.addWidget(logo1)
        logo_container.addWidget(logo2)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addLayout(logo_container)

        header.setLayout(header_layout)
        return header

    def create_middle_col(self):
        frame = QFrame()
        layout = QVBoxLayout()

        buttons_texts = ["اضافة/حذف", "تعديل البيانات", "تعديل بيانات الطلاب"]
        for text in buttons_texts:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #A0B5CF;
                    color:#00234E;
                    font-size: 30px;
                    font-weight: bold;
                    width: 80px;
                    height: 130px;
                    padding: 20px;
                    border-radius: 60px;
                }
                QPushButton:hover {
                    background-color:#8096B0;
                }
            """)
            if text == "تعديل بيانات الطلاب":
                btn.clicked.connect(self.open_edit_student_dialog)
            elif text == "تعديل البيانات":
                btn.clicked.connect(self.open_edit_selection_window)
            elif text == "اضافة/حذف" and self.role == "system admin":
                btn.clicked.connect(self.open_add_delete_page)
            layout.addWidget(btn)

        frame.setLayout(layout)
        return frame

    def create_right_col(self):
        frame = QFrame()
        layout = QVBoxLayout()

        buttons_texts = ["تشعيب الطلبة", "نتائج التشعيب", "اضافة/حذف طالب"]
        for text in buttons_texts:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #A0B5CF;
                    color:#00234E;
                    font-size: 30px;
                    font-weight: bold;
                    width: 80px;
                    height: 130px;
                    padding: 20px;
                    border-radius: 60px;
                }
                QPushButton:hover {
                    background-color:#8096B0;
                }
            """)
            if text == "تشعيب الطلبة":
                btn.clicked.connect(self.run_assignment_process)
            elif text == "نتائج التشعيب":
                btn.clicked.connect(self.save_assignment_results)
            elif text == "اضافة/حذف طالب" and self.role in ["admin", "system admin"]:
                btn.clicked.connect(self.open_add_delete_student_page)
            layout.addWidget(btn)

        frame.setLayout(layout)
        return frame

    def save_assignment_results(self):
        try:
            pm = ProjectManager()
            path = pm.get_project_path()
            print(f"Debug: Project path retrieved: {path}")

            with get_session(source="database", project_path=str(path)) as session:
                print("Debug: Database session created")
                student_assignment_service = StudentAssignmentService(session)
                assignments = student_assignment_service.get_all()
                if not assignments:
                    QMessageBox.warning(self, "تحذير", "لا توجد نتائج تشعيب للحفظ.")
                    return

                directory = QFileDialog.getExistingDirectory(
                    self,
                    "اختر مجلد لحفظ ملف النتائج",
                    str(path),
                    QFileDialog.Option.ShowDirsOnly
                )

                if not directory:
                    print("Debug: No directory selected")
                    QMessageBox.warning(self, "تحذير", "لم يتم اختيار مجلد لحفظ الملف.")
                    return

                print(f"Debug: Selected directory: {directory}")

                file_path = Path(directory) / "results.csv"
                if file_path.exists():
                    reply = QMessageBox.question(
                        self,
                        "تأكيد الكتابة فوق الملف",
                        f"الملف results.csv موجود بالفعل في {directory}. هل تريد الكتابة فوقه؟",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if reply == QMessageBox.StandardButton.No:
                        print("Debug: User chose not to overwrite")
                        return

                student_assignment_service.save_to_csv(directory)
                print("Debug: Results saved to CSV")

                QMessageBox.information(
                    self,
                    "تم",
                    f"تم حفظ نتائج التشعيب في ملف CSV في المجلد:\n{directory}"
                )

        except PermissionError as pe:
            print(f"Debug: PermissionError occurred: {pe}")
            QMessageBox.critical(
                self,
                "خطأ",
                f"لا يمكن حفظ الملف بسبب مشكلة في الأذونات:\n{pe}"
            )
        except Exception as e:
            print(f"Debug: Exception occurred: {e}")
            QMessageBox.critical(
                self,
                "خطأ",
                f"فشل حفظ نتائج التشعيب:\n{e}"
            )

    def get_mean_gpa(self):
        pm = ProjectManager()
        path = pm.get_project_path()
        with get_session("database", path) as session:
            student_service = StudentService(session)
            mean_gpa = student_service.get_mean_gpa()
            return mean_gpa

    def create_stats_section(self):
        stats_frame = QFrame()
        stats_frame.setStyleSheet("background-color:#8096b0; border-radius: 40px;")
        stats_frame.setFixedWidth(420)

        stats_layout = QVBoxLayout()
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(15)

        header = QLabel("الإحصائيات")
        header.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #00234E;")
    
        stats_layout.addWidget(header)

        card_data = [
            ("رغبات الطلاب", resource_path("frontend/images/9.png"), "right"),
            ("متوسط GPA", resource_path("frontend/images/9.png"), "left"),
            ("احصائيات الاقسام", resource_path("frontend/images/9.png"), "right")
        ]


        for title, image_path, img_side in card_data:
            stat_frame = QFrame()
            stat_frame.setStyleSheet("background-color: #CFC996;color:#00234E; font: bold; padding: 10px; border-radius: 30px;")
            stat_main_layout = QHBoxLayout(stat_frame)

            image_label = QLabel()
            image_label.setPixmap(QPixmap(image_path).scaled(130, 130, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            image_label.setFixedSize(140, 140)

            info_layout = QVBoxLayout()
            stat_label = QLabel(title)
            stat_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
            stat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            stat_button = QPushButton("عرض")
            stat_button.setStyleSheet(""" 
            QPushButton {
                background-color: #0D2956;
                color: #FFC107;
                font-size: 16px;
                padding: 6px 20px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #23497F;
            }
        """)

            stat_button.setFixedHeight(40)
            stat_button.setFixedWidth(100)
            stat_button.clicked.connect(lambda checked, stat_type=title: self.on_print_button_clicked(stat_type))

            info_layout.addWidget(stat_label, alignment=Qt.AlignmentFlag.AlignCenter)
            info_layout.addWidget(stat_button, alignment=Qt.AlignmentFlag.AlignCenter)

            if img_side == "right":
                stat_main_layout.addWidget(image_label)
                stat_main_layout.addLayout(info_layout)
            else:
                stat_main_layout.addLayout(info_layout)
                stat_main_layout.addWidget(image_label)

            stats_layout.addWidget(stat_frame)

        stats_frame.setLayout(stats_layout)
        return stats_frame

    def on_print_button_clicked(self, stat_type):
        try:
            pm = ProjectManager()
            path = pm.get_project_path()
            print(f"Debug: Project path retrieved: {path}")
            with get_session("database", project_path=str(path)) as session:
                print("Debug: Database session created")
                if stat_type == "رغبات الطلاب":
                    preferences_service = PreferencesService(session)
                    percentages = preferences_service.get_first_preference_percentages()
                    if percentages:
                        result_text = "\n".join([f"{name}: {percentage:.2f}%" for name, percentage in percentages.items()])
                        QMessageBox.information(self, "رغبات الطلاب", f"نسب اختيار الرغبة الأولى:\n{result_text}")
                    else:
                        QMessageBox.information(self, "رغبات الطلاب", "لا توجد رغبات متاحة للطلاب.")
                elif stat_type == "متوسط GPA":
                    mean_gpa = self.get_mean_gpa()
                    print(f"Debug: متوسط GPA هو: {mean_gpa}")
                    QMessageBox.information(self, "متوسط GPA", f"متوسط GPA لجميع الطلاب هو: {mean_gpa:.2f}")
                elif stat_type == "احصائيات الاقسام":
                    student_assignment_service = StudentAssignmentService(session)
                    result_frequencies = student_assignment_service.get_result_frequencies()
                    if result_frequencies:
                        result_text = "\n".join([f"{result}: {count} طالب" for result, count in result_frequencies.items()])
                        QMessageBox.information(
                            self,
                            "إحصائيات الأقسام",
                            f"عدد الطلاب المخصصين لكل نتيجة:\n{result_text}"
                        )
                        reply = QMessageBox.question(
                            self,
                            "تصدير الإحصائيات",
                            "هل تريد تصدير إحصائيات الأقسام إلى ملف CSV؟",
                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                        )
                        if reply == QMessageBox.StandardButton.Yes:
                            directory = QFileDialog.getExistingDirectory(
                                self,
                                "اختر مجلد لحفظ ملف الإحصائيات",
                                str(path),
                                QFileDialog.Option.ShowDirsOnly
                            )
                            if directory:
                                df = pd.DataFrame(list(result_frequencies.items()), columns=["القسم", "عدد الطلاب"])
                                file_path = Path(directory) / "department_stats.csv"
                                df.to_csv(file_path, index=False, encoding='utf-8-sig')
                                print(f"Debug: Department stats saved to {file_path}")
                                QMessageBox.information(
                                    self,
                                    "تم",
                                    f"تم حفظ الإحصائيات في:\n{file_path}"
                                )
                            else:
                                print("Debug: No directory selected for CSV export")
                    else:
                        QMessageBox.information(
                            self,
                            "إحصائيات الأقسام",
                            "لا توجد نتائج تخصيص متاحة."
                        )
        except Exception as e:
            print(f"Debug: Exception occurred: {e}")
            QMessageBox.critical(self, "خطأ", f"فشل عرض الإحصائيات:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pm = ProjectManager()
    path = pm.get_project_path()
    with get_session(source="database", project_path=str(path)) as session:
        window = StudentPlacement(user_name="Dr.Eman", role="system admin", session=session)
        window.show()
    sys.exit(app.exec())