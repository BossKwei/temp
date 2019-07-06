import sqlite3


def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("CREATE TABLE blog (id INT, article TEXT)")
    c.execute("INSERT INTO blog VALUES(10001, 'a123456')")
    c.execute("INSERT INTO blog VALUES(10002, 'b123456')")
    c.execute("INSERT INTO blog VALUES(10003, 'c123456')")
    conn.commit()
    conn.close()


def inquire_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT * FROM blog")
    results = c.fetchall()
    print(type(results), results)
    conn.close()


if __name__ == '__main__':
    init_db()
    inquire_db()
