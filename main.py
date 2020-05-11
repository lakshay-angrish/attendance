import sqlite3
import datetime

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
    for row in cur.execute('SELECT * FROM STUDENTS ORDER BY ID ASC'):
        print(row)

def add_subject():
    degree = input('Enter degree: ')
    semester = int(input('Enter semester: '))
    subject = input('Enter subject name: ')

    try:
        cur.execute('INSERT INTO CLASSES VALUES (?, ?, ?)', (degree, semester, subject))

        cur.execute(f'''CREATE TABLE IF NOT EXISTS {subject}(
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
    subject = input('Enter subject name: ')

    try:
        cur.execute(f'DROP TABLE {subject}')
        cur.execute('DELETE FROM CLASSES WHERE SUBJECT = ?', (subject,))
        conn.commit()
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

def mark_attendance():
    degree = input('Enter degree: ')
    semester = int(input('Enter semester: '))
    subject = input('Enter subject name: ')

    try:
        print('\nEnter 0 for absent, 1 for present')
        attendance = []
        for row in cur.execute('SELECT * FROM STUDENTS WHERE DEGREE = ? AND SEMESTER = ?', (degree, semester)):
            presence = int(input(f'{row[0]}: '))
            attendance.append((row[0], str(datetime.date.today()), degree, presence))

        cur.executemany(f'INSERT INTO {subject} VALUES (?, ?, ?, ?)', attendance)
        conn.commit()

    except Exception as e:
        print(e)
    else:
        print('\nAttendance Marked')


def monthly_report():
    degree = input('Enter degree: ')
    subject = input('Enter subject name: ')
    year = int(input('Enter year: '))
    month = int(input('Enter month: '))

    records = []
    total_days = []
    presents = {}

    try:
        for row in cur.execute(f'SELECT * FROM {subject} WHERE DEGREE = ? ORDER BY ID ASC', (degree, )):
            date = datetime.datetime.strptime(row[1], '%Y-%m-%d').date()
            if date.year == year and date.month == month:
                records.append(row)
                total_days.append(date.day)
                presents[row[0]] = 0

        distinct_days = set(total_days)
        print(f'Total days: {len(distinct_days)}')
        for record in records:
            if record[3] == 1:
                presents[record[0]] += 1

        for student, attendance in presents.items():
            percentage = (attendance * 100) / len(distinct_days)
            print(f'{student}: {percentage}%')

    except Exception as e:
        print(e)

def menu():
    print('\n===============================')
    print('1. Add a student')
    print('2. Remove a student')
    print('3. View all students')
    print('4. Add a subject')
    print('5. Remove a subject')
    print('6. View all subjects')
    print('7. Mark attendance')
    print('8. View full record of a subject')
    print('9. View monthly report')
    print('10. Exit')
    print('\n===============================')
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
        mark_attendance()
        return True

    elif option == 8:
        view_full_record()
        return True

    elif option == 9:
        monthly_report()
        return True

    elif option == 10:
        return False

    else:
        print('Invalid Choice')
        return True


while menu():
    pass

conn.close()