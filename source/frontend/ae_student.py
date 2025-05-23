import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QListWidget, QMessageBox, QDialog, QLineEdit, QDoubleSpinBox, QSizePolicy
)
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
from backend.services.student_service import StudentService
from backend.database.database_config import get_session
from backend.services.project_service import ProjectManager
from backend.services.admin_service import AdminService
from frontend.login import LoginWindow
from frontend.main_f import StudentPlacement
from frontend.student import StudentPlacement as StudentPlacementStudent

def resource_path(relative_path):
    """
    ترجع المسار الصحيح للملف سواء داخل .exe أو خلال التطوير
    """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class AddStudentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إضافة طالب جديد")
        self.setStyleSheet("background-color: #00234E; color: white;")
        self.resize(500, 400)
        self.init_ui()

    def init_ui(self):
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Form frame
        form_frame = QFrame()
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        # ID field
        id_label = QLabel("رقم الطالب:")
        id_label.setFont(QFont("Arial", 14))
        self.id_input = QLineEdit()
        self.id_input.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        form_layout.addWidget(id_label)
        form_layout.addWidget(self.id_input)

        # Name field
        name_label = QLabel("اسم الطالب:")
        name_label.setFont(QFont("Arial", 14))
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_input)

        # Email field
        email_label = QLabel("الإيميل:")
        email_label.setFont(QFont("Arial", 14))
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)

        # GPA field
        gpa_label = QLabel("المعدل التراكمي:")
        gpa_label.setFont(QFont("Arial", 14))
        self.gpa_input = QDoubleSpinBox()
        self.gpa_input.setRange(0.0, 4.0)
        self.gpa_input.setDecimals(2)
        self.gpa_input.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        form_layout.addWidget(gpa_label)
        form_layout.addWidget(self.gpa_input)

        # Preferences field
        preferences_label = QLabel("التفضيلات (مفصولة بفواصل، أقصى 6):")
        preferences_label.setFont(QFont("Arial", 14))
        self.preferences_input = QLineEdit()
        self.preferences_input.setStyleSheet("font-size: 16px; padding: 6px; background-color: white; color: black;")
        form_layout.addWidget(preferences_label)
        form_layout.addWidget(self.preferences_input)

        # Submit button
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
        return {
            "id_num": self.id_input.text().strip(),
            "name": self.name_input.text().strip(),
            "email": self.email_input.text().strip(),
            "gpa": self.gpa_input.value(),
            "preferences": self.preferences_input.text().strip()
        }

class AddDeleteStudentPage(QWidget):
    def __init__(self, user_name="Dr.Eman", role="admin", session=None, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.role = role  # استقبال الدور
        self.session = session
        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        self.setWindowTitle("إضافة/حذف طالب")

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
                background-color: #A9A9A9; border-radius: 10px; padding: 6px;
            }
            QListWidget::item {
                background-color: #00234E; color: white; font-size: 16px;
                padding: 10px; margin: 5px; border-radius: 5px;
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
            background-color: #FDC400; color: black; font-size: 18px;
            padding: 10px; border-radius: 20px; width: 150px;
        """)
        add_button.clicked.connect(self.add_item)
        buttons_layout.addWidget(add_button)

        delete_button = QPushButton("حذف")
        delete_button.setStyleSheet("""
            background-color: #FDC400; color: black; font-size: 18px;
            padding: 10px; border-radius: 20px; width: 150px;
        """)
        delete_button.clicked.connect(self.delete_item_by_name)
        buttons_layout.addWidget(delete_button)

        form_layout.addLayout(buttons_layout)
        form_frame.setLayout(form_layout)
        content_background_layout.addWidget(form_frame)

        content_layout.addWidget(header)
        content_layout.addWidget(content_background)

        sidebar = self.create_sidebar()

        main_layout.addLayout(content_layout)
        main_layout.addWidget(sidebar)
        self.setLayout(main_layout)
        self.load_data()

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
            color: white; font-size: 24px; background: none; border: none;
            padding-right: 100px; padding-top: 20px;
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
            color: white; font-size: 26px; background: none; border: none;
            text-align: right; padding-right: 100px;
        """)
        logout_btn.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        logout_btn.clicked.connect(self.logout)
        sidebar_layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignBottom)

        sidebar.setLayout(sidebar_layout)
        return sidebar

    def go_to_main(self):
        print(f"Debug: Role is {self.role}")  # Debugging
        if hasattr(self, 'session') and self.session:
            self.session.close()
        self.close()
        pm = ProjectManager()
        path = pm.get_project_path()
        with get_session(source="database", project_path=str(path)) as new_session:
            if self.role == "system admin":
                # If it's system admin, navigate to StudentPlacement from main_f.py
                print("Debug: Navigating to System Admin page.")
                self.main_window = StudentPlacement(user_name=self.user_name, role=self.role, session=new_session)
            else:
                # If it's admin or other roles, navigate to StudentPlacement from student.py
                print("Debug: Navigating to Admin/Other role page.")
                self.main_window = StudentPlacementStudent(user_name=self.user_name, role=self.role, session=new_session)
            self.main_window.show()


    def load_data(self):
        try:
            print("Debug: Starting load_data")
            self.list_widget.clear()
            print("Debug: Loading data for students")
            service = StudentService(self.session)
            items = service.get_all()
            for item in items:
                self.list_widget.addItem(f"{item.name} (ID: {item.id_num})")
            print("Debug: load_data completed successfully")
        except Exception as e:
            print(f"Debug: Error in load_data: {e}")
            QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء تحميل بيانات الطلاب:\n{e}")

    def add_item(self):
        dialog = AddStudentDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            id_num = data["id_num"]
            name = data["name"]
            email = data["email"]
            gpa = data["gpa"]
            preferences = data["preferences"]

            if not id_num or not name or not email:
                QMessageBox.warning(self, "تحذير", "يرجى ملء جميع الحقول الأساسية (رقم الطالب، الاسم، الإيميل).")
                return

            preference_names = [p.strip() for p in preferences.split(',') if p.strip()] if preferences else None

            try:
                service = StudentService(self.session)
                service.create(
                    id_num=id_num,
                    name=name,
                    email=email,
                    gpa=gpa,
                    preference_names=preference_names
                )
                QMessageBox.information(self, "تم", f"تم إضافة الطالب {name} بنجاح.")
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء الإضافة:\n{e}")

    def delete_item_by_name(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "تحذير", "من فضلك اختر طالباً للحذف.")
            return

        item_text = selected_item.text()
        student_name = item_text.split(" (ID:")[0].strip()

        service = StudentService(self.session)
        student = service.get_by_name(student_name)
        if not student:
            QMessageBox.warning(self, "خطأ", f"لم يتم العثور على الطالب {student_name} في قاعدة البيانات.")
            return

        reply = QMessageBox.question(self, "تأكيد الحذف", f"هل أنت متأكد أنك تريد حذف الطالب {student.name}؟",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                service.delete(student.id_num)
                QMessageBox.information(self, "تم الحذف", f"تم حذف الطالب {student.name} بنجاح.")
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"حصل خطأ أثناء الحذف:\n{e}")

    def logout(self):
        if hasattr(self, 'session') and self.session:
            self.session.close()
        self.close()
        try:
            self.login_window = LoginWindow()
            self.login_window.show()
        except Exception as e:
            print(f"Debug: Error opening login window: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pm = ProjectManager()
    path = pm.get_project_path()
    with get_session(source="database", project_path=str(path)) as session:
        window = AddDeleteStudentPage(user_name="Dr.Eman", role="admin", session=session)
        window.show()
    sys.exit(app.exec())