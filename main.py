import json
import pymongo
from academy_sqlite import Student, Advisor
from db_managers.sqlite_manager import DatabaseManager as SqlManager
from db_managers.mongo_manager import DatabaseManager as MongoManager

if __name__ == "__main__":
    # Open json file and read data to store and manipulate in databases
    with open('data.json', 'r') as f:
        data = json.load(f)
        advisors = data['advisors']
        students = data['students']

    """
    Demonstrate several actions using SQLite database manager below
    """
    # Initialize and create tables in sqlite database
    sql_manager = SqlManager()
    sql_manager.create_table()

    # First we add advisors to DB, so that students can choose their advisors
    for advisor_id, advisor_dict in enumerate(advisors, start=1):
        advisor = Advisor(advisor_id, advisor_dict['name'], advisor_dict['surname'], advisor_dict['age'])
        advisor.add_advisor('advisors')

    # Here we add students to student and their advisors
    for student_id, student_dict in enumerate(students, start=1):
        student = Student(student_id, student_dict['name'], student_dict['surname'], student_dict['age'], 5)
        student.add_student('students')
        student.add_advisor_relationship('advisors', 'student_advisor')

    # Example code to update and search db
    sql_manager.update('students', {'name': 'Jason', 'surname': 'Brody'}, {'age': 20})
    print('Updated entries in students table:')
    print(sql_manager.search('students', ['name', 'surname', 'age'], {'age': 20}))

    """
    Demonstrate several actions using MongoDb database manager below
    """
    mongo_manager = MongoManager()

    try:  # Try to create collections in database
        mongo_manager.create_collection('students')
        mongo_manager.create_collection('advisors')
        mongo_manager.create_collection('student_advisor')
    except pymongo.errors.CollectionInvalid:
        pass

    # Add each advisor to DB
    for adv_id, advisor in enumerate(advisors, start=1):
        mongo_manager.add_document('advisors', adv_id, advisor)

    # Add each student in 'students' collection and then for each student add 5 random adviser in junction collection
    for stud_id, student in enumerate(students, start=1):
        mongo_manager.add_document('students', stud_id, student)

        # Adding random advisors for each student
        random_advisor_ids = mongo_manager.get_random_data_ids('advisors', 5)
        for inner_id, rand_advisor_id in enumerate(random_advisor_ids, start=1):
            doc_id = f'{stud_id}_{inner_id}'
            mongo_manager.add_document('student_advisor',
                                       doc_id,
                                       {'student_id': stud_id, 'advisor_id': rand_advisor_id})

    # Demonstrate retrieval of relationships: get list of students for each advisor
    relationships = mongo_manager.get_relationships('advisors', 'students', '_id', '_id')
    print(f'\n{relationships}')
