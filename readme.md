# Database managers

### Description
This project demonstrates structure and usage of SQL and noSQL database managers with SQLite3 and MongoDB examples.

Both managers handle common database operations, plus demonstrate many-to-many relationship capabilities.

'academy_sqlite.py' contains 2 classes - Student and Advisor. They handle SQLite3 specific tasks.

'main.py' contains some usage examples of both databases. It's messy but works for demonstration purposes.
I have used 'data.json' as data source, which contains made up data about academic advisors and students.

Feel free to modify 'main.py' to use different methods defined in DB manager modules and achieve particular goals.

### Observations
MongoDB write and read times in this specific case were better than SQLite. However, defining and retrieving relationships
from SQL DB is more convenient and requires less code.

### Requirements
 - Python 3.x
 - pymongo

To install required packages run in terminal:
- pip install -r requirements.txt


