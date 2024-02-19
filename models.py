from datetime import date

from sqlalchemy import create_engine, String, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column, relationship
from config import DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME

DATABASE_URL = rf'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'

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


class Teachers(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)


class Subjects(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_name: Mapped[str] = mapped_column(String(50), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id'))
    teacher: Mapped['Teachers'] = relationship('Teachers')


class Grades(Base):
    __tablename__ = 'grades'
    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[int] = mapped_column()
    score_date: Mapped[date] = mapped_column(Date)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'))
    subject_id: Mapped[int] = mapped_column(ForeignKey('subjects.id'))
    student: Mapped['Students'] = relationship('Students')
    subject: Mapped['Subjects'] = relationship('Subjects')
