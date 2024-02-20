from sqlalchemy import Integer, String, ForeignKey, create_engine, select, and_, or_, not_, desc, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, Mapped, mapped_column

engine = create_engine("sqlite:///:memory:", echo=False)
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(120))


class Address(Base):
    __tablename__ = 'addresses'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user_fk: Mapped["User"] = relationship("User")


Base.metadata.create_all(engine)

if __name__ == '__main__':
    n_user = User(fullname='Jack Jones')
    session.add(n_user)
    n_address = Address(email='jones@mail.com', user_fk=n_user)
    session.add(n_address)
    n_address = Address(email='jones_next@mail.com', user_fk=n_user)
    session.add(n_address)
    session.commit()

    n_user = User(fullname='Vasya Pupkin')
    session.add(n_user)
    n_address = Address(email='pupkin@mail.com', user_fk=n_user)
    session.add(n_address)
    n_address = Address(email='pupkin2@mail.com', user_fk=n_user)
    session.add(n_address)
    n_address = Address(email='pupkin3@mail.com', user_fk=n_user)
    session.add(n_address)
    session.commit()

    n_user = User(fullname='Vasya Horse')
    session.add(n_user)
    n_address = Address(email='horse@mail.com', user_fk=n_user)
    session.add(n_address)
    session.commit()

    statement = select(User.id, User.fullname)
    # print(statement)      # Виводить SQL-запит
    for row in session.execute(statement):
        print(row)

    statement = select(Address.id, Address.email, User.fullname).join(Address.user_fk)
    # print(statement)
    for row in session.execute(statement):
        print(row)

    statement = select(User)
    columns = ["id", "fullname"]
    # З використанням scalars()
    result = [dict(zip(columns, (row.id, row.fullname))) for row in session.execute(statement).scalars()]
    print(result)
    # Те саме, тільки без scalars()
    result = [dict(zip(columns, (row.User.id, row.User.fullname))) for row in session.execute(statement)]
    print(result)

    # where
    print("   ***   WHERE example:   ***")
    statement = select(User).where(User.fullname == "Jack Jones")
    result = [dict(zip(columns, (row.User.id, row.User.fullname))) for row in session.execute(statement)]
    print(result)
    # Для однієї строки:
    r = session.execute(statement).scalar_one_or_none()
    if r:
        print(r.id, r.fullname)

    print("   ***   LIKE example:   ***")
    statement = select(User).where(User.fullname.like("Vasya%"))
    # columns = ["id", "fullname"]
    # result = [dict(zip(columns, (row.User.id, row.User.fullname))) for row in session.execute(statement)]
    # print(result)
    r = session.execute(statement).scalars()
    for row in r:
        print(row.id, row.fullname)

    print("   ***   LIKE, WHERE AND example:   ***")
    statement = select(User).where(User.fullname.like("Vasya%")).where(User.id == 3)
    r = session.execute(statement).scalars()
    for row in r:
        print(row.id, row.fullname)

    print("   ***   LIKE, WHERE AND example (variant 2):   ***")
    statement = select(User).where(and_(User.fullname.like("Vasya%"), User.id == 3))
    r = session.execute(statement).scalars()
    for row in r:
        print(row.id, row.fullname)

    print("   ***   LIKE, WHERE OR example:   ***")
    statement = select(User).where(or_(User.fullname.like("Vasya%"), User.id == 3))
    r = session.execute(statement).scalars()
    for row in r:
        print(row.id, row.fullname)

    print("   ***   ORDER BY:   ***")
    # statement = select(User).order_by(User.fullname)              # ASC
    statement = select(User).order_by(desc(User.fullname))          # DESC
    columns = ["id", "fullname"]
    result = [dict(zip(columns, (row.User.id, row.User.fullname))) for row in session.execute(statement)]
    print(result)

    print("   ***   AVG:   ***")
    statement = (
        select(User.fullname, func.count(Address.id))
        .join(Address)
        .group_by(User.fullname)
        .order_by(desc(func.count(Address.id)))
    )
    result = session.execute(statement).all()
    for fullname, count in result:
        print(f"USER {fullname} have {count} email(s)")

    print("   ***   AVG (mappings):   ***")
    statement = (
        select(User.fullname, func.count(Address.id))
        .join(Address)
        .group_by(User.fullname)
        .order_by(desc(func.count(Address.id)))
    )
    result = session.execute(statement).mappings()
    for row in result:
        print(row)


    session.close()
