import sqlite3
from db_managers.sqlite_manager import DatabaseManager as SqlManager


class Student:
    def __init__(self, primary_key: int, name: str, surname: str, age: int, num_advisors: int):
        self.id = primary_key
        self.name = name
        self.surname = surname
        self.age = age
        self.num_advisors = num_advisors
        self.sql_manager = SqlManager()

    def add_student(self, table: str):
        """Adds a student to database"""
        try:
            self.sql_manager.add_record(table, self.id, self.name, self.surname, self.age)
        except sqlite3.IntegrityError:
            pass

    def add_advisor_relationship(self, advisor_table: str, junction_table: str):
        """Adds 5 random advisor for a student to database junction table.

        This method belongs to student class, 
        similar to real life when typically students choose advisors, not vice versa"""

        rand_advisors = self.sql_manager.get_random_data(advisor_table, self.num_advisors)
        for rand_advisor in rand_advisors:
            advisor_obj = Advisor(rand_advisor[0], rand_advisor[1], rand_advisor[2], rand_advisor[3])
            advisor_count = self.sql_manager.get_count_of_relations('student_advisor', 'student_id', self.id)

            if advisor_count < self.num_advisors:
                try:
                    self.sql_manager.add_record(junction_table, self.id, advisor_obj.id)
                except sqlite3.IntegrityError:
                    pass


class Advisor:
    def __init__(self, primary_key, name, surname, age):
        self.id = primary_key
        self.name = name
        self.surname = surname
        self.age = age
        self.sql_manager = SqlManager()

    def add_advisor(self, table: str):
        """Adds an advisor to database"""
        try:
            self.sql_manager.add_record(table, self.id, self.name, self.surname, self.age)
        except sqlite3.IntegrityError:
            pass
