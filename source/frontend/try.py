#try.py
import pandas as pd
import re

file_path = r'D:\PythonProject\Students_Data_Final.xlsx'

excel_file = pd.ExcelFile(file_path)
df = excel_file.parse('CTRL_Term_Bigsheet_CoursesGrade', skiprows=4)

df.columns = [str(col).strip() for col in df.columns]

id_col = 'رقم الجلوس'
name_col = 'الاسم'

course_columns = df.columns[df.columns.get_loc('المقررات'):]

def extract_hours(course_text):
    if isinstance(course_text, str):
        match = re.search(r'\((\d+(?:\.\d+)?)\s*ساعة\)', course_text)
        if match:
            return float(match.group(1))
    return None

output_rows = []

for idx in range(0, len(df), 2):
    if idx + 1 >= len(df):
        break

    row_info = df.iloc[idx]
    row_grades = df.iloc[idx + 1]

    student_id = row_info.get(id_col)
    student_name = row_info.get(name_col)

    if pd.isna(student_id) or pd.isna(student_name):
        continue

    for col in course_columns:
        course_name = row_info.get(col)
        grade_cell = row_grades.get(col)

        # تعديل مهم: استخدام الرقم الأصفر (المعدل) في حال وجود أكثر من قيمة
        if isinstance(grade_cell, str) and '\n' in grade_cell:
            parts = grade_cell.split('\n')
            numeric_grade = parts[1] if len(parts) > 1 else parts[0]
        else:
            numeric_grade = grade_cell

        if pd.notna(course_name) and pd.notna(numeric_grade):
            hours = extract_hours(course_name)
            main_course_name = course_name.split('\n')[0] if isinstance(course_name, str) else course_name

            output_rows.append({
                'ID': student_id,
                'اسم الطالب': student_name,
                'المقرر': main_course_name,
                'المعدل': numeric_grade,
                'عدد الساعات': hours
            })

    # المعدل الفصلي والتراكمي
    term_gpa = row_info.get('المعدل الفصلى')
    cumulative_gpa = row_info.get('المعدل التراكمي')
    total_hours = row_info.get('مجموع الساعات')

    output_rows.append({
        'ID': student_id,
        'اسم الطالب': student_name,
        'المقرر': 'المعدل الفصلى',
        'المعدل': term_gpa,
        'عدد الساعات': total_hours
    })

    output_rows.append({
        'ID': student_id,
        'اسم الطالب': student_name,
        'المقرر': 'المعدل التراكمى',
        'المعدل': cumulative_gpa,
        'عدد الساعات': None
    })

df_output = pd.DataFrame(output_rows)

output_path = r'd:\PythonProject\Converted_Student_Data_v5.csv'
df_output.to_csv(output_path, index=False, encoding='utf-8-sig')

print("✅ تم حفظ الملف كـ CSV في:", output_path)
