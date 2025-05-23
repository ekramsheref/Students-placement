#student.py
import sys
import subprocess
import os
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QProgressBar, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QSizePolicy, QInputDialog, QMessageBox, QDialog, QLineEdit, QFileDialog
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.student_service import StudentService
from backend.services.admin_service import AdminService
from backend.database.database_config import get_session
from backend.services.project_service import ProjectInfoService, ProjectManager
from frontend.login import LoginWindow
import bcrypt
from backend.database.models import Admin
from backend.services.department_service import DepartmentService
from backend.services.program_service import ProgramService
from backend.services.specialization_service import SpecializationService
from backend.services.student_assignment_service import StudentAssignmentService
from backend.process.assignment_process import AssignmentProcess
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

        self.save_button = QPushButton("تحديث البيانات")
        self.save_button.setStyleSheet("background-color: #FDC400; color: black; font-size: 18px; padding: 10px; border-radius: 20px;")
        self.save_button.clicked.connect(self.update_student)
        form_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)

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

class EditAdminForm(QDialog):
    def __init__(self, session, admin_id, parent=None):
        super().__init__(parent)
        self.session = session
        self.admin_id = admin_id
        self.setWindowTitle("تعديل بيانات الأدمن")
        self.setStyleSheet("background-color: #00234E; color: white;")
        self.resize(500, 400)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("اسم الأدمن")
        self.name_input.setStyleSheet("font-size: 16px; padding: 8px; background-color: white; color: black; border-radius: 10px;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")
        self.username_input.setStyleSheet("font-size: 16px; padding: 8px; background-color: white; color: black; border-radius: 10px;")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("كلمة المرور (اتركها فارغة لعدم التغيير)")
        self.password_input.setStyleSheet("font-size: 16px; padding: 8px; background-color: white; color: black; border-radius: 10px;")

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
            else:
                msg = QMessageBox()
                msg.setStyleSheet("background:white;")
                msg.warning(self, "خطأ", "الأدمن غير موجود.")
                self.close()
        except Exception as e:
            msg = QMessageBox()
            msg.setStyleSheet("background:white;")
            msg.critical(self, "خطأ", f"حصل خطأ أثناء تحميل بيانات الأدمن:\n{e}")
            self.close()

    def save_admin(self):
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not name:
            msg = QMessageBox()
            msg.setStyleSheet("background:white;")
            msg.warning(self, "خطأ", "من فضلك أكمل جميع الحقول.")
            return

        try:
            admin_service = AdminService(self.session)
            admin_service.update(
                admin_id=self.admin_id,
                name=name,
                username=username,
                password=password if password else None
            )
            self.session.commit()
            msg = QMessageBox()
            msg.setStyleSheet("background:white;")
            msg.information(self, "تم التحديث", "تم تعديل بيانات الأدمن بنجاح.")
            self.close()
        except ValueError as ve:
            msg = QMessageBox()
            msg.setStyleSheet("background:white;")
            msg.warning(self, "خطأ", str(ve))
        except Exception as e:
            msg = QMessageBox()
            msg.setStyleSheet("background:white;")
            msg.critical(self, "خطأ", f"حصل خطأ أثناء تعديل الأدمن:\n{e}")

def create_stats_section(parent):
    stats_frame = QFrame()
    stats_frame.setStyleSheet("background-color:#8096b0 ; border-radius: 40px; padding: 0px;")
    stats_frame.setFixedWidth(380)

    stats_layout = QVBoxLayout()
    stats_layout.setContentsMargins(0, 0, 0, 0)
    stats_layout.setSpacing(10)

    header = QLabel("إحصائيات الأقسام")
    header.setFont(QFont("Arial", 24, QFont.Weight.Bold))
    header.setStyleSheet("""
        color:#00234E;
        min-height: 40px; 
        border-top-left-radius: 40px; 
        border-top-right-radius: 40px;
    """)
    header.setAlignment(Qt.AlignmentFlag.AlignCenter)
    stats_layout.addWidget(header)

    content_layout = QVBoxLayout()
    content_layout.setContentsMargins(20, 15, 20, 20)
    content_layout.setSpacing(15)

    pie_chart = QLabel()
    pie_chart.setPixmap(QPixmap(resource_path("frontend/images/9.png")).scaled(260, 260, Qt.AspectRatioMode.KeepAspectRatio))
    pie_chart.setAlignment(Qt.AlignmentFlag.AlignCenter)
    content_layout.addWidget(pie_chart)

    departments = [
        ("CS", 90),
        ("Stat/CS", 70),
        ("Math/CS", 60),
        ("Math", 30),
        ("Biology", 80),
        ("Geology", 40),
    ]

    for dept, progress in departments:
        bar_layout = QHBoxLayout()
        bar_layout.setSpacing(10)

        label = QLabel(dept)
        label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        label.setStyleSheet("color: #00234E;")

        progress_bar = QProgressBar()
        progress_bar.setValue(progress)
        progress_bar.setFixedHeight(10)
        progress_bar.setStyleSheet("""
            QProgressBar {
                background: #FFC107;
                border: none;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #0D2956;
                border-radius: 5px;
            }
        """)

        bar_layout.addWidget(label)
        bar_layout.addWidget(progress_bar)
        content_layout.addLayout(bar_layout)

    show_all_button = QPushButton("عرض الكل")
    show_all_button.setStyleSheet("""
        QPushButton {
            background-color: #0D2956;
            color: yellow;
            padding: 8px;
            font-size: 14px;
            border-radius: 15px;
        }
        QPushButton:hover {
            background-color: #23497F;
        }
    """)
    show_all_button.setFixedHeight(35)
    show_all_button.clicked.connect(parent.show_department_stats_only)
    content_layout.addWidget(show_all_button, alignment=Qt.AlignmentFlag.AlignCenter)

    stats_layout.addLayout(content_layout)
    stats_frame.setLayout(stats_layout)
    return stats_frame

class StudentViewPage(QWidget):
    def __init__(self, student_id, session, parent=None):
        super().__init__(parent)
        self.student_id = student_id
        self.session = session
        self.setWindowTitle("عرض بيانات طالب")
        self.setStyleSheet("background-color: #00234E; color: white;")
        self.resize(600, 500)

        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        outer_layout.setContentsMargins(0, 40, 0, 20)
        outer_layout.setSpacing(20)

        form_framesides = QFrame()
        form_framesides.setFixedWidth(500)
        center_layout = QHBoxLayout()
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(18)

        self.id_num_input = QLineEdit()
        self.id_num_input.setReadOnly(True)
        self.name_input = QLineEdit()
        self.name_input.setReadOnly(True)
        self.email_input = QLineEdit()
        self.email_input.setReadOnly(True)
        self.gpa_input = QLineEdit()
        self.gpa_input.setReadOnly(True)
        self.preferences_input = QLineEdit()
        self.preferences_input.setReadOnly(True)

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
            field.setStyleSheet("font-size: 16px; padding: 6px; background-color:white; color:black;")
            field.setFixedWidth(280)
            row.addWidget(field)
            row.addWidget(label)
            form_layout.addLayout(row)

        form_framesides.setLayout(form_layout)
        center_layout.addWidget(form_framesides)
        outer_layout.addLayout(center_layout)
        self.setLayout(outer_layout)
        self.load_student_data()

    def load_student_data(self):
        try:
            student_service = StudentService(self.session)
            self.student = student_service.get(self.student_id)
            if self.student:
                self.id_num_input.setText(str(self.student.id_num))
                self.name_input.setText(self.student.name)
                self.email_input.setText(self.student.email)
                self.gpa_input.setText(str(self.student.gpa))
                preferences = [pref.name for pref in getattr(self.student, 'preferences', [])]
                self.preferences_input.setText(", ".join(preferences) if preferences else "")
            else:
                QMessageBox.warning(self, "تنبيه", f"الطالب برقم {self.student_id} غير موجود.")
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء تحميل البيانات:\n{e}")
            self.close()

class StudentPlacement(QWidget):
    def __init__(self, user_name="Mohamed", role="admin", session=None):
        super().__init__()
        self.user_name = user_name
        self.role = role  # إضافة الدور
        self.session = session
        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        self.setWindowTitle("Student Placement")
        self.setGeometry(100, 100, 1200, 700)

        main_layout = QHBoxLayout()
        content_layout = QVBoxLayout()
        header = self.create_header()

        content_background = QFrame()
        content_background.setStyleSheet("background-color: #D3D3D3; padding: 10px; border-radius: 10px;")
        content_background_layout = QHBoxLayout(content_background)

        stats_section = create_stats_section(self)
        middle_col = self.create_middle_col()
        right_col = self.create_right_col()

        content_background_layout.addWidget(stats_section, 1)
        content_background_layout.addWidget(middle_col, 1)
        content_background_layout.addWidget(right_col, 1)

        content_layout.addWidget(header)
        content_layout.addWidget(content_background)

        sidebar = self.create_sidebar()
        main_layout.addLayout(content_layout)
        main_layout.addWidget(sidebar)

        self.setLayout(main_layout)

    def create_middle_col(self):
        frame = QFrame()
        layout = QVBoxLayout()

        buttons_texts = ["بحث عن بيانات طالب", "تعديل بيانات الطلاب", "إضافة/حذف طالب"]
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
            if text == "بحث عن بيانات طالب":
                btn.clicked.connect(self.open_view_student_dialog)
            elif text == "تعديل بيانات الطلاب":
                btn.clicked.connect(self.open_edit_student_dialog)
            elif text == "إضافة/حذف طالب" and self.role in ["admin", "system admin"]:
                btn.clicked.connect(self.open_add_delete_student_page)
            layout.addWidget(btn)

        frame.setLayout(layout)
        return frame

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

    def open_view_student_dialog(self):
        student_id, ok = QInputDialog.getText(self, "بحث عن طالب", "ادخل رقم الطالب:")
        if ok and student_id.isdigit():
            try:
                self.view_window = StudentViewPage(int(student_id), self.session)
                self.view_window.show()
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"فشل فتح نافذة عرض الطالب:\n{e}")
        elif ok:
            QMessageBox.warning(self, "خطأ", "من فضلك ادخل رقم صحيح للطالب.")

    def create_right_col(self):
        frame = QFrame()
        layout = QVBoxLayout()

        buttons_texts = ["تشعيب الطلبة", "نتائج التشعيب"]
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
            layout.addWidget(btn)

        frame.setLayout(layout)
        return frame

    def open_add_delete_student_page(self):
        if self.role not in ["admin", "system admin"]:
            QMessageBox.warning(self, "تحذير", "ليس لديك صلاحية الوصول إلى هذا الخيار.")
            return
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
        except Exception as e:
            print(f"Debug: Exception occurred: {e}")
            QMessageBox.critical(self, "خطأ", f"فشل فتح نافذة الإضافة/حذف للطلاب:\n{e}")

    def create_header(self):
        header = QFrame()
        header.setStyleSheet("background-color: white; padding: 0px;")
        header.setFixedHeight(100)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 0, 10, 0)

        title = QLabel("Student Placement")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #FDC400;")

        logo1 = QLabel()
        logo1.setPixmap(QPixmap(resource_path("frontend/images/1.png")).scaledToHeight(100, Qt.TransformationMode.SmoothTransformation))
        logo1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        logo2 = QLabel()
        logo2.setPixmap(QPixmap(resource_path("frontend/images/2.png")).scaledToHeight(100, Qt.TransformationMode.SmoothTransformation))
        logo2.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        logo_container = QHBoxLayout()
        logo_container.setContentsMargins(0, 0, 0, 0)
        logo_container.setSpacing(0)
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

        sidebar_layout.addSpacing(30)

        buttons = [
            ("تعديل بياناتي", resource_path("frontend/images/l3.png"), self.edit_admin),
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
            btn.setMinimumWidth(280)
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

    def edit_admin(self):
        with get_session(source="user") as session:
            admin_service = AdminService(session)
            admin = admin_service.get_by_username(self.user_name)
            if admin:
                self.edit_admin_form = EditAdminForm(session, admin.id)
                self.edit_admin_form.exec()
            else:
                msg = QMessageBox()
                msg.setStyleSheet("background:white;")
                msg.warning(self, "تنبيه", f"لم يتم العثور على أدمن باسم المستخدم {self.user_name}.")

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

    def show_department_stats_only(self):
        try:
            pm = ProjectManager()
            path = pm.get_project_path()
            with get_session("database", project_path=str(path)) as session:
                student_assignment_service = StudentAssignmentService(session)
                result_frequencies = student_assignment_service.get_result_frequencies()
                if result_frequencies:
                    result_text = "\n".join([f"{result}: {count} طالب" for result, count in result_frequencies.items()])
                    QMessageBox.information(
                        self,
                        "إحصائيات الأقسام",
                        f"عدد الطلاب المخصصين لكل نتيجة:\n{result_text}"
                    )
                else:
                    QMessageBox.information(
                        self,
                        "إحصائيات الأقسام",
                        "لا توجد نتائج تخصيص متاحة."
                    )
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل عرض الإحصائيات:\n{e}")

    def logout(self):
        if hasattr(self, 'session') and self.session:
            self.session.close()
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pm = ProjectManager()
    path = pm.get_project_path()
    with get_session(source="database", project_path=str(path)) as session:
        window = StudentPlacement(user_name="Mohamed", role="admin", session=session)
        window.show()
    sys.exit(app.exec())