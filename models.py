from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column, relationship
from config import DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME

DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'

engine = create_engine(DATABASE_URL)
session = sessionmaker(bind=engine)

Base = declarative_base()


class Groups(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str] = mapped_column(String(50))


class Students(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    group: Mapped['Groups'] = relationship('Groups')
