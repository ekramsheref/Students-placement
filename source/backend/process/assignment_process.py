# process/assignment_process.py

seats_dict = {}


def pass_required_subjects(student, required_subjects):
    if not required_subjects:
        return True

    for subject in required_subjects:
        for studied_subject in student.student_grades:
            if subject.name == studied_subject.name:
                if studied_subject.points < subject.min_grade:
                    return False
    return True


def is_within_capacity(name):
    global seats_dict
    return seats_dict[name] >= 1


def is_eligible_for_program(student, program):
    return (student.gpa >= program.gpa_threshold and
            pass_required_subjects(student, program.subjects_required) and
            is_within_capacity(program.name))


class AssignmentProcess:

    def __init__(self, student_service, program_service, specialization_service, department_service, project_service):
        self.student_service = student_service
        self.program_service = program_service
        self.specialization_service = specialization_service
        self.department_service = department_service
        self.project_service = project_service

    def assign_students(self):
        project_type = self.project_service.get_project_type()
        students = self.student_service.ranked_students()
        self.set_seats_dict()

        # print("project_type:", project_type)
        #
        # print("Students ranked by GPA:")
        # for student in students:
        #     print(f"ID: {student.id_num}, Name: {student.name}, GPA: {student.gpa}")
        #
        # print("Seats available:")
        # for name, seats in seats_dict.items():
        #     print(f"{name}: {seats} seats")

        for student in students:
            preferences = student.preferences
            if project_type == 'program':
                # print(f"Assigning {student.name} to program based on preferences: {preferences}")
                self.assign_to_program(student, preferences)
            # elif project_type == 'specialization':
            #     self.assign_to_specialization(student, preferences)
            # elif project_type == 'department':
            #     self.assign_to_department(student, preferences)

    def assign_to_program(self, student, preferences):
        programs = self.program_service.get_all()
        for preference in preferences:
            for program in programs:
                # print(f"Checking preference: {preference.name.strip()} against program: {program.name.strip()}")
                if program.name.strip() == preference.name.strip():
                    print(f"Checking eligibility for {student.name} in {program.name}")
                    if is_eligible_for_program(student, program):
                        print(f"Assigning {student.name} to {program.name}")
                        self.student_service.assign_to_prefered_program(student.id_num, program.id, program.name)
                        return

    # def assign_to_specialization(self, student, preferences):
    #     specializations = self.specialization_service.get_all_specializations()
    #     for preference in preferences:
    #         for specialization in specializations:
    #             if specialization.id == preference.specialization_id and self.is_eligible_for_specialization(student, specialization):
    #                 self.student_service.assign_to_specialization(student.id, specialization.id)
    #                 return

    # def assign_to_department(self, student, preferences):
    #     departments = self.department_service.get_all_departments()
    #     for preference in preferences:
    #         for department in departments:
    #             if department.id == preference.department_id and self.is_eligible_for_department(department):
    #                 self.student_service.assign_to_department(student.id, department.id)
    #                 return

    # def is_eligible_for_specialization(self, student, specialization):
    #     return (student.gpa >= specialization.gpa_threshold and
    #             pass_required_subjects(student, specialization.subjects_required) and
    #             is_within_capacity(specialization.name))
    #
    # def is_eligible_for_department(self, department):
    #     return is_within_capacity(department.name)

    def set_seats_dict(self):
        global seats_dict

        project_type = self.project_service.get_project_type()
        if project_type == 'program':
            programs = self.program_service.get_all()
            for program in programs:
                seats_dict[program.name.strip()] = program.student_capacity
        elif project_type == 'specialization':
            specializations = self.specialization_service.get_all()
            for specialization in specializations:
                seats_dict[specialization.name.strip()] = specialization.student_capacity
        elif project_type == 'department':
            departments = self.department_service.get_all()
            for department in departments:
                seats_dict[department.name.strip()] = department.student_capacity
