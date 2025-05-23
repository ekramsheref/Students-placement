# Students-placement

## Project Overview
This project is designed to streamline the process of assigning students to specialized departments within educational institutions. The system enhances administrative efficiency and accuracy by automating the evaluation of student preferences against department eligibility criteria.

## Features
Automated Processing: Automatically assigns students to departments based on preferences and eligibility (e.g., GPA, specialization) without manual input.
Program Management: Admins can add, update, and manage department programs and set enrollment criteria.
User Access Control: This feature provides access to key statistics (GPA, enrollment data, popular choices) with user-specific permissions.
Statistics: Secure data management with tools to control access and modification rights.


## Prerequisites

To set up and run the Student Affairs Management System, ensure your system meets the following requirements:

### Software Dependencies
The following Python libraries are required:
- SQLAlchemy (~2.0.39): For database management
- PyQt6 (~6.7.1): For the graphical user interface
- bcrypt (~4.3.0): For secure password hashing
- pandas (~2.0.3): For data manipulation
- openpyxl (~3.1.5): For Excel file integration

### Required Build Tools
- Python 3.9+: Download from https://www.python.org/downloads/
- pip: Python package manager (included with Python)
- Git: Optional, for cloning the project repository (download from https://git-scm.com/downloads)

## Setup Instructions

The Student Affairs Management System is a Python-based application that requires setting up a Python environment and installing dependencies. Follow these step-by-step instructions to set up and run the project on Windows or macOS.

أنا فاهمة إنك عايزة طريقة عرض الملفات (زي الـ README.md أو ملفات المشروع) بشكل أصغر أو أكثر ترتيبًا، ويمكن تقصدي إن التعليمات (مثل خطوات الفتح أو التشغيل) تكون مكتوبة بشكل موجز أكتر ومرتبة تحت بعض بطريقة أوضح وأقل حجمًا. لو قصدك شيء تاني زي طريقة عرض الملفات في واجهة المشروع نفسه أو شيء متعلق بالواجهة الرسومية، ممكن توضحي أكتر؟

بناءً على فهمي، هعدل قسم Setup Instructions في الـ README.md عشان يكون أصغر وأوضح، مع الإبقاء على كل التفاصيل المهمة (تثبيت Python، إعداد المكتبات، تشغيل التطبيق، إلخ) لنظامي Windows وmacOS. هحط التعليمات في نقاط مرقمة مختصرة، مرتبة تحت بعض، من غير تفاصيل زيادة. هكرر المحتوى الكامل للـ README.md مع تعديل قسم Setup Instructions بس، عشان تقدري تنسخيه مباشرة كملف نصي وتحطيه في README.md.

محتوى ملف README.md (بتعديل مختصر لقسم Setup Instructions)
text

نسخ
# Student Affairs Management System

## Project Overview
The Student Affairs Management System is a desktop application designed to streamline and automate student affairs processes for educational institutions. It simplifies tasks such as managing student records, class data, and administrative operations. The application features a user-friendly graphical interface built with PyQt6 and a secure SQLite database managed via SQLAlchemy. It supports role-based access control with secure password hashing using bcrypt, and integrates pandas and openpyxl for data manipulation and Excel file handling. This system is ideal for administrators and student affairs staff seeking an efficient and intuitive tool to manage student-related data.

## Features
- Role-based access for Admin and Student Affairs interfaces
- Secure user authentication with bcrypt
- SQLite database for robust data storage
- Data import/export with Excel file support
- User-friendly PyQt6 interface for seamless interaction

## Prerequisites

### System Requirements
- Operating System: Windows 10/11 (64-bit) or macOS 11 (Big Sur) or later
- Python Version: Python 3.9 or higher
- Disk Space: At least 500 MB of free disk space
- Memory: Minimum 4 GB RAM (8 GB recommended)
- Internet Connection: Required for installing dependencies

### Software Dependencies
- SQLAlchemy (~2.0.39): For database management
- PyQt6 (~6.7.1): For the graphical user interface
- bcrypt (~4.3.0): For secure password hashing
- pandas (~2.0.3): For data manipulation
- openpyxl (~3.1.5): For Excel file integration

### Required Build Tools
- Python 3.9+: Download from https://www.python.org/downloads/
- pip: Python package manager (included with Python)
- Git: Optional, for cloning the project repository (download from https://git-scm.com/downloads)

## Setup Instructions

1. **Get the Project**:
   - Clone: `git clone <repository-url> && cd student-affairs-management-system`
   - Or download and extract the project folder.
   - Ensure it has: `login.py`, `Data/Class_2024`, `Files/Converted_Student_Data_v4`, `Files/form`.

2. **Install Python**:
   - Windows: Download from python.org, check "Add Python to PATH", verify with `python --version`.
   - macOS: Download from python.org, verify with `python3 --version`.

3. **Set Up Virtual Environment**:
   - Windows: `python -m venv venv && venv\Scripts\activate`
   - macOS: `python3 -m venv venv && source venv/bin/activate`

4. **Install Libraries**:
   - Run: `pip install SQLAlchemy==2.0.39 PyQt6==6.7.1 bcrypt==4.3.0 pandas==2.0.3 openpyxl==3.1.5`
   - Verify: `pip list`

5. **Configure Data**:
   - Existing project: Ensure `Data/Class_2024` exists.
   - New project: Ensure `Data/Class_2024`, `Files/Converted_Student_Data_v4`, `Files/form` exist.

6. **Run Application**:
   - Windows: `python login.py`
   - macOS: `python3 login.py`

7. **Log In**:
   - Admin: Username `Eman`, Password `111`
   - Student Affairs: Username `Ekram`, Password `333`

  
## Usage Guide
Once logged in, the application provides two interfaces:

- Admin Interface:
  - Add/update department programs and set enrollment criteria.
  - Manage user accounts and access rights.
  - View statistics (GPA, enrollment, popular choices) and export to Excel.

- Student Affairs Interface:
  - View and update student records and department assignments.
  - Import/export student data using Excel files.
 
    
## Troubleshooting Common Issues

1. Python Not Found:
   - Ensure Python is installed and added to PATH.
   - Windows: Reinstall and check "Add Python to PATH".
   - macOS: Use `python3` instead of `python`.

2. Module Not Found Error:
   - Verify virtual environment is activated ((venv) in terminal).
   - Reinstall dependencies with pip install command.
   - Use specified versions (e.g., SQLAlchemy==2.0.39).

3. Database Connection Issues:
   - Check `Data/Class_2024` exists with SQLite database.
   - Ensure read/write permissions for project directory.
   - Consult documentation for initializing a new database.

4. PyQt6 Window Not Displaying:
   - Check for compatible display drivers.
   - macOS: Grant terminal screen access (System Settings > Privacy & Security > Screen Recording).
   - Windows: Update graphics drivers.

5. Excel File Errors:
   - Ensure `Files/Converted_Student_Data_v4` and `Files/form` files are not corrupted and in .xlsx format.

6. Login Issues:
   - Verify username/password (case-sensitive).
   - Ensure SQLite database has user data.

For additional help, open an issue on the project's repository (if available) or contact the project maintainer.
