from orm_base import Base
from sqlalchemy import Table
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import String, Integer
from sqlalchemy.types import Time
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, CheckConstraint
from IntrospectionFactory import IntrospectionFactory
from Department import Department
from Course import Course
from typing import List
from constants import START_OVER, REUSE_NO_INTROSPECTION, INTROSPECT_TABLES

introspection_type = IntrospectionFactory().introspection_type
if introspection_type == START_OVER or REUSE_NO_INTROSPECTION:

    class Section(Base):
        """A group of students that meet for instruction at a particular day and time, while still
        teaching the same subject. For example, Section 1 of CECS 323 meets on Mondays and Wednesdays
         at 3:30 whereas Section 2 meets at 12 noon."""
        __tablename__ = "sections"

        departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', String(10), primary_key=True)
        courseNumber: Mapped[int] = mapped_column('course_number', Integer, primary_key=True)
        sectionNumber: Mapped[int] = mapped_column('section_number', Integer, primary_key=True)
        semester: Mapped[str] = mapped_column('semester', String(10), CheckConstraint("semester IN('Fall','Spring','Winter','Summer I','Summer II')",
                                                                                      name="semester_values_check"), nullable=False, primary_key=True)  # cuz mandatory
        sectionYear: Mapped[int] = mapped_column('section_year', Integer, nullable=False,
                                                  primary_key=True)
        schedule: Mapped[str] = mapped_column('schedule', String(6),
                                              CheckConstraint("schedule IN('MW','TuTh','MWF','F','S')",
                                                              name="schedule_values_check"), nullable=False)

        room: Mapped[int] = mapped_column('room', Integer, nullable=False)
        building: Mapped[str] = mapped_column('building', String(6),
                                              CheckConstraint("building IN('VEC', 'ECS', 'EN2', 'EN3', 'EN4', 'ET', 'SSPA')",
                                                              name="building_values_check"), nullable=False)
        startTime: Mapped[Time] = mapped_column('start_time', Time, nullable=False)
        instructor: Mapped[str] = mapped_column('instructor', String(80), nullable=False)

        course: Mapped["Course"] = relationship(back_populates="sections")

        __table_args__ = (UniqueConstraint("section_year", "semester", "schedule", "start_time",
                                           "building", "room", name="sections_uk_01"),
                          UniqueConstraint("section_year", "semester", "schedule", "start_time",
                                           "instructor", name="sections_uk_02"),
                          ForeignKeyConstraint([departmentAbbreviation, courseNumber],
                                               [Course.departmentAbbreviation, Course.courseNumber]))

        def __init__(self, course: Course, sectionNumber: int,
                     semester: str, sectionYear: int, building: str, room: int, schedule: str,
                     startTime: Time, instructor: str):
            # not sure how to use compound primary keys/relationship
            #self.departmentAbbreviation = department_abbreviation
            #self.courseNumber = course_number
            self.set_course(course)
            self.sectionNumber = sectionNumber
            self.semester = semester
            self.sectionYear = sectionYear
            self.building = building
            self.room = room
            self.schedule = schedule
            self.startTime = startTime
            self.instructor = instructor

elif introspection_type == INTROSPECT_TABLES:
    class Section(Base):
        __table__ = Table("sections", Base.metadata, autoload_with=engine)
        departmentAbbreviation: Mapped[str] = column_property(__table__.c.department_abbreviation)
        courseNumber: Mapped[str] = column_property(__table__.c.course_number)
        sectionNumber: Mapped[str] = column_property(__table__.c.section_number)

        sectionYear: Mapped[str] = column_property(__table__.c.section_year)

        startTime: Mapped[str] = column_property(__table__.c.start_time)



        def __init__(self, course: Course, sectionNumber: int, semester: str, sectionYear: int, building: str,
                     room: int, schedule: str, startTime: Time, instructor: str):
            # not sure how to use compound primary keys/relationship
            #self.departmentAbbreviation = department_abbreviation
            #self.courseNumber = course_number
            self.set_course(course)
            self.sectionNumber = sectionNumber
            self.semester = semester
            self.sectionYear = sectionYear
            self.building = building
            self.room = room
            self.schedule = schedule
            self.startTime = startTime
            self.instructor = instructor

#indenting might help initialize the selfs
def set_course(self, course: Course):
    self.course = course
    self.departmentAbbreviation = course.departmentAbbreviation
    self.courseNumber = course.courseNumber
def __str__(self):
    return f"Department Abbreviation: {self.departmentAbbreviation}\nCourse Number: {self.courseNumber}\n" \
           f"Section Number: {self.sectionNumber}\nSemester: {self.semester}\nSection Year: {self.sectionYear}\n" \
           f"Building: {self.building}\nRoom: {self.room}\nSchedule: {self.schedule}\nStart Time: {self.startTime}\n" \
           f"Instructor: {self.instructor}"




setattr(Section, 'set_course', set_course)
setattr(Section, '__str__', __str__)
