import argparse
from sqlalchemy import select, func, desc, and_
from tabulate import tabulate

from connect_db import session
from models import Base, Groups, Students, Teachers, Subjects, Grades


def create_model(args):
    print(f"Creating {args.model} with name '{args.name}'")


def list_model(args):
    print(f"Listing all {args.model}")
    # statement = select(args.model)
    # print(statement)
    # result = session.execute(statement).mappings()
    # # headers = ["Student's Name", "AVG Score"]
    # # print_result(title, headers, result)
    # print(tabulate(result))

    # Отримуємо клас моделі за назвою, переданою через args
    table_name = args.model
    print(table_name)
    ModelClass = globals()[table_name]

    # Створюємо запит з використанням класу моделі
    statement = select(ModelClass)
    # statement = select(table_name)
    # print(statement)
    # Виконуємо запит та отримуємо результат
    # result = session.execute(statement) #.mappings()
    result = session.query(ModelClass).all()
    print(tabulate(result))
    # # Виводимо дані
    # for row in result:
    #     print(row.__dict__)


def update_model(args):
    print(f"Updating {args.model} with id={args.id} to name '{args.name}'")


def remove_model(args):
    print(f"Removing {args.model} with id={args.id}")


def main():
    parser = argparse.ArgumentParser(description="CRUD operations with models")
    parser.add_argument('--action', '-a', required=True, choices=['create', 'list', 'update', 'remove'],
                        help='CRUD operation')
    parser.add_argument('--model', '-m', required=True, help='Model name')
    parser.add_argument('--id', type=int, help='ID of the model')
    parser.add_argument('--name', help='Name of the model')

    args = parser.parse_args()

    action_functions = {
        'create': create_model,
        'list': list_model,
        'update': update_model,
        'remove': remove_model
    }

    action_functions[args.action](args)


if __name__ == "__main__":
    """
    Приклад:

    --action create -m Teacher --name 'Boris Jonson'            # створення вчителя
    --action list -m Teacher                                    # показати всіх вчителів
    --action update -m Teacher --id 3 --name 'Andry Bezos'      # оновити дані вчителя з id=3
    --action remove -m Teacher --id 3                           # видалити вчителя з id=3
    """

    main()
