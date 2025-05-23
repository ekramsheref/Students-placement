# services/project_service.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))




from sqlalchemy.orm import Session
from backend.database.models import ProjectInfo

# project_manager.py

class ProjectManager:
    _instance = None
    _project_path = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProjectManager, cls).__new__(cls)
        return cls._instance

    def set_project_path(self, path: str):
        self._project_path = path

    def get_project_path(self) -> str:
        if self._project_path is None:
            raise ValueError("Project path is not set.")
        return self._project_path


# Example usage:
# from project_manager import ProjectManager
#
# pm = ProjectManager()
# print(pm.get_project_path())



class ProjectInfoService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str, ptype: str, db_directory: str, note: str = None):
        new_project = ProjectInfo(
            name=name,
            ptype=ptype,
            db_directory=db_directory,
            Note=note
        )
        self.session.add(new_project)
        self.session.commit()
        return new_project

    def get(self, project_id: int = 1):
        return self.session.get(ProjectInfo, project_id)

    # def get_all(self):
    #     return self.session.query(ProjectInfo).all()

    def update(self, name: str = None, ptype: str = None,
               db_directory: str = None, note: str = None, project_id: int = 1):
        project = self.get(project_id)
        if not project:
            return None

        if name is not None:
            project.name = name
        if ptype is not None:
            project.ptype = ptype
        if db_directory is not None:
            project.db_directory = db_directory
        if note is not None:
            project.Note = note

        self.session.commit()
        return project

    def update_db_directory(self, new_db_directory: str, project_id: int=1):
        """
        Specific method for updating only the db_directory
        """
        project = self.get(project_id)
        if not project:
            return None

        project.db_directory = new_db_directory
        self.session.commit()
        return project

    def delete(self, project_id: int =1):
        project = self.get(project_id)
        if not project:
            return None

        self.session.delete(project)
        self.session.commit()
        return project

    def get_project_type(self, project_id: int = 1):
        project = self.get(project_id)
        if not project:
            return None
        return project.ptype
