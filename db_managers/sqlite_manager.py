import sqlite3


class DatabaseManager:
    def __init__(self):
        self.db_path = '../academy.db'

    def create_connection(self):
        return sqlite3.connect(self.db_path)

    def create_table(self):
        with self.create_connection() as conn:
            curs = conn.cursor()
            curs.executescript('''
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                age INTEGER
            );

            CREATE TABLE IF NOT EXISTS advisors (
                advisor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                age INTEGER
            );

            CREATE TABLE IF NOT EXISTS student_advisor (
                student_id INTEGER,
                advisor_id INTEGER,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (advisor_id) REFERENCES advisors(advisor_id),
                PRIMARY KEY (student_id, advisor_id)
            );
            ''')
            conn.commit()

    def add_record(self, table_name: str, *args):
        """Adds a record based on provided parameters"""
        with self.create_connection() as conn:
            curs = conn.cursor()
            args_placeholders = (len(args) - 1) * '?, ' + '?'  # Question marks needed for query
            query = f"INSERT INTO {table_name} VALUES ({args_placeholders})"
            curs.execute(query, args)
            conn.commit()

    def get_random_data(self, table_name: str, sample_size: int):
        """Returns a list of randomly selected non-repeating rows (tuples) of given size"""
        with self.create_connection() as conn:
            curs = conn.cursor()
            curs.execute(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT {sample_size}")
            return curs.fetchall()

    def get_count_of_relations(self, table_name: str, col_name: str, value_in_col):
        """Returns a count of relationship one entity has"""
        with self.create_connection() as conn:
            curs = conn.cursor()
            curs.execute(f"SELECT COUNT ({col_name}) FROM {table_name} WHERE {col_name} = {value_in_col}")
            return curs.fetchone()[0]

    def delete_row_by_key(self, table_name: str, col_name: str, prim_key):
        """Deleter a record based on the primary key"""
        with self.create_connection() as conn:
            curs = conn.cursor()
            curs.execute(f"DELETE FROM {table_name} WHERE {col_name} = ?", (prim_key,))
            conn.commit()

    def load_data(self, table_name: str):
        """Returns all data from a table"""
        with self.create_connection() as conn:
            curs = conn.cursor()
            curs.execute(f"SELECT * FROM {table_name}")
            return curs.fetchall()

    def search(self, table_name: str, columns=None, conditions=None):
        """Selects specific columns from a table based on multiple conditions.

        Args:
        - table_name: The name of the table to select from.
        - columns: (Optional) A list of column names to select. If None, selects all columns.
        - conditions: (Optional) A dictionary where keys are column names and values are the corresponding condition values.

        Returns:
        - A list of tuples, where each tuple represents a row selected from the table.
        """
        with self.create_connection() as conn:
            curs = conn.cursor()
            # Building a query
            if columns:
                selected_columns = ', '.join(columns)
            else:
                selected_columns = '*'
            query = f"SELECT {selected_columns} FROM {table_name}"
            condition_values = ()

            if conditions:
                condition_str = ' AND '.join([f"{column} = ?" for column in conditions.keys()])
                query += f" WHERE {condition_str}"
                condition_values = tuple(conditions.values())

            curs.execute(query, condition_values)
            return curs.fetchall()

    def update(self, table_name: str, update_values: dict, conditions: dict):
        """Updates values in table based on multiple parameters
        
        Args:
        - table_name: name of the table to update values.
        - update_values: dictionary where keys are columns that should be updated and values are values that should be set
        - conditions: dictionary where keys are condition columns and values are current values
        """
        with self.create_connection() as conn:
            curs = conn.cursor()
            query = f'UPDATE {table_name} SET '
            update_cols = ' '.join([f'{val} = ?,' for val in update_values.keys()])[:-1]
            update_values = list(update_values.values())

            condition_cols = ' '.join([f'{col} = ? and' for col in conditions.keys()])[:-3]
            condition_values = list(conditions.values())
            query += update_cols + ' WHERE ' + condition_cols

            update_values.extend(condition_values)

            curs.execute(query, update_values)
            conn.commit()
