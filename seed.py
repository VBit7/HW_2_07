from connect_db import session

from faker import Faker
from models import Groups, Students, Teachers, Subjects, Grades
from random import randint, choice

NUMBER_TEACHERS = 5
NUMBER_SUBJECTS = 8
NUMBER_GROUPS = 3
NUMBER_STUDENTS = 50
NUMBER_GRADES = 20

faker = Faker()

fake_subjects = [
    "Introduction to Computer Science",
    "Principles of Economics",
    "Calculus I",
    "English Composition",
    "Introduction to Psychology",
    "World History",
    "Biology Fundamentals",
    "Art Appreciation",
    "Environmental Science",
    "Business Management Theory"
]

def db_populate():
    try:
        list_groups = []
        for i in range(1, NUMBER_GROUPS + 1):
            n_group = Groups(group_name=f'Group {i}')
            list_groups.append(n_group)
        session.add_all(list_groups)

        list_students = []
        for i in range(1, NUMBER_STUDENTS + 1):
            n_student = Students(full_name=faker.name(), group=choice(list_groups))
            list_students.append(n_student)
        session.add_all(list_students)

        list_teachers = []
        for i in range(1, NUMBER_TEACHERS + 1):
            n_teacher = Teachers(full_name=faker.name())
            list_teachers.append(n_teacher)
        session.add_all(list_teachers)

        list_subjects = []
        for i in range(1, NUMBER_SUBJECTS + 1):
            n_subject = Subjects(
                subject_name=choice(fake_subjects),
                teacher=choice(list_teachers)
            )
            list_subjects.append(n_subject)
        session.add_all(list_subjects)

        list_grades = []
        for i in range(1, NUMBER_GRADES * NUMBER_STUDENTS + 1):
            n_grade = Grades(
                score=randint(50, 100),
                score_date=faker.date_between(start_date="-1y", end_date="today"),
                student=choice(list_students),
                subject=choice(list_subjects)
            )
            list_grades.append(n_grade)
        session.add_all(list_grades)

        session.commit()

    except Exception as e:
        print(e)
    finally:
        session.close()


if __name__ == '__main__':
    db_populate()
