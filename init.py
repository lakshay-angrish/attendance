import sqlite3

conn = sqlite3.connect('attendance.db')

try:
    conn.execute('''CREATE TABLE STUDENTS(
                    ID INT PRIMARY KEY,
                    NAME TEXT NOT NULL,
                    SEMESTER INT NOT NULL,
                    DEGREE TEXT NOT NULL
                    );
    ''')

    conn.execute('''CREATE TABLE CLASSES(
                    DEGREE TEXT NOT NULL,
                    SEMESTER INT NOT NULL,
                    SUBJECT TEXT NOT NULL,
                    PRIMARY KEY(DEGREE, SEMESTER, SUBJECT)
                    );
    ''')

except Exception as e:
    print(e)

conn.commit()
conn.close()