from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

import sys
import os

# إضافة المسار الجذري للمشروع إلى sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# الآن استيراد الخدمات الخلفية
from backend.services.admin_service import AdminService
from backend.database.database_config import get_session, init_user_db
from frontend.p4 import HomeWindow

def resource_path(relative_path):
    """
    ترجع المسار الصحيح للملف سواء داخل .exe أو خلال التطوير
    """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # تهيئة قاعدة البيانات
        init_user_db()

        self.setWindowTitle("Login")
        self.setStyleSheet("background-color: #002147;")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(20)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        central_layout = QHBoxLayout()
        left_spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        right_spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        form_container = QVBoxLayout()
        form_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_container.setSpacing(20)

        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.setSpacing(20)

        self.logo1 = QLabel(self)
        pixmap1 = QPixmap(resource_path("frontend/images/2.png"))
        self.logo1.setPixmap(pixmap1)
        self.logo1.setScaledContents(True)
        self.logo1.setFixedSize(140, 140)

        self.logo2 = QLabel(self)
        pixmap2 = QPixmap(resource_path("frontend/images/1.png"))
        self.logo2.setPixmap(pixmap2)
        self.logo2.setScaledContents(True)
        self.logo2.setFixedSize(140, 140)

        logo_layout.addWidget(self.logo1)
        logo_layout.addWidget(self.logo2)

        self.title = QLabel("تسجيل الدخول")
        self.title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.setSpacing(20)

        field_width = 300
        field_height = 50

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("اسم المستخدم")
        self.phone_input.setFixedSize(field_width, field_height)
        self.phone_input.setStyleSheet("background: white; padding: 8px; border-radius: 5px; font-size: 16px;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedSize(field_width, field_height)
        self.password_input.setStyleSheet("background: white; padding: 8px; border-radius: 5px; font-size: 16px;")

        self.login_button = QPushButton("الدخول")
        self.login_button.setFixedSize(field_width, field_height)
        self.login_button.setStyleSheet("""
            background-color: #FFC107;
            color: black;
            font-weight: bold;
            font-size: 18px;
            border-radius: 5px;
        """)

        form_container.addLayout(logo_layout)
        form_container.addWidget(self.title)
        form_container.addWidget(self.phone_input, alignment=Qt.AlignmentFlag.AlignCenter)
        form_container.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)
        form_container.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        central_layout.addItem(left_spacer)
        central_layout.addLayout(form_container)
        central_layout.addItem(right_spacer)

        main_layout.addLayout(central_layout)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # ربط حدث الضغط على زر الدخول
        self.login_button.clicked.connect(self.handle_login)

    def handle_login(self):
        user_name = self.phone_input.text()
        password = self.password_input.text()
        try:
            with get_session(source="user") as session:
                admin_service = AdminService(session)
                role = admin_service.login(user_name, password)  # تعيد الدور مباشرة

                if role is None:  # للتعامل مع حالة الفشل (كما في الكود الأصلي، لكن يجب تعديلها)
                    QMessageBox.warning(self, "خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة.")
                    QMessageBox.styleSheet("background:white;")
                else:
                    if role in ["admin", "system admin"]:
                        self.window = HomeWindow(session=session, role=role, user_name=user_name)
                        self.window.show()
                        self.close()
                    else:
                        QMessageBox.warning(self, "خطأ", "ليس لديك صلاحية الوصول.")
        except ValueError as e:
            QMessageBox.warning(self, "خطأ", str(e))
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تسجيل الدخول: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())