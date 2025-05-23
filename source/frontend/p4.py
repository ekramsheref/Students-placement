#p4.py
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog, QDialog, QComboBox, QLineEdit, QSizePolicy
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
import sys
import os
import shutil

# إضافة المسار الجذري للمشروع إلى sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.process.project_management import start_app
from backend.database.database_config import get_session, init_project_database
from backend.services.project_service import ProjectManager, ProjectInfoService

def resource_path(relative_path):
    """
    ترجع المسار الصحيح للملف سواء كنت بتشغّل من الكود أو من PyInstaller .exe
    """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class HomeWindow(QWidget):
    def __init__(self, session=None, role="user", user_name="Guest", parent=None):
        super().__init__(parent)

        self.session = session
        self.role = role
        self.user_name = user_name
        
        self.setWindowTitle("Home")
        self.setStyleSheet("background-color: #002147;")
        self.setGeometry(100, 100, 900, 500)

        # تخطيط الصفحة
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(50)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # العنوان
        self.title = QLabel("المشروع")
        self.title.setFont(QFont("Arial bold", 24, QFont.Weight.Bold))
        self.title.setStyleSheet("color: white;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # تخطيط الأزرار
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(80)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # زر "المشروع الحالي"
        self.current_project_button = QPushButton()
        self.current_project_button.setFixedSize(220, 160)
        self.current_project_button.setStyleSheet("""background-color: #E5E5E5; border-radius: 20px;""")
        self.current_project_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        current_project_icon = QLabel()
        current_project_icon.setPixmap(QPixmap(resource_path("frontend/images/4.png")))
        current_project_icon.setScaledContents(True)
        current_project_icon.setFixedSize(100, 100)

        current_project_label = QLabel("فتح مشروع قديم")
        current_project_label.setFont(QFont("Arial bold", 16))
        current_project_label.setStyleSheet("color: #FFC107;")
        current_project_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        current_project_layout = QVBoxLayout(self.current_project_button)
        current_project_layout.addWidget(current_project_icon, alignment=Qt.AlignmentFlag.AlignCenter)
        current_project_layout.addWidget(current_project_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # زر "فتح مشروع جديد"
        self.new_project_button = QPushButton()
        self.new_project_button.setFixedSize(220, 160)
        self.new_project_button.setStyleSheet("""background-color: #E5E5E5; border-radius: 20px;""")
        self.new_project_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        new_project_icon = QLabel()
        new_project_icon.setPixmap(QPixmap(resource_path("frontend/images/3.png")))
        new_project_icon.setScaledContents(True)
        new_project_icon.setFixedSize(100, 100)

        new_project_label = QLabel("فتح مشروع جديد")
        new_project_label.setFont(QFont("Arial bold", 16))
        new_project_label.setStyleSheet("color: #FFC107;")
        new_project_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        new_project_layout = QVBoxLayout(self.new_project_button)
        new_project_layout.addWidget(new_project_icon, alignment=Qt.AlignmentFlag.AlignCenter)
        new_project_layout.addWidget(new_project_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # إضافة الأزرار إلى التخطيط
        buttons_layout.addWidget(self.current_project_button)
        buttons_layout.addWidget(self.new_project_button)

        # إضافة العناصر إلى التخطيط الرئيسي
        main_layout.addWidget(self.title)
        main_layout.addLayout(buttons_layout)

        # تعيين التخطيط للنافذة
        self.setLayout(main_layout)

        # ربط الأزرار
        self.current_project_button.clicked.connect(self.open_existing_project)
        self.new_project_button.clicked.connect(self.open_new_project)

    def open_existing_project(self):
        folder_path = QFileDialog.getExistingDirectory(self, "اختر مجلد المشروع", os.getcwd())
        if folder_path:
            try:
                folder_path_str = str(folder_path)
                print(f"Debug: Selected folder path: {folder_path_str}")
                start_app(operation="existing", exist_db_folder=str(folder_path_str))
                pm = ProjectManager()
                pm.set_project_path(str(folder_path_str))
                path = pm.get_project_path()
                print(f"Debug: Project path from ProjectManager: {path}")
                path_str = str(path)
                with get_session(source="database", project_path=folder_path_str) as session:
                    init_project_database(str(folder_path_str))
                    db_path = session.bind.url if session.bind else "Unknown ascendancy"
                    print(f"Debug: Initialized database at {db_path}")
                    if self.role == "system admin":
                        from frontend.main_f import StudentPlacement
                        self.window = StudentPlacement(user_name=self.user_name, role=self.role, session=session)
                    else:
                        from frontend.student import StudentPlacement as StudentPlacementStudent
                        self.window = StudentPlacementStudent(user_name=self.user_name, role=self.role, session=session)
                    self.window.show()
                    self.close()
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"فشل فتح المشروع: {str(e)}. تأكد من اختيار مجلد المشروع الصحيح .")

    def open_new_project(self):
        self.new_project_window = AddProjectForm(session=self.session, role=self.role, user_name=self.user_name, parent=self)
        self.new_project_window.show()

class AddProjectForm(QDialog):
    def __init__(self, session, role, user_name, parent=None):
        super().__init__(parent)

        self.session = session
        self.role = role
        self.user_name = user_name
        self.student_file = None
        self.preference_file = None
        self.exist_db_folder = None

        self.setWindowTitle("إضافة مشروع جديد")
        self.setStyleSheet("background-color: #D3D3D3; color: #00234E;")
        self.resize(500, 400)

        # إعداد التخطيط
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # حقل العام
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Year")
        self.year_input.setStyleSheet("font-size: 16px; padding: 8px; background-color: #00234E; color: white; border-radius: 10px;")

        # حقل المستوى
        self.level_input = QLineEdit()
        self.level_input.setPlaceholderText("Level")
        self.level_input.setStyleSheet("font-size: 16px; padding: 8px; background-color: #00234E; color: white; border-radius: 10px;")

        # حقل السيمستر
        self.term_input = QLineEdit()
        self.term_input.setPlaceholderText("Term")
        self.term_input.setStyleSheet("font-size: 16px; padding: 8px; background-color: #00234E; color: white; border-radius: 10px;")

        # حقل نوع المشروع
        self.ptype_input = QComboBox()
        self.ptype_input.setPlaceholderText("Type")
        self.ptype_input.addItems(["department", "program", "specialization"])
        self.ptype_input.setStyleSheet("font-size: 16px; padding: 8px; background-color: #00234E; color: white; border-radius: 10px;")

        # حقل الملاحظات (اختياري)
        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("ملاحظات (اختياري)")
        self.note_input.setStyleSheet("font-size: 16px; padding: 8px; background-color: #00234E; color: white; border-radius: 10px;")

        # زر اختيار مجلد قاعدة بيانات موجود
        self.exist_db_button = QPushButton("اختيار مجلد قاعدة بيانات قديمه")
        self.exist_db_button.clicked.connect(self.load_exist_db_folder)
        self.exist_db_button.setStyleSheet("font-size: 16px; padding: 8px; background-color: #CFC996; color: black; border-radius: 10px;")

        # أزرار تحميل الملفات
        self.student_file_button = QPushButton("تحميل ملف الطلاب")
        self.student_file_button.clicked.connect(self.load_student_file)
        self.student_file_button.setStyleSheet("font-size: 16px; padding: 8px; background-color: #CFC996; color: black; border-radius: 10px;")

        self.preference_file_button = QPushButton("تحميل ملف التفضيلات")
        self.preference_file_button.clicked.connect(self.load_preference_file)
        self.preference_file_button.setStyleSheet("font-size: 16px; padding: 8px; background-color: #CFC996; color: black; border-radius: 10px;")

        # زر إنشاء المشروع
        add_button = QPushButton("إنشاء المشروع")
        add_button.setStyleSheet("""
            background-color: #FDC400;
            color: black;
            font-size: 18px;
            padding: 12px;
            border-radius: 10px;
        """)
        add_button.clicked.connect(self.create_project)

        # إضافة الحقول والأزرار
        layout.addWidget(self.year_input)
        layout.addWidget(self.level_input)
        layout.addWidget(self.term_input)
        layout.addWidget(self.ptype_input)
        layout.addWidget(self.note_input)
        layout.addWidget(self.exist_db_button)
        layout.addWidget(self.student_file_button)
        layout.addWidget(self.preference_file_button)
        layout.addWidget(add_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # تعيين التخطيط
        self.setLayout(layout)

    def load_student_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("All Files (*.*)")
        if file_dialog.exec():
            self.student_file = file_dialog.selectedFiles()[0]
            self.student_file_button.setText(f"ملف الطلاب: {os.path.basename(self.student_file)}")

    def load_preference_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("All Files (*.*)")
        if file_dialog.exec():
            self.preference_file = file_dialog.selectedFiles()[0]
            self.preference_file_button.setText(f"ملف التفضيلات: {os.path.basename(self.preference_file)}")

    def load_exist_db_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "اختر مجلد قاعدة بيانات موجود", os.getcwd())
        if folder_path:
            self.exist_db_folder = str(folder_path)
            self.exist_db_button.setText(f"مجلد قاعدة بيانات: {os.path.basename(folder_path)}")

    def create_project(self):
        year = self.year_input.text().strip()
        level = self.level_input.text().strip()
        term = self.term_input.text().strip()
        ptype = self.ptype_input.currentText()
        note = self.note_input.text().strip() if self.note_input.text().strip() else None

        if not year or not level or not term:
            QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول (العام، المستوى، الفصل)")
            return

        if not self.student_file or not self.preference_file:
            QMessageBox.warning(self, "خطأ", "يرجى تحميل ملف الطلاب وملف التفضيلات")
            return

        try:
            project_name = f"ClassInfo_{year}_{level}_{term}_{ptype}"
            base_dir = os.path.dirname(os.path.abspath(__file__))
            assist_folder = os.path.join(base_dir, 'assist')

            start_app(
                operation="new",
                year=year,
                level=level,
                term=term,
                ptype=ptype,
                student_file=str(self.student_file),
                preference_file=str(self.preference_file),
                exist_db_folder=self.exist_db_folder,
                note=note
            )
            pm = ProjectManager()
            pm.set_project_path(str(project_name))
            path = pm.get_project_path()
            print(f"Debug: Project path from ProjectManager: {path}")
            path_str = str(path)

            if os.path.exists(assist_folder):
                project_assist_folder = os.path.join(path_str, 'assist')
                if not os.path.exists(project_assist_folder):
                    shutil.copytree(assist_folder, project_assist_folder)
                print(f"Debug: Copied assist folder to {project_assist_folder}")

            with get_session(source="database", project_path=path_str) as session:
                init_project_database(str(path_str))
                QMessageBox.information(self, "نجاح", "تم إنشاء المشروع بنجاح!")
                if self.role == "system admin":
                    from frontend.main_f import StudentPlacement
                    self.window = StudentPlacement(user_name=self.user_name, role=self.role, session=session)
                else:
                    from frontend.student import StudentPlacement as StudentPlacementStudent
                    self.window = StudentPlacementStudent(user_name=self.user_name, role=self.role, session=session)
                self.window.show()
                self.accept()
                self.parent().close()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل إنشاء المشروع: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec())