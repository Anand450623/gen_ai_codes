import sqlite3

## connect to sqllite
connection=sqlite3.connect("student.db")

## create a cursor object for CRUD operation
cursor=connection.cursor()

## create
table_info = """
create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25),
SECTION VARCHAR(25), MARKS INT)
"""

cursor.execute(table_info)

## insert
cursor.execute("""insert into student values('krish', 'data science', 'A',90)""")
cursor.execute("""insert into student values('John', 'data science', 'B',100)""")
cursor.execute("""insert into student values('Mukesh', 'data science', 'A',86)""")
cursor.execute("""insert into student values('Jacob', 'data science', 'A',50)""")
cursor.execute("""insert into student values('Dipesh', 'data science', 'A',35)""")

## Display
print("The inserted records are")
data=cursor.execute("""select * from student""")
for row in data:
    print(row)

## Commit your changes in db
connection.commit()
connection.close()