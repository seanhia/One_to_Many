from orm_base import Base
from sqlalchemy import Table
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import String, Integer, Time
from sqlalchemy import UniqueConstraint, ForeignKey, ForeignKeyConstraint
from Course import Course
from typing import List
from constants import START_OVER, REUSE_NO_INTROSPECTION, INTROSPECT_TABLES

introspection_type == IntrospectionFactory().introspection_type
if introspection_type == START_OVER or REUSE_NO_INTROSPECTION:

    class Section(Base):
        """A group of students that meet for instruction at a particular day and time, while still
        teaching the same subject. For example, Section 1 of CECS 323 meets on Mondays and Wednesdays
         at 3:30 whereas Section 2 meets at 12 noon."""
        __tablename__ = "sections"

        department_abbreviation: Mapped[str] = mapped_column('department_abbreviation', String(10),
                                                             primary_key=True)
        course_number: Mapped[int] = mapped_column('course_number', Integer, primary_key=True)
        section_number: Mapped[int] = mapped_column('section_number', Integer, primary_key=True)
        semester: Mapped[str] = mapped_column('semester', String(10), nullable=False, primary_key=True)  # cuz mandatory
        section_year: Mapped[int] = mapped_column('section_year', Integer, nullable=False,
                                                  primary_key=True)
        building: Mapped[str] = mapped_column('building', String(6), nullable=False)
        room: Mapped[int] = mapped_column('room', Integer, nullable=False)
        schedule: Mapped[str] = mapped_column('schedule', String(6), nullable=False)
        start_time: Mapped[Time] = mapped_column('start_time', Time, nullable=False)
        instructor: Mapped[str] = mapped_column('instructor', String(80), nullable=False)

        courses: Mapped[List["Course"]] = relationship(back_populates="sections")

        __table_args__ = (UniqueConstraint("section_year", "semester", "schedule", "start_time",
                                           "building", "room", name="sections_uk_01"),
                          UniqueConstraint("section_year", "semester", "schedule", "start_time",
                                           "instructor", name="sections_uk_02"),
                          ForeignKeyConstraint([department_abbreviation, course_number],
                                               [Course.department_abbreviation, Course.course_number]))

    def __init__(self, department_abbreviation: str, course_number: int, section_number: int,
                 semester: str, section_year: int, building: str, room: int, schedule: str,
                 start_time: Time, instructor: int, courses: Course):
        # not sure how to use compound primary keys/relationship
        self.department_abbreviation = department_abbreviation
        self.course_number = course_number
        self.section_number = section_number
        self.semester = semester
        self.section_year = section_year
        self.building = building
        self.room = room
        self.schedule = schedule
        self.start_time = start_time
        self.instructor = instructor
        self.set_course(courses)

elif introspection_type == INTROSPECT_TABLES:


    def __str__(self):
        return f"Department Abbreviation: {self.department_abbreviation}\nCourse Number: {self.course_number}\nSection Number: {self.section_number}\nSemester: {self.semester}\nSection Year: {self.section_year}\nBuilding: {self.building}\nRoom: {self.room}\nSchedule: {self.schedule}\nStart Time: {self.start_time}\nInstructor: {self.instructor}"
