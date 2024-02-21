from sqlalchemy import select, func, desc, and_
# from sqlalchemy.orm import join
from tabulate import tabulate

from connect_db import session
from models import Groups, Students, Teachers, Subjects, Grades


def print_result(title, headers, result):
    print(f'{title}:')
    if result:
        data = [list(row.values()) for row in result]
        print(tabulate(data, headers=headers, tablefmt='fancy_grid'))
    else:
        print('No results for query...')
    print("-" * 50)


def select_1():
    title = """1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів"""

    statement = select(
        Students.full_name,
        func.round(func.avg(Grades.score), 2)
    ).join(
        Grades
    ).group_by(
        Students.full_name
    ).order_by(
        desc(func.avg(Grades.score))
    ).limit(5)

    result = session.execute(statement).mappings()
    headers = ["Student's Name", "AVG Score"]
    print_result(title, headers, result)


def select_2(subject_id):
    title = """2. Знайти студента із найвищим середнім балом з певного предмета"""

    statement = select(
        Students.full_name,
        Subjects.subject_name,
        func.round(func.avg(Grades.score), 2)
    ).join(
        Grades, Students.id == Grades.student_id
    ).join(
        Subjects, Grades.subject_id == Subjects.id
    ).where(
        Subjects.id == subject_id
    ).group_by(
        Students.full_name,
        Subjects.subject_name
    ).order_by(
        desc(func.avg(Grades.score))
    ).limit(1)

    result = session.execute(statement).mappings()
    headers = ["Student's Name", "Subject", "AVG Score"]
    print_result(title, headers, result)


def select_3(subject_id):
    title = """3. Знайти середній бал у групах з певного предмета"""

    statement = select(
        Groups.group_name,
        Subjects.subject_name,
        func.round(func.avg(Grades.score), 2)
    ).join(
        Students, Groups.id == Students.group_id
    ).join(
        Grades, Students.id == Grades.student_id
    ).join(
        Subjects, Grades.subject_id == Subjects.id
    ).where(
        Subjects.id == subject_id
    ).group_by(
        Groups.group_name,
        Subjects.subject_name
    ).order_by(
        Groups.group_name
    )

    result = session.execute(statement).mappings()
    headers = ["Group", "Subject", "AVG Score"]
    print_result(title, headers, result)


def select_4():
    title = """4. Знайти середній бал на потоці (по всій таблиці оцінок)"""

    statement = select(
        func.round(
            func.avg(Grades.score), 2)
    )

    result = session.execute(statement).mappings()
    headers = ["AVG Score"]
    print_result(title, headers, result)


def select_5(teacher_id):
    title = """5. Знайти які курси читає певний викладач"""

    statement = select(
        Teachers.full_name,
        Subjects.subject_name
    ).join(
        Subjects, Teachers.id == Subjects.teacher_id
    ).where(
        Teachers.id == teacher_id
    ).order_by(
        Subjects.subject_name
    )

    result = session.execute(statement).mappings()
    headers = ["Teacher's Name", "Subject"]
    print_result(title, headers, result)


def select_6(ext_group_id):
    title = """6. Знайти список студентів у певній групі"""
    statement = select(
        Students.full_name,
        Groups.group_name
    ).join(
        Groups
    ).where(
        Groups.id == ext_group_id
    ).order_by(
        Students.full_name
    )

    result = session.execute(statement).mappings()
    headers = ["Student's Name", "Group"]
    print_result(title, headers, result)


def select_7(ext_group_id, ext_subject_id):
    title = """7. Знайти оцінки студентів у окремій групі з певного предмета"""

    statement = select(
        Students.full_name,
        Groups.group_name,
        Subjects.subject_name,
        Grades.score,
        Grades.score_date
    ).join(
        Groups, Groups.id == Students.group_id
    ).join(
        Grades, Students.id == Grades.student_id
    ).join(
        Subjects, Grades.subject_id == Subjects.id
    ).where(
        and_(
            Groups.id == ext_group_id,
            Subjects.id == ext_subject_id)
    ).order_by(
        Students.full_name
    ).limit(10)

    result = session.execute(statement).mappings()
    headers = ["Student's Name", "Group", "Subject", "Score", "Date of Score"]
    print_result(title, headers, result)


def select_8(ext_teacher_id):
    title = """8. Знайти середній бал, який ставить певний викладач зі своїх предметів"""

    statement = select(
        Teachers.full_name,
        Subjects.subject_name,
        func.round(func.avg(Grades.score), 2)
    ).join(
        Subjects, Teachers.id == Subjects.teacher_id
    ).join(
        Grades, Subjects.id == Grades.subject_id
    ).where(
        and_(
            Teachers.id == ext_teacher_id
        )
    ).group_by(
        Teachers.full_name, Subjects.subject_name
    ).order_by(
        Subjects.subject_name
    )

    result = session.execute(statement).mappings()
    headers = ["Teacher's Name", "Subject", "AVG Score"]
    print_result(title, headers, result)


def select_9(ext_student_id):
    title = """9. Знайти список курсів, які відвідує певний студент"""

    statement = select(
        Students.full_name,
        Subjects.subject_name
    ).join(
        Grades, Students.id == Grades.student_id
    ).join(
        Subjects, Grades.subject_id == Subjects.id
    ).where(
        Students.id == ext_student_id
    ).group_by(
        Students.full_name, Subjects.subject_name
    ).order_by(
        Subjects.subject_name
    )

    result = session.execute(statement).mappings()
    headers = ["Student's Name", "Subject"]
    print_result(title, headers, result)


def select_10(ext_student_id, ext_teacher_id):
    title = """10. Список курсів, які певному студенту читає певний викладач"""

    statement = select(
        Students.full_name,
        Subjects.subject_name,
        Teachers.full_name
    ).join(
        Grades, Students.id == Grades.student_id
    ).join(
        Subjects, Grades.subject_id == Subjects.id
    ).join(
        Teachers, Subjects.teacher_id == Teachers.id
    ).where(
        and_(
            Students.id == ext_student_id, Teachers.id == ext_teacher_id
        )
    ).group_by(
        Students.full_name,
        Subjects.subject_name,
        Teachers.full_name
    ).order_by(
        Subjects.subject_name
    )

    result = session.execute(statement).mappings()
    headers = ["Student's Name", "Subject", "Teacher's Name"]
    print_result(title, headers, result)


def select_11(ext_student_id, ext_teacher_id):
    title = """11. Середній бал, який певний викладач ставить певному студентові"""

    statement = select(
        Teachers.full_name,
        Students.full_name,
        func.round(func.avg(Grades.score), 2)
    ).join(
        Subjects, Teachers.id == Subjects.teacher_id
    ).join(
        Grades, Grades.subject_id == Subjects.id
    ).join(
        Students, Grades.student_id == Students.id
    ).where(
        and_(
            Students.id == ext_student_id,
            Teachers.id == ext_teacher_id)
    ).group_by(
        Teachers.full_name,
        Students.full_name
    )

    result = session.execute(statement).mappings()
    headers = ["Teacher's Name", "Student's Name", "Subject"]
    print_result(title, headers, result)


def select_12(ext_group_id, ext_subject_id):
    title = """12. Оцінки студентів у певній групі з певного предмета на останньому занятті"""

    max_score_date_subquery = select(
        func.max(Grades.score_date)
    ).join(
        Students
    ).where(
        and_(
            Students.group_id == ext_group_id,
            Grades.subject_id == ext_subject_id
        )
    ).scalar_subquery()

    statement = select(
        Students.full_name,
        Groups.group_name,
        Subjects.subject_name,
        Grades.score,
        Grades.score_date
    ).join(
        Groups, Students.group_id == Groups.id
    ).join(
        Grades, Students.id == Grades.student_id
    ).join(
        Subjects, Grades.subject_id == Subjects.id
    ).where(
        and_(
            Groups.id == ext_group_id,
            Subjects.id == ext_subject_id,
            Grades.score_date == max_score_date_subquery
        )
    )
    result = session.execute(statement).mappings()
    headers = ["Student's Name", "Group", "Subject", "Score", "Date of Score"]
    print_result(title, headers, result)


if __name__ == '__main__':
    select_1()
    select_2(1)
    select_3(1)
    select_4()
    select_5(3)
    select_6(1)
    select_7(1, 1)
    select_8(3)
    select_9(1)
    select_10(1, 3)
    select_11(1, 3)
    select_12(1, 1)
