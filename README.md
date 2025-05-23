# Students-placement

## Project Overview
The Students-placement system is a desktop application designed to streamline the process of assigning students to specialized departments within educational institutions. It enhances administrative efficiency and accuracy by automating the evaluation of student preferences against department eligibility criteria. The application features a user-friendly graphical interface built with PyQt6 and a secure SQLite database managed via SQLAlchemy. It supports role-based access control with secure password hashing using bcrypt, and integrates pandas and openpyxl for data manipulation and Excel file handling.

## Features
- Automated Processing: Assigns students to departments based on preferences and eligibility (e.g., GPA, specialization) without manual input.
- Program Management: Admins can add, update, and manage department programs and set enrollment criteria.
- User Access Control: Provides access to key statistics (GPA, enrollment data, popular choices) with user-specific permissions.
- Statistics: Secure data management with tools to control access and modification rights.
- Data Import/Export: Supports Excel file integration for efficient data handling.

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
   - Clone: `git clone <repository-url> && cd students-placement`
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
   - Continuing an old project: Use `Data/Class_2024` folder for existing SQLite database.
   - Starting a new project: Use `Data/Class_2024` as reference, plus `Files/Converted_Student_Data_v4` and `Files/form` for student data and templates.

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
