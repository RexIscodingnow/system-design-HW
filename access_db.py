import sqlite3

print(sqlite3.__doc__)


try:
    db = sqlite3.connect("test.db")
    cursor = db.cursor()

    cursor.execute("create table lang(user)")
    cursor.execute("insert into ")
    


except:
    print("error")

