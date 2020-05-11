import sqlite3

#  CREATE TABLE STUDENTS(
#    ...> ID INT PRIMARY KEY,
#    ...> NAME TEXT NOT NULL,
#    ...> SEMESTER INT NOT NULL,
#    ...> DEGREE TEXT NOT NULL
#    ...> );

# CREATE TABLE CLASSES(
#    ...> DEGREE TEXT NOT NULL,
#    ...> SEMESTER INT NOT NULL,
#    ...> SUBJECT TEXT NOT NULL
#    ...> );

conn = sqlite3.connect('attendance.db')


cur = conn.cursor()

def add_student():
    id = int(input('Enter id: '))
    name = input('Enter name: ')
    semester = int(input('Enter semester: '))
    degree = input('Enter degree: ')

    try:
        cur.execute('INSERT INTO STUDENTS VALUES (?, ?, ?, ?)', (id, name, semester, degree))
        conn.commit()
    except Exception as e:
        print(e)
    else:
        print('\nStudent Added')

def remove_student():
    id = int(input('Enter id: '))

    try:
        cur.execute('DELETE FROM STUDENTS WHERE ID = ?', (id,))
        conn.commit()
    except Exception as e:
        print(e)
    else:
        print('\nStudent Removed')

def view_students():
    for row in cur.execute('SELECT * FROM STUDENTS'):
        print(row)

def add_subject():
    degree = input('Enter degree: ')
    semester = int(input('Enter semester: '))
    subject = input('Enter subject name: ')

    try:
        cur.execute('INSERT INTO CLASSES VALUES (?, ?, ?)', (degree, semester, subject))

        cur.execute(f'''CREATE TABLE {subject}(
                        ID INT NOT NULL,
                        DATE TEXT NOT NULL,
                        DEGREE TEXT NOT NULL,
                        PRESENCE INT NOT NULL,
                        PRIMARY KEY(ID, DATE)
                        );
        ''',)

        conn.commit()
    except Exception as e:
        print(e)
    else:
        print('\nSubject Added')

def remove_subject():
    degree = input('Enter degree: ')
    semester = int(input('Enter semester: '))
    subject = input('Enter subject name: ')

    try:
        cur.execute(f'DROP TABLE {subject}')
        cur.execute('DELETE FROM CLASSES WHERE DEGREE = ? AND SUBJECT = ? AND SEMESTER = ?', (degree, subject, semester))
    except Exception as e:
        print(e)
    else:
        print('\nSubject Deleted')

def view_subjects():
    for row in cur.execute('SELECT * FROM CLASSES'):
        print(row)

def view_full_record():
    degree = input('Enter degree: ')
    subject = input('Enter subject name: ')

    try:
        for row in cur.execute(f'SELECT * FROM {subject} WHERE DEGREE = ?', (degree,)):
            print(row)
    except Exception as e:
        print(e)

def menu():
    print('\n===================')
    print('1. Add a student')
    print('2. Remove a student')
    print('3. View all students')
    print('4. Add a subject')
    print('5. Remove a subject')
    print('6. View all subject')
    print('7. View full record of a subject')
    print('8. Exit')
    print('===================\n')
    option = int(input("Enter choice: "))

    if option == 1:
        add_student()
        return True

    elif option == 2:
        remove_student()
        return True

    elif option == 3:
        view_students()
        return True

    elif option == 4:
        add_subject()
        return True

    elif option == 5:
        remove_subject()
        return True

    elif option == 6:
        view_subjects()
        return True

    elif option == 7:
        view_full_record()
        return True

    elif option == 8:
        return False

    else:
        print('Invalid Choice')
        return True


while menu():
    pass

conn.close()