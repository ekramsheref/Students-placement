#ae.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QListWidget, QMessageBox, QInputDialog, QSizePolicy, QLineEdit,
    QComboBox, QDialog, QDoubleSpinBox, QSpinBox
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
from backend.services.department_service import DepartmentService
from backend.services.program_service import ProgramService
from backend.services.specialization_service import SpecializationService
from backend.database.database_config import get_session
from backend.services.project_service import ProjectManager
from frontend.login import LoginWindow
from frontend.main_f import StudentPlacement
def resource_path(relative_path):
    """
    ترجع المسار الصحيح للملف سواء داخل .exe أو خلال التطوير
    """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)
class AddDepartmentDialog(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("إضافة قسم")
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

        submit_button = QPushButton("إضافة")
        submit_button.setStyleSheet("""
            background-color: #FDC400;
            color: black;
            font-size: 18px;
            padding: 10px;
            border-radius: 20px;
        """)
        submit_button.clicked.connect(self.accept)
        form_layout.addWidget(submit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        self.setLayout(layout)

    def get_data(self):
        return {"name": self.name_input.text().strip()}

class AddProgramDialog(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("إضافة برنامج")
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
        self.dept_combo = QComboBox()
        self.dept_combo.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        self.load_departments()
        form_layout.addWidget(dept_label)
        form_layout.addWidget(self.dept_combo)

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

        submit_button = QPushButton("إضافة")
        submit_button.setStyleSheet("""
            background-color: #FDC400;
            color: black;
            font-size: 18px;
            padding: 10px;
            border-radius: 20px;
        """)
        submit_button.clicked.connect(self.accept)
        form_layout.addWidget(submit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        self.setLayout(layout)

    def load_departments(self):
        try:
            dept_service = DepartmentService(self.session)
            departments = dept_service.get_all()
            self.dept_combo.addItem("اختر قسم", -1)
            for dept in departments:
                self.dept_combo.addItem(dept.name, dept.id)
        except Exception as e:
            print(f"Debug: Error loading departments: {e}")
            QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء تحميل الأقسام:\n{e}")

    def get_data(self):
        name = self.name_input.text().strip()
        dept_id = self.dept_combo.currentData()
        gpa_threshold = self.gpa_input.value()
        student_capacity = self.capacity_input.value()
        subjects_required_dict = {}
        if self.subject1_code.text().strip():
            subjects_required_dict[self.subject1_code.text().strip()] = self.subject1_grade.value()
        if self.subject2_code.text().strip():
            subjects_required_dict[self.subject2_code.text().strip()] = self.subject2_grade.value()
        return {
            "name": name,
            "department_id": dept_id,
            "gpa_threshold": gpa_threshold,
            "student_capacity": student_capacity,
            "subjects_required_dict": subjects_required_dict if subjects_required_dict else None
        }

class AddSpecializationDialog(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("إضافة تخصص")
        self.setStyleSheet("background-color: #00234E; color: white;")
        self.resize(500, 500)

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

        dept_label = QLabel("القسم:")
        dept_label.setFont(QFont("Arial", 14))
        self.dept_combo = QComboBox()
        self.dept_combo.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        self.load_departments()
        form_layout.addWidget(dept_label)
        form_layout.addWidget(self.dept_combo)

        program_label = QLabel("البرنامج:")
        program_label.setFont(QFont("Arial", 14))
        self.program_combo = QComboBox()
        self.program_combo.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        self.load_programs()
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

        submit_button = QPushButton("إضافة")
        submit_button.setStyleSheet("""
            background-color: #FDC400;
            color: black;
            font-size: 18px;
            padding: 10px;
            border-radius: 20px;
        """)
        submit_button.clicked.connect(self.accept)
        form_layout.addWidget(submit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)
        self.setLayout(layout)

    def load_departments(self):
        try:
            dept_service = DepartmentService(self.session)
            departments = dept_service.get_all()
            self.dept_combo.addItem("اختر قسم", -1)
            for dept in departments:
                self.dept_combo.addItem(dept.name, dept.id)
        except Exception as e:
            print(f"Debug: Error loading departments: {e}")
            QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء تحميل الأقسام:\n{e}")

    def load_programs(self):
        try:
            program_service = ProgramService(self.session)
            programs = program_service.get_all()
            self.program_combo.addItem("اختر برنامج", -1)
            for program in programs:
                self.program_combo.addItem(program.name, program.id)
        except Exception as e:
            print(f"Debug: Error loading programs: {e}")
            QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء تحميل البرامج:\n{e}")

    def get_data(self):
        name = self.name_input.text().strip()
        dept_id = self.dept_combo.currentData()
        program_id = self.program_combo.currentData()
        gpa_threshold = self.gpa_input.value()
        student_capacity = self.capacity_input.value()
        subjects_required_dict = {}
        if self.subject1_code.text().strip():
            subjects_required_dict[self.subject1_code.text().strip()] = self.subject1_grade.value()
        if self.subject2_code.text().strip():
            subjects_required_dict[self.subject2_code.text().strip()] = self.subject2_grade.value()
        return {
            "name": name,
            "department_id": dept_id,
            "program_id": program_id,
            "gpa_threshold": gpa_threshold,
            "student_capacity": student_capacity,
            "subjects_required_dict": subjects_required_dict if subjects_required_dict else None
        }

class AddDeletePage(QWidget):
    def __init__(self, user_name="Dr.Eman", session=None, ptype=None, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.session = session
        ptype, ok = QInputDialog.getItem(
            self,
            "اختيار النوع",
            "اختر النوع:",
            ["قسم", "برنامج", "تخصص"],
            0,
            False
        )
        if ok:
            ptype_map = {"قسم": "department", "برنامج": "program", "تخصص": "specialization"}
            self.ptype = ptype_map[ptype]
        else:
            self.ptype = "department"
        print(f"Debug: Initializing AddDeletePage with user_name={self.user_name}, ptype={self.ptype}")
        self.init_ui()
        print("Debug: init_ui completed")
        self.showMaximized()
        print("Debug: showMaximized called")

    def init_ui(self):
        self.setWindowTitle("إضافة/حذف")
        main_layout = QHBoxLayout()
        content_layout = QVBoxLayout()

        header = self.create_header()

        content_background = QFrame()
        content_background.setStyleSheet("background-color: #D3D3D3; padding: 10px; border-radius: 10px;")
        content_background_layout = QVBoxLayout(content_background)
        content_background_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_frame = QFrame()
        form_layout = QVBoxLayout()
        form_layout.setSpacing(18)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #A9A9A9;
                border-radius: 10px;
                padding: 6px;
            }
            QListWidget::item {
                background-color: #00234E;
                color: white;
                font-size: 16px;
                padding: 10px;
                margin: 5px;
                border-radius: 5px;
            }
            QListWidget::item:selected {
                background-color: #003080;
            }
        """)
        self.list_widget.setFixedHeight(500)
        form_layout.addWidget(self.list_widget)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        add_button = QPushButton("إضافة")
        add_button.setStyleSheet("""
            background-color: #FDC400;
            color: black;
            font-size: 18px;
            padding: 10px;
            border-radius: 20px;
            width: 150px;
        """)
        add_button.clicked.connect(self.add_item)
        buttons_layout.addWidget(add_button)

        delete_button = QPushButton("حذف")
        delete_button.setStyleSheet("""
            background-color: #FDC400;
            color: black;
            font-size: 18px;
            padding: 10px;
            border-radius: 20px;
            width: 150px;
        """)
        delete_button.clicked.connect(self.delete_item)
        buttons_layout.addWidget(delete_button)

        form_layout.addLayout(buttons_layout)
        form_frame.setLayout(form_layout)
        content_background_layout.addWidget(form_frame)

        content_layout.addWidget(header)
        content_background.setLayout(content_background_layout)
        content_layout.addWidget(content_background)

        sidebar = self.create_sidebar()

        main_layout.addLayout(content_layout)
        main_layout.addWidget(sidebar)
        self.setLayout(main_layout)
        print("Debug: UI layout set")
        self.load_data()
        print("Debug: load_data called")

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
        try:
            logo1.setPixmap(QPixmap(resource_path("frontend/images/1.png")).scaledToHeight(100, Qt.TransformationMode.SmoothTransformation))
        except Exception as e:
            print(f"Debug: Failed to load logo1: {e}")
            logo1.setText("Logo 1")

        logo2 = QLabel()
        try:
            logo2.setPixmap(QPixmap(resource_path("frontend/images/2.png")).scaledToHeight(100, Qt.TransformationMode.SmoothTransformation))
        except Exception as e:
            print(f"Debug: Failed to load logo2: {e}")
            logo2.setText("Logo 2")

        logo_container = QHBoxLayout()
        logo_container.addWidget(logo1)
        logo_container.addWidget(logo2)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addLayout(logo_container)

        header.setLayout(header_layout)
        return header

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: #00234E; color: white;")
        sidebar.setFixedWidth(320)
        sidebar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(10, 20, 10, 20)

        profile_pic = QLabel()
        try:
            profile_pic.setPixmap(QPixmap(resource_path("frontend/images/image2_no_bg.png")).scaled(182, 182, Qt.AspectRatioMode.KeepAspectRatio))
        except Exception as e:
            print(f"Debug: Failed to load profile_pic: {e}")
            profile_pic.setText("Profile Pic")
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

        home_btn = QPushButton("الرئيسية")
        try:
            home_btn.setIcon(QIcon(resource_path("frontend/images/icon1_new_no_bg.png")))
        except Exception as e:
            print(f"Debug: Failed to load home icon: {e}")
            home_btn.setText("الرئيسية (Icon Missing)")
        home_btn.setIconSize(QSize(40, 40))
        home_btn.setStyleSheet("""
            color: white;
            font-size: 24px;
            background: none;
            border: none;
            padding-right: 100px;
            padding-top: 20px;
        """)
        home_btn.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        home_btn.clicked.connect(self.go_to_main)
        sidebar_layout.addWidget(home_btn)

        sidebar_layout.addStretch()

        logout_btn = QPushButton("تسجيل الخروج")
        try:
            logout_btn.setIcon(QIcon(resource_path("frontend/images/icon3_new_no_bg.png")))
        except Exception as e:
            print(f"Debug: Failed to load logout icon: {e}")
            logout_btn.setText("تسجيل الخروج (Icon Missing)")
        logout_btn.setIconSize(QSize(64, 64))
        logout_btn.setStyleSheet("""
            color: white;
            font-size: 26px;
            background: none;
            border: none;
            text-align: right;
            padding-right: 100px;
        """)
        logout_btn.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        logout_btn.clicked.connect(self.logout)
        sidebar_layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignBottom)

        sidebar.setLayout(sidebar_layout)
        return sidebar

    def go_to_main(self):
        if hasattr(self, 'session') and self.session:
            self.session.close()
        self.close()
        pm = ProjectManager()
        path = pm.get_project_path()
        with get_session(source="database", project_path=str(path)) as new_session:
            self.main_window = StudentPlacement(user_name=self.user_name, session=new_session)
            self.main_window.show()
        print("Debug: Navigated to main window")

    def load_data(self):
        try:
            print("Debug: Starting load_data")
            self.list_widget.clear()
            print(f"Debug: Loading data for ptype={self.ptype}")
            if self.ptype == "department":
                service = DepartmentService(self.session)
                print("Debug: DepartmentService created")
                items = service.get_all()
                print(f"Debug: Retrieved {len(items)} departments")
                for item in items:
                    self.list_widget.addItem(item.name)
            elif self.ptype == "program":
                service = ProgramService(self.session)
                print("Debug: ProgramService created")
                items = service.get_all()
                print(f"Debug: Retrieved {len(items)} programs")
                for item in items:
                    self.list_widget.addItem(item.name)
            elif self.ptype == "specialization":
                service = SpecializationService(self.session)
                print("Debug: SpecializationService created")
                items = service.get_all()
                print(f"Debug: Retrieved {len(items)} specializations")
                for item in items:
                    self.list_widget.addItem(item.name)
            print("Debug: load_data completed successfully")
        except Exception as e:
            print(f"Debug: Error in load_data: {e}")
            QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء تحميل البيانات:\n{e}")

    def add_item(self):
        try:
            if self.ptype == "department":
                dialog = AddDepartmentDialog(self.session, self)
                if dialog.exec():
                    data = dialog.get_data()
                    if not data["name"]:
                        QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم القسم.")
                        return
                    service = DepartmentService(self.session)
                    if service.get_by_username(data["name"]):
                        QMessageBox.warning(self, "خطأ", f"القسم '{data['name']}' موجود بالفعل.")
                        return
                    service.create(name=data["name"])
                    print(f"Debug: Department '{data['name']}' created")
                    QMessageBox.information(self, "تم", f"تم إضافة {data['name']} بنجاح.")
                    self.load_data()
            elif self.ptype == "program":
                dialog = AddProgramDialog(self.session, self)
                if dialog.exec():
                    data = dialog.get_data()
                    if not data["name"]:
                        QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم البرنامج.")
                        return
                    if data["department_id"] == -1:
                        QMessageBox.warning(self, "خطأ", "يرجى اختيار قسم.")
                        return
                    service = ProgramService(self.session)
                    if service.get_by_name(data["name"]):
                        QMessageBox.warning(self, "خطأ", f"البرنامج '{data['name']}' موجود بالفعل.")
                        return
                    service.create(
                        name=data["name"],
                        department_id=data["department_id"],
                        gpa_threshold=data["gpa_threshold"],
                        student_capacity=data["student_capacity"],
                        subjects_required_dict=data["subjects_required_dict"]
                    )
                    print(f"Debug: Program '{data['name']}' created")
                    QMessageBox.information(self, "تم", f"تم إضافة {data['name']} بنجاح.")
                    self.load_data()
            elif self.ptype == "specialization":
                dialog = AddSpecializationDialog(self.session, self)
                if dialog.exec():
                    data = dialog.get_data()
                    if not data["name"]:
                        QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم التخصص.")
                        return
                    if data["department_id"] == -1:
                        QMessageBox.warning(self, "خطأ", "يرجى اختيار قسم.")
                        return
                    if data["program_id"] == -1:
                        QMessageBox.warning(self, "خطأ", "يرجى اختيار برنامج.")
                        return
                    service = SpecializationService(self.session)
                    # Assuming SpecializationService has get_by_name
                    if hasattr(service, 'get_by_name') and service.get_by_name(data["name"]):
                        QMessageBox.warning(self, "خطأ", f"التخصص '{data['name']}' موجود بالفعل.")
                        return
                    service.create(
                        name=data["name"],
                        department_id=data["department_id"],
                        program_id=data["program_id"],
                        gpa_threshold=data["gpa_threshold"],
                        student_capacity=data["student_capacity"],
                        subjects_required_dict=data["subjects_required_dict"]
                    )
                    print(f"Debug: Specialization '{data['name']}' created")
                    QMessageBox.information(self, "تم", f"تم إضافة {data['name']} بنجاح.")
                    self.load_data()
        except Exception as e:
            print(f"Debug: Error in add_item: {e}")
            QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء الإضافة:\n{e}")

    def delete_item(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "خطأ", "يرجى تحديد عنصر لحذفه.")
            return
        name = selected_item.text()
        try:
            if self.ptype == "department":
                service = DepartmentService(self.session)
                department = service.get_by_username(name)
                if department:
                    service.delete(department.id)
                    print(f"Debug: Department '{name}' deleted")
                else:
                    QMessageBox.warning(self, "خطأ", f"القسم '{name}' غير موجود.")
                    return
            elif self.ptype == "program":
                service = ProgramService(self.session)
                program = service.get_by_name(name)
                if program:
                    service.delete(program.id)
                    print(f"Debug: Program '{name}' deleted")
                else:
                    QMessageBox.warning(self, "خطأ", f"البرنامج '{name}' غير موجود.")
                    return
            elif self.ptype == "specialization":
                service = SpecializationService(self.session)
                items = service.get_all()
                target_item = next((item for item in items if item.name == name), None)
                if target_item:
                    service.delete(target_item.id)
                    print(f"Debug: Specialization '{name}' deleted")
                else:
                    QMessageBox.warning(self, "خطأ", f"التخصص '{name}' غير موجود.")
                    return
            QMessageBox.information(self, "تم", f"تم حذف {name} بنجاح.")
            self.load_data()
        except Exception as e:
            print(f"Debug: Error in delete_item: {e}")
            QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء الحذف:\n{e}")

    def logout(self):
        if hasattr(self, 'session') and self.session:
            self.session.close()
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()
        print("Debug: Logged out")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pm = ProjectManager()
    path = pm.get_project_path()
    with get_session(source="database", project_path=str(path)) as session:
        window = AddDeletePage(session=session)
        window.show()
    sys.exit(app.exec())