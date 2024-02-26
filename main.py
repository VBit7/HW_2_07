import argparse
from sqlalchemy import select, func, desc, and_
from tabulate import tabulate

from connect_db import session
from models import Base, Groups, Students, Teachers, Subjects, Grades


table_dict = {
    'Groups': Groups,
    'Teachers': Teachers,
    'Subjects': Subjects,
    'Students': Students,
    'Grades': Grades,
}


def create_model(args):
    match args.model:
        case 'Teachers':
            n_field = Teachers(full_name=args.name)
        case 'Groups':
            n_field = Groups(group_name=args.name)
        case _:
            print(f"The functionality for table {args.model} is not implemented")
    try:
        session.add(n_field)
        session.commit()
        print(f"Creating {args.model} with name '{args.name}'")
    except NotImplementedError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()


def list_model(args):
    print(f"Listing all {args.model}")
    try:
        model_name = table_dict[args.model]
        statement = select(model_name)
        result = session.execute(statement).scalars()
        for row in result:
            values = list(row.__dict__.items())[1:]
            row_string = ", ".join([f"{key}: {value}" for key, value in values])
            print(row_string)
    except NotImplementedError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()


def update_model(args):
    try:
        match args.model:
            case 'Teachers':
                teacher = session.query(Teachers).filter_by(id=args.id).first()
                if teacher:
                    teacher.full_name = args.name
                    session.commit()
                    print(f"Update {args.model} with ID {args.id}: full_name='{args.name}'")
                else:
                    print(f"No {args.model} found with ID {args.id}")
            case 'Groups':
                group = session.query(Groups).filter_by(id=args.id).first()
                if group:
                    group.group_name = args.name
                    session.commit()
                    print(f"Update {args.model} with ID {args.id}: group_name='{args.name}'")
                else:
                    print(f"No {args.model} found with ID {args.id}")
            case _:
                raise NotImplementedError(f"The functionality for updating table {args.model} is not implemented")
    except NotImplementedError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def remove_model(args):
    try:
        match args.model:
            case 'Teachers':
                teacher = session.query(Teachers).filter_by(id=args.id).first()
                if teacher:
                    session.delete(teacher)
                    session.commit()
                    print(f"Removed {args.model} with ID {args.id}")
                else:
                    print(f"No {args.model} found with ID {args.id}")
            case 'Groups':
                group = session.query(Groups).filter_by(id=args.id).first()
                if group:
                    session.delete(group)
                    session.commit()
                    print(f"Removed {args.model} with ID {args.id}")
                else:
                    print(f"No {args.model} found with ID {args.id}")
            case 'Subjects':
                subject = session.query(Groups).filter_by(id=args.id).first()
                if subject:
                    session.delete(subject)
                    session.commit()
                    print(f"Removed {args.model} with ID {args.id}")
                else:
                    print(f"No {args.model} found with ID {args.id}")
            case 'Students':
                student = session.query(Groups).filter_by(id=args.id).first()
                if student:
                    session.delete(student)
                    session.commit()
                    print(f"Removed {args.model} with ID {args.id}")
                else:
                    print(f"No {args.model} found with ID {args.id}")
            case 'Grades':
                grade = session.query(Groups).filter_by(id=args.id).first()
                if grade:
                    session.delete(grade)
                    session.commit()
                    print(f"Removed {args.model} with ID {args.id}")
                else:
                    print(f"No {args.model} found with ID {args.id}")
    except NotImplementedError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

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

    --action create -m Teachers --name 'Boris Jonson'            # створення вчителя
    --action list -m Teachers                                    # показати всіх вчителів
    --action update -m Teachers --id 3 --name 'Andry Bezos'      # оновити дані вчителя з id=3
    --action remove -m Teachers --id 3                           # видалити вчителя з id=3
    """

    main()
