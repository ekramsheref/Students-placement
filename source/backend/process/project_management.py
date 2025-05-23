# backend/database/process/project_management.py

from .student_data_processor import StudentDataProcessor
from backend.database.database_config import init_project_database, copy_fixed_tables_to_project, get_session
from backend.services.project_service import ProjectInfoService, ProjectManager


def start_app(operation="existing",  # "existing" or "new"
              exist_db_folder=None,  # if prev project or we will load prev data
              year=None,
              level=None,
              term=None,
              ptype=None,  # "department" or "program" or "specialization"
              student_file=None,
              preference_file=None,
              note=None):
    # -> new without old data

    # -> new with old data

    # -> existing with old data

    pm = ProjectManager()
    if operation == "existing":
        # Open an existing project
        pm.set_project_path(exist_db_folder)
        init_project_database(exist_db_folder)


    elif operation == "new":
        project_name = f"ClassInfo_{year}_{level}_{term}_{ptype}"

        init_project_database(project_name)

        if exist_db_folder:
            copy_fixed_tables_to_project(
                university_folder=exist_db_folder,
                project_name=project_name,
                # skip_existing_tables=True,
                # clear_existing_data=False
            )

        with get_session("database", project_name) as session:
            # Create a new project
            path = project_name
            pm.set_project_path(path)
            project_service = ProjectInfoService(session)
            project_service.create(
                name=project_name,
                ptype=ptype,
                db_directory=path,
                note=note
            )
            data_proc = StudentDataProcessor(student_file, preference_file, session)
            data_proc.process_all_data()
