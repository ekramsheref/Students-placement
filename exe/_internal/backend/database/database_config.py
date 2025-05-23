from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from .base_models import UserBase, ProjectBase

BASE_PATH = Path("../data").resolve()  # Normalize base path

user_db_uri = f"sqlite:///{BASE_PATH / 'user_info.db'}"
user_engine = create_engine(user_db_uri, echo=True)


from pathlib import Path

def get_db_path(project_name: str) -> Path:
    if not project_name:
        raise ValueError("Project name is not set.")
    base = Path("../data").resolve()
    project_path = base / project_name  # Use pathlib to join paths
    project_path.mkdir(parents=True, exist_ok=True)  # Ensure the project directory exists
    db_path = base / project_name / "database.db"
    return db_path

def init_user_db():
    """Initialize the global user database."""

    BASE_PATH.mkdir(parents=True, exist_ok=True)

    UserBase.metadata.create_all(user_engine)
    print("GlobalBase and its tables created successfully.")

def get_project_engine(project_name: str):
    """Get the SQLAlchemy engine for the project database."""
    db_path = get_db_path(project_name) # Use pathlib to construct the path
    return create_engine(f"sqlite:///{db_path}", echo=True)

def init_project_database(project_name: str):
    """Initialize the project database at the specified path."""
    project_engine = get_project_engine(project_name)
    ProjectBase.metadata.create_all(project_engine)
    print(f"Database for project created at '{get_db_path(project_name)}'")


def copy_fixed_tables_to_project(university_folder: str, project_name: str):
    """
    Copy fixed tables from university DB to the new project's DB.
    The list of tables is constant and copied every time.
    """
    tables_to_copy = [
        "department", "program", "specialization",
        "subjects_required", "department_head"
    ]

    university_db_path = Path(university_folder) / "database.db"  # Normalize path using pathlib
    project_db_path = get_db_path(project_name)  # Normalize path for project DB

    # Create engines for both DBs
    source_engine = create_engine(f"sqlite:///{university_db_path}", echo=True)
    target_engine = create_engine(f"sqlite:///{project_db_path}", echo=True)

    # Reflect only the needed tables from source
    source_metadata = MetaData()
    source_metadata.reflect(bind=source_engine, only=tables_to_copy)

    # Reflect current target metadata to avoid errors on create
    target_metadata = MetaData()
    target_metadata.reflect(bind=target_engine)

    with source_engine.connect() as source_conn, target_engine.connect() as target_conn:
        with target_conn.begin():
            for table in source_metadata.sorted_tables:
                table_name = table.name
                print(f"Processing table: {table_name}")

                # Create the table in the target (if it doesn't already exist)
                if table_name not in target_metadata.tables:
                    table.metadata.create_all(target_engine)

                # Read rows from source
                rows = source_conn.execute(table.select()).fetchall()
                column_names = [column.name for column in table.columns]
                rows_to_insert = [dict(zip(column_names, row)) for row in rows]

                # Insert into target
                if rows_to_insert:
                    print(f"Inserting {len(rows_to_insert)} row(s) into '{table_name}'...")
                    target_conn.execute(table.insert(), rows_to_insert)
                else:
                    print(f"No rows found in '{table_name}' to insert.")

    print("Finished copying fixed tables.")


UserSessionFactory = sessionmaker(bind=user_engine)


def get_project_session_factory(project_path: str):
    """Get session factory for the project database."""
    project_engine = get_project_engine(project_path)
    return sessionmaker(bind=project_engine)


@contextmanager
def get_session(source: str = "user", project_path: str = None):
    """Context manager for obtaining a database session."""
    if source == "user":
        session_factory = UserSessionFactory
    elif source == "database":
        if not project_path:
            raise ValueError("project_path is required for project session")
        session_factory = get_project_session_factory(project_path)
    else:
        raise ValueError("Invalid source. Choose 'user' or 'database'.")

    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
