from sqlalchemy import select, func, desc
from sqlalchemy.orm import join

from connect_db import session
from models import Groups, Students, Teachers, Subjects, Grades

def select_1():
    """
    1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів

    select  full_name, round(avg(Score), 2) as avg_score
    from students s
        join Grades g on s.id = g.student_id
    group by full_name
    order by avg(Score) DESC
    limit 5;
    """

    statement = select(Students.full_name, func.round(func.avg(Grades.score), 2).label('avg_score'))\
        .join(Grades)\
        .group_by(Students.full_name)\
        .order_by(desc(func.avg(Grades.score)))\
        .limit(5)
    print(statement)
    columns = ['full_name', 'avg_score']
    # result = [dict(zip(columns, (row.full_name, row.avg_score))) for row in session.execute(statement).scalars()]
    # result = [dict(zip(columns, (row.full_name, row[0]))) for row in session.execute(statement).scalars()]
    result = session.execute(statement).mappings()
    # result = session.execute(statement).scalars()
    for row in result:
        print(row)
    # print(result)


def select_2(subject_id):
    """
    2. Знайти студента із найвищим середнім балом з певного предмета

    select full_name, s2.subject_name, avg(score)
    from students s
        join grades g ON s.id = g.student_id
        join subjects s2 ON g.subject_id = s2.id
    where s2.id = 1
    group by s2.subject_name, s.full_name
    order by avg(g.score) desc
    limit 1;
    """
    statement = select(
            Students.full_name,
            Subjects.subject_name,
            func.round(func.avg(Grades.score), 2).label('avg_score')
        )\
        .join(Grades)\
        .group_by(Students.full_name, Subjects.subject_name)\
        .order_by(desc(func.avg(Grades.score)))\
        .limit(1)
    print(statement)
    result = session.execute(statement).mappings()
    for row in result:
        print(row)


def select_3():
    """
    3. Знайти середній бал у групах з певного предмета
    """
    pass


def select_4():
    """
    4. Знайти середній бал на потоці (по всій таблиці оцінок)
    """
    pass


def select_5():
    """
    5. Знайти які курси читає певний викладач
    """
    pass


def select_6():
    """
    6. Знайти список студентів у певній групі
    """
    pass


def select_7():
    """
    7. Знайти оцінки студентів у окремій групі з певного предмета
    """
    pass



def select_8():
    """
    8. Знайти середній бал, який ставить певний викладач зі своїх предметів
    """
    pass


def select_9():
    """
    9. Знайти список курсів, які відвідує певний студент
    """
    pass


def select_10():
    """
    10. Список курсів, які певному студенту читає певний викладач
    """
    pass


def select_11():
    """
    11. Середній бал, який певний викладач ставить певному студентові
    """
    pass


def select_12():
    """
    12. Оцінки студентів у певній групі з певного предмета на останньому занятті
    """
    pass


if __name__ == '__main__':
    # select_1()
    select_2(1)