import logging
# My option lists for
from menu_definitions import menu_main, debug_select
from IntrospectionFactory import IntrospectionFactory
from db_connection import engine, Session
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Student, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Department import Department
from Course import Course
from Section import Section
from Option import Option
from Menu import Menu
import time
# Poor man's enumeration of the two available modes for creating the tables
from constants import START_OVER, INTROSPECT_TABLES, REUSE_NO_INTROSPECTION
import IPython  # So that I can exit out to the console without leaving the application.
from sqlalchemy import inspect  # map from column name to attribute name
from pprint import pprint



def add_department(session):
    """
    Prompt the user for the information for a new department and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_abbreviation: bool = False
    name: str = ''
    abbreviation: str = ''
    while not unique_abbreviation or not unique_name:
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        name_count: int = session.query(Department).filter(Department.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a department by that name.  Try again.")
        if unique_name:
            abbreviation_count = session.query(Department). \
                filter(Department.abbreviation == abbreviation).count()
            unique_abbreviation = abbreviation_count == 0
            if not unique_abbreviation:
                print("We already have a department with that abbreviation.  Try again.")
    new_department = Department(abbreviation, name)
    session.add(new_department)


def add_course(session):
    """
    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this course?")
    department: Department = select_department(sess)
    unique_number: bool = False
    unique_name: bool = False
    number: int = -1
    name: str = ''
    while not unique_number or not unique_name:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))
        name_count: int = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation,
                                                       Course.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            number_count = session.query(Course). \
                filter(Course.departmentAbbreviation == department.abbreviation,
                       Course.courseNumber == number).count()
            unique_number = number_count == 0
            if not unique_number:
                print("We already have a course in this department with that number.  Try again.")
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))
    course = Course(department, number, name, description, units)
    session.add(course)


def add_section(session):
    unique_year: bool = False
    unique_semester: bool = False
    unique_schedule: bool = False
    unique_start_time: bool = False
    unique_building: bool = False
    unique_room: bool = False
    unique_instructor: bool = False

    year: int = ''
    semester: str = ''
    schedule: str = ''
    start_time: time = ''
    building: str = ''
    room: int = ''
    instructor: str = ''

    while not unique_year or not unique_semester or not unique_schedule or not unique_start_time or not unique_room or not unique_building or not unique_instructor:
        year = int(input("Section Year--> "))
        semester = input("Section semester--> ")
        schedule = input("Schedule--> ")
        start_time = time(input("Start time--> "))
        building = input("Section building--> ")
        room = int(input("Section room--> "))
        instructor = input("Section instructor--> ")

        year_count: int = session.query(Section).filter(Section.section_year == year).count()
        unique_year = year_count == 0
        if not unique_year:
            print("We already have a section with that year. Try again")
            if unique_year:
                semester_count = session.query(Section).filter(Section.semester == semester).count()
                unique_semester = semester_count == 0
                if not unique_semester:
                    print("We already have a section in that semester. Try again")
                    if unique_semester:
                        schedule_count = session.query(Section).filter(Section.schedule == schedule).count()
                        unique_schedule = schedule_count == 0
                        if not unique_schedule:
                            print("We already have a section with that schedule. Try again")
                            if unique_schedule:
                                start_time_count = session.query(Section).filter(Section.startTime == start_time).count()
                                unique_start_time = start_time_count == 0
                                if not unique_start_time:
                                    print("We already have a section with that start time. Try again")
                                    if unique_start_time:
                                        building_count = session.query(Section).filter(Section.building == building).count()
                                        unique_building = building_count == 0
                                        if not unique_building:
                                            print("We already have a section in that building. Try again")
                                            if unique_building:
                                                room_count = session.query(Section).filter(
                                                    Section.room == room).count()
                                                unique_room = room_count == 0
                                                if not unique_room:
                                                    print("We already have a section in that room. Try again")
                                                    if unique_room:
                                                        instructor_count = session.query(Section).filter(
                                                            Section.instructor == instructor).count()
                                                        unique_instructor = instructor_count == 0
        newSection = Section(year, semester, schedule, start_time, building, room, instructor)
        session.add(newSection)



def select_department(sess) -> Department:
    """
    Prompt the user for a specific department by the department abbreviation.
    :param sess:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Enter the department abbreviation--> ")
        abbreviation_count: int = sess.query(Department). \
            filter(Department.abbreviation == abbreviation).count()
        found = abbreviation_count == 1
        if not found:
            print("No department with that abbreviation.  Try again.")
    return_student: Department = sess.query(Department). \
        filter(Department.abbreviation == abbreviation).first()
    return return_student


def select_course(sess) -> Course:
    """
    Select a course by the combination of the department abbreviation and course number.
    Note, a similar query would be to select the course on the basis of the department
    abbreviation and the course name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = -1
    while not found:
        department_abbreviation = input("Department abbreviation--> ")
        course_number = int(input("Course Number--> "))
        name_count: int = sess.query(Course).filter(Course.departmentAbbreviation == department_abbreviation,
                                                    Course.courseNumber == course_number).count()
        found = name_count == 1
        if not found:
            print("No course by that number in that department.  Try again.")
    course = sess.query(Course).filter(Course.departmentAbbreviation == department_abbreviation,
                                       Course.courseNumber == course_number).first()
    return course

def select_section(sess) -> Section: #still need to work on this one
    #prompt the user for a course
    #go to the list of sections within that course object and display the sections
    found: bool = False

def delete_course(session):
    #be sure to tell the user if they attempt to delete a course that does not exist
    #use the select a course utility that is in the sample code to allow the user to select the course easily
    #if the course that the user identifies for deletion is the parent to one or more sections, stop them before you have an exception thrown by the database
    print("deleting a course")
    course = select_course(session)
    has_section = session.query(Course).filter_by(Course.departmentAbbreviation).first() #check if there are any sections in course
    if has_section:
        print("This course is a parent to one or more sections. Delete them first, then come back here to delete the course.")
    else:
        session.delete(course)



def delete_section(session):
    #be sure to tell the user if they attempt to delete a section that does not exist
    #you can do this either by performing a select in the database and presenting the user a menu of sections to delete
    #or prompt them for the information to identify the section (using the columns in one of the uniqueness constraints)
    print("deleting a section")
    section = select_section(session)
    n_courses = session.query(Section).filter(Section.departmentAbbreviation == section.abbreviation).count() #this line could change depending on how we do select_section
    if n_courses > 0:
        print(f"Sorry, there are {n_courses} courses in that section.  Delete them first, "
              "then come back here to delete the section.")
    else:
        session.delete(section)
def delete_department(session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a department")
    department = select_department(session)
    n_courses = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation).count()
    if n_courses > 0:
        print(f"Sorry, there are {n_courses} courses in that department.  Delete them first, "
              "then come back here to delete the department.")
    else:
        session.delete(department)

def list_section(session): #still needs work
    pass
    #list section in course
    #prompt user to select a course
    #go to the list of sections within that course object and display the sections


def list_departments(session):
    """
    List all departments, sorted by the abbreviation.
    :param session:     The connection to the database.
    :return:            None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    departments: [Department] = list(session.query(Department).order_by(Department.abbreviation))
    for department in departments:
        print(department)


def list_courses(sess):
    """
    List all courses currently in the database.
    :param sess:    The connection to the database.
    :return:        None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    courses: [Course] = sess.query(Course).order_by(Course.courseNumber)
    for course in courses:
        print(course)


def move_course_to_new_department(sess):
    """
    Take an existing course and move it to an existing department.  The course has to
    have a department when the course is created, so this routine just moves it from
    one department to another.

    The change in department has to occur from the Course end of the association because
    the association is mandatory.  We cannot have the course not have any department for
    any time the way that we would if we moved it to a new department from the department
    end.

    Also, the change in department requires that we make sure that the course will not
    conflict with any existing courses in the new department by name or number.
    :param sess:    The connection to the database.
    :return:        None
    """
    print("Input the course to move to a new department.")
    course = select_course(sess)
    old_department = course.department
    print("Input the department to move that course to.")
    new_department = select_department(sess)
    if new_department == old_department:
        print("Error, you're not moving to a different department.")
    else:
        # check to be sure that we are not violating the {departmentAbbreviation, name} UK.
        name_count: int = sess.query(Course).filter(Course.departmentAbbreviation == new_department.abbreviation,
                                                    Course.name == course.name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            # Make sure that moving the course will not violate the {departmentAbbreviation,
            # course number} uniqueness constraint.
            number_count = sess.query(Course). \
                filter(Course.departmentAbbreviation == new_department.abbreviation,
                       Course.courseNumber == course.courseNumber).count()
            if number_count != 0:
                print("We already have a course by that number in that department.  Try again.")
            else:
                course.set_department(new_department)


def select_student_from_list(session):
    """
    This is just a cute little use of the Menu object.  Basically, I create a
    menu on the fly from data selected from the database, and then use the
    menu_prompt method on Menu to display characteristic descriptive data, with
    an index printed out with each entry, and prompt the user until they select
    one of the Students.
    :param session:     The connection to the database.
    :return:            None
    """
    # query returns an iterator of Student objects, I want to put those into a list.  Technically,
    # that was not necessary, I could have just iterated through the query output directly.
    students: [Department] = list(sess.query(Department).order_by(Department.lastName, Department.firstName))
    options: [Option] = []  # The list of menu options that we're constructing.
    for student in students:
        # Each time we construct an Option instance, we put the full name of the student into
        # the "prompt" and then the student ID (albeit as a string) in as the "action".
        options.append(Option(student.lastName + ', ' + student.firstName, student.studentId))
    temp_menu = Menu('Student list', 'Select a student from this list', options)
    # text_studentId is the "action" corresponding to the student that the user selected.
    text_studentId: str = temp_menu.menu_prompt()
    # get that student by selecting based on the int version of the student id corresponding
    # to the student that the user selected.
    returned_student = sess.query(Department).filter(Department.studentId == int(text_studentId)).first()
    # this is really just to prove the point.  Ideally, we would return the student, but that
    # will present challenges in the exec call, so I didn't bother.
    print("Selected student: ", returned_student)


def list_department_courses(sess):
    department = select_department(sess)
    dept_courses: [Course] = department.get_courses()
    print("Course for department: " + str(department))
    for dept_course in dept_courses:
        print(dept_course)


if __name__ == '__main__':
    print('Starting off')
    logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    logging.getLogger("sqlalchemy.engine").setLevel(eval(logging_action))
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    logging.getLogger("sqlalchemy.pool").setLevel(eval(logging_action))

    # Prompt the user for whether they want to introspect the tables or create all over again.
    introspection_mode: int = IntrospectionFactory().introspection_type
    if introspection_mode == START_OVER:
        print("starting over")
        # create the SQLAlchemy structure that contains all the metadata, regardless of the introspection choice.
        metadata.drop_all(bind=engine)  # start with a clean slate while in development

        # Create whatever tables are called for by our "Entity" classes that we have imported.
        metadata.create_all(bind=engine)
    elif introspection_mode == INTROSPECT_TABLES:
        print("reusing tables")
        # The reflection is done in the imported files that declare the entity classes, so there is no
        # reflection needed at this point, those classes are loaded and ready to go.
    elif introspection_mode == REUSE_NO_INTROSPECTION:
        print("Assuming tables match class definitions")

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')
