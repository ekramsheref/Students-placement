# from backend.services.admin_service import AdminService
# # from backend.database.database_config import get_session, init_user_db, init_project_db
# #
# #
# #
# # # Initialize the database
# #
# # init_user_db()
# # init_project_db("Class 2025")
# #
# # # Create a session
# # with get_session() as session:
# #     # Example usage of the session
# #     admin_service = AdminService(session)
# #
# #     # Add a new admin
# #     # admin_service.create("Ahmed Hussein", "ramen_goblin", "123", "admin")
# #
# #     # # Method to set password (hashing)
# #     # admin_service.login("ramen_goblin", "123")
# #     # print("hi hi \n")
# #     # admin_service.login("ramen_goblin", "000")
#
#
# from backend.process.project_management import (
#     init_new_project,
#     start_new_project_with_university_data,
#     open_existing_project
# )
# from backend.database.database_config import get_session
# from backend.services.faculty_service import FacultyService
# import os
#
#
# # Define project names and paths
# new_project_name = "Class 2027"
# existing_project_path = "../data/Class 2025"
#
# # # Initialize new project
# #
# # init_new_project(new_project_name)
# #
# # project_path = os.path.join("../data/", new_project_name)
# #
# # with get_session("database", project_path) as session:
# #
# #     faculity_service = FacultyService(session)
# #
# #     faculity_service.create("Engineering")
#
#
# # # Initialize new project with university data
#
# start_new_project_with_university_data(new_project_name, existing_project_path)
#
#
#
#
#
# # # Initialize new project with university data
# # start_new_project_with_university_data(new_project_name, "../data/university")
#
# # Open existing project
# # open_existing_project(existing_project_path)
# #
# # with get_session("database", existing_project_path) as session:
# #
# #     faculity_service = FacultyService(session)
# #
# #     faculity_service.create("Engineering")
#
#
#
#
# # with get_session() as session:
# #     # Example usage of the session
# #     admin_service = AdminService(session)
# #     # Add a new admin
# #     admin_service.create("Ahmed Hussein", "ramen_goblin", "123", "admin")
# #     admin_service.create("Yousif Ahmed", "zoota", "456", "admin")
# #     admin_service.create("Eman", "Emo", "456", "system admin")
#
#
#
# # import os
# #
# # from sqlalchemy import create_engine, MetaData
# # # from backend.database.database_config import BASE_PATH
# #
# # BASE_PATH = "../data/"
# #
# # project_name = "Class 2027"
# # prev_project_path = "../data/Class 2025"
# #
# #
# # tables_to_copy = ["faculty", "department", "program", "specialization", "subjects_required", "department_head"]
# # prev_db_path = os.path.join(prev_project_path, "database.db")
# #
# #
# # project_path = os.path.join(BASE_PATH, project_name)
# # project_db_path = os.path.join(project_path, "database.db")
# #
# #
# # source_engine = create_engine(f"sqlite:///{prev_db_path}", echo=True)
# # target_engine = create_engine(f"sqlite:///{project_db_path}", echo=True)
# #
# # source_metadata = MetaData()
# # source_metadata.reflect(bind=source_engine, only=tables_to_copy)
# #
# # target_metadata = MetaData()
# # target_metadata.reflect(bind=target_engine)
# #
# # with source_engine.connect() as source_conn, target_engine.connect() as target_conn:
# #     for table in source_metadata.sorted_tables:
# #         table_name = table.name
# #
# #         # Create the table in the target if not exists
# #         table.metadata.create_all(target_engine)
# #
# #         rows = source_conn.execute(table.select()).fetchall()
# #
# #         column_names = [column.name for column in table.columns()]
# #
# #         rows_to_insert = [dict(zip(column_names, row)) for row in rows]
# #
# #         if rows_to_insert:
# #             print(f"Inserting {len(rows_to_insert)} row(s) into '{table_name}'...")
# #             target_conn.execute(table.insert(), rows_to_insert)
# #
# #
# #
# #
# #
# #
# #
# # def copy_fixed_tables_to_project(
# #     university_folder: str,
# #     project_name: str,
# #     skip_existing_tables: bool = False,
# #     clear_existing_data: bool = False
# # ):
# #     """Copy fixed tables from university DB to project DB."""
# #     tables_to_copy = ["faculty", "department", "program", "specialization", "subjects_required", "department_head"]
# #     university_db_path = os.path.join(university_folder, "database.db")
# #
# #     project_path = os.path.join(BASE_PATH, project_name)
# #     project_db_path = os.path.join(project_path, "database.db")
# #
# #     source_engine = create_engine(f"sqlite:///{university_db_path}", echo=True)
# #     target_engine = create_engine(f"sqlite:///{project_db_path}", echo=True)
# #
# #     source_metadata = MetaData()
# #     source_metadata.reflect(bind=source_engine, only=tables_to_copy)
# #
# #     target_metadata = MetaData()
# #     target_metadata.reflect(bind=target_engine)
# #
# #     with source_engine.connect() as source_conn, target_engine.connect() as target_conn:
# #         for table in source_metadata.sorted_tables:
# #             table_name = table.name
# #             if skip_existing_tables and table_name in target_metadata.tables:
# #                 print(f"Skipping '{table_name}' (already exists).")
# #                 continue
# #
# #             # Create the table in the target if not exists
# #             table.metadata.create_all(target_engine)
# #
# #             if clear_existing_data:
# #                 target_conn.execute(table.delete())  # Use table.delete() to clear the table
# #
# #             # Fetch data and convert each row to a dictionary format
# #             rows = source_conn.execute(table.select()).fetchall()
# #             column_names = [column.name for column in table.columns]
# #
# #             # Convert rows to dictionaries
# #             rows_to_insert = [dict(zip(column_names, row)) for row in rows]
# #
# #             if rows_to_insert:
# #                 print(f"Inserting {len(rows_to_insert)} row(s) into '{table_name}'...")
# #                 target_conn.execute(table.insert(), rows_to_insert)
# #
# #     print("Finished copying selected university tables.")

# from backend.process.project_management import open_existing_project

# Initialize the database

# open_existing_project("Z:\projects new\Graduation project\data\Class 2025")

# Create a session

from backend.database.database_config import get_session
from backend.process.assignment_process import AssignmentProcess
#
# from backend.process.project_management import start_app
# start_app(operation="existing",
#           exist_db_folder="Z:\projects new\Graduation project\data\ClassInfo_2025_2_1_department")
#
# #
#
#
#
#
#
#
from backend.process.project_management import start_app
from backend.services.department_service import DepartmentService
from backend.services.program_service import ProgramService
from backend.services.project_service import ProjectInfoService
from backend.services.project_service import ProjectManager
from backend.services.student_service import StudentService

# Initialize user database
# init_user_db()
# get session
# Create a session
# with get_session() as session:
#     admin_service = AdminService(session)
#
#     user_name = "ramen_goblin"
#     password = "123"
#
#     admin_service.login(user_name, password)
# start(operation="existing",
#       exist_db_folder="Z:\projects new\Graduation project\data\ClassInfo_2025_2_1_department",
#       )
# start(operation="existing",
#       exist_db_folder="Z:\projects new\ClassInfo_2025_2_1_department"
# )
# pm = ProjectManager()
# path = pm.get_project_path()
#
# from backend.services.student_service import StudentService
#
# with get_session("database", path) as session:
#     student_service = StudentService(session)
#
#     student1 = student_service.create(
#         id_num="123456",
#         name="Ahmed",
#         email="a@gmail.com",
#         gpa=3.5,
#         preference_names=["CS", "AI", "ML"]
#     )
# start_app(operation="new",
#         year=2025,
#         level=2,
#         term=1,
#         ptype="department",
#         student_file=None,
#         prefrence_file=None,
#         note=None
#     )

# start_app(operation="new",
#           year=2029,
#           level=2,
#           term=1,
#           ptype='program',
#           student_file=r"Z:\projects new\Graduation project\Department-Specialization-for-Students\files\Converted_Student_Data_v4.csv",
#           preference_file=r"Z:\projects new\Graduation project\Department-Specialization-for-Students\files\form.csv",
#           note=None
#           )

start_app(operation="existing",
          exist_db_folder=r"Z:\projects new\Graduation project\data\ClassInfo_2029_2_1_program",
          )

pm = ProjectManager()
path = pm.get_project_path()
with get_session("database", path) as session:
    # from backend.services.student_service import StudentService

    student_service = StudentService(session)
    #
    # # Fetch all students
    # all_students = student_service.get_all()
    # for student in all_students:
    #     print(f"ID: {student.id_num}, Name: {student.name}, GPA: {student.gpa}")
    #
    # # add department
    # from backend.services.department_service import DepartmentService
    # department_service = DepartmentService(session)
    # dep1= department_service.create("Mathematics")
    # department_service.create("Physics")
    #
    # # add program
    # from backend.services.program_service import ProgramService
    program_service = ProgramService(session)
    #
    # program_service.create("الاحصاء الرياضي", dep1.id, 1, 50)
    # program_service.create("علوم الحاسب", dep1.id, 2, 50)
    # program_service.create("رياضيات", dep1.id, 1, 50)

    # add specialization
    from backend.services.specialization_service import SpecializationService

    specialization_service = SpecializationService(session)

    department_service = DepartmentService(session)

    A = AssignmentProcess(student_service, program_service, specialization_service, department_service,
                          ProjectInfoService(session))

    A.assign_students()
