import re
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from backend.services.student_service import StudentService
from backend.services.student_grades_service import StudentGradesService
from backend.services.preferences_service import PreferencesService

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names:
    - lowercase all letters
    - replace spaces with underscores
    - remove leading/trailing whitespace
    - replace non-alphanumeric characters with underscores
    - collapse multiple underscores
    """

    def clean(col):
        col = col.strip()  # remove leading/trailing spaces
        col = col.lower()  # lowercase
        col = re.sub(r'\s+', '_', col)  # spaces/tabs to underscores
        col = re.sub(r'[^\w]', '_', col)  # non-word characters to underscores
        col = re.sub(r'_+', '_', col)  # collapse multiple underscores
        col = col.strip('_')  # remove leading/trailing underscores
        return col

    df.columns = [clean(col) for col in df.columns]
    return df


class StudentDataProcessor:
    def __init__(self, student_file, form_file, session: Session):
        self.student_file = Path(student_file)
        self.form_file = Path(form_file)
        self.df_grades = pd.read_csv(Path(student_file))
        self.df_form = pd.read_csv(Path(form_file))
        self.session = session

    def create_student_table(self):
        # Clean column names
        self.df_grades = clean_column_names(self.df_grades)
        self.df_form = clean_column_names(self.df_form)
        # Extract emails from the form
        df_emails = self.df_form[['id', 'email']]

        # Filter to get only cumulative GPA rows
        df_gpa = self.df_grades.query('subject_code == "المعدل التراكمى"')
        df_gpa = df_gpa.drop(columns=['subject_code', 'cridet_hours'])

        # Merge GPA data with emails
        df_student_table = pd.merge(df_gpa, df_emails, on='id')

        return df_student_table

    def create_student_grade_table(self, student_table):
        # Clean column names
        self.df_grades = clean_column_names(self.df_grades)

        # Filter out non-subject rows
        df_subjects = self.df_grades.query(
            'subject_code != "المعدل الفصلى" and subject_code != "المعدل التراكمى"'
        )
        df_subjects = df_subjects.drop(columns=['name'])

        # Keep only rows with IDs in student_table
        df_subjects = df_subjects[df_subjects['id'].isin(student_table['id'])]

        return df_subjects

    def create_student_preference_table(self):
        # Clean column names
        self.df_form = clean_column_names(self.df_form)
        # Drop name and Email columns
        df_raw = self.df_form.drop(columns=['name', 'email'])

        preference_cols = ['first_prefrence', 'second_prefrence', 'third_prefrence', 'forth_prefrence',
                           'fifth_prefrence', 'sixth_prefrence']

        existing_cols = [col for col in preference_cols if col in df_raw.columns]

        # Melt to long format
        df_melted = df_raw.melt(
            id_vars=['id'],
            value_vars=existing_cols,
            var_name='preference_type',
            value_name='preference'
        )

        # Map preference order
        pref_map = {
            'first_prefrence': 1,
            'second_prefrence': 2,
            'third_prefrence': 3,
            'forth_prefrence': 4,
            'fifth_prefrence': 5,
            'sixth_prefrence': 6
        }
        df_melted['preference_order'] = df_melted['preference_type'].map(pref_map)

        # Drop unneeded column and sort
        df_preference = df_melted.drop(columns=['preference_type'])
        df_preference = df_preference.sort_values(by=['id', 'preference_order'])

        return df_preference

    def process_all_data(self):
        # Generate the student table, grade table, and preference table
        student_table = self.create_student_table()
        student_grades = self.create_student_grade_table(student_table)
        student_preferences = self.create_student_preference_table()

        student_service = StudentService(self.session)
        student_service.add_df(student_table)

        student_grades_service = StudentGradesService(self.session)
        student_grades_service.add_df(student_grades)

        student_preferences_service = PreferencesService(self.session)
        student_preferences_service.add_df(student_preferences)

