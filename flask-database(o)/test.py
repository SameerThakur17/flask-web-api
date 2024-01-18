import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int,username text,password text)"
cursor.execute(create_table)

# inserting into the database
user = (1, "sam", "abc")
insert_query = "INSERT INTO users VALUES(? ,? ,?)"
cursor.execute(insert_query, user)

# inserting multiple rows of data
users = [(2, "rkay", "xyz"), (3, "ks", "kra")]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"

# retrieving data from the db
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
