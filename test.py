from sqlalchemy import select, func, desc, and_
from tabulate import tabulate

from connect_db import session
from models import Groups, Students, Teachers, Subjects, Grades

table_dict = {
    'Groups': Groups,
}


def read_record(table_name, **kwargs):
    # model = globals()['Groups']

    # records = session.query(model).all()
    # for record in records:
    #     print(record)

    table_name = table_dict('Groups')
    statement = select(table_name)
    result = session.execute(statement).scalars()
    #     # mappings()
    #
    for row in result:
        print(list(row.__dict__.values())[1:])
        # print(row.__dict__)
        # print(keys_except_first)

    # # Динамічно отримуємо клас моделі за його ім'ям
    # table_class = globals().get(table_name)
    # print(table_class)
    #
    # if table_class:
    #     # Читання записів з таблиці за вказаними параметрами
    #     records = session.query(table_class).filter_by(**kwargs).all()
    #     if records:
    #         for record in records:
    #             print(record.__dict__)
    #     else:
    #         print("Записів з такими параметрами не знайдено.")
    # else:
    #     print("Таблицю з таким ім'ям не знайдено.")


if __name__ == '__main__':
    read_record('groups', id=1)
    # table_name = 'groups'
    # ModelClass = globals().get(table_name)
    # print(ModelClass)