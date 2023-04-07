import unittest
import sqlite3
import json
import os
import numpy as np
import matplotlib.pyplot as plt
# starter code

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# TASK 1
# CREATE TABLE FOR EMPLOYEE INFORMATION IN DATABASE AND ADD INFORMATION
def create_employee_table(cur, conn):
    employee_columns = ["employee_id", "first_name", "last_name", "job_id", "hire_date", "salary"]
    cur.execute('CREATE TABLE IF NOT EXISTS employees(employee_id INTEGER PRIMARY KEY,first_name TEXT,last_name TEXT,job_id INTEGER,hire_date TEXT,salary NUMERIC)')
    
    conn.commit()

# ADD EMPLOYEE'S INFORMTION TO THE TABLE
def add_employee(filename, cur, conn):
    #load .json file and read job data
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))
    file_data = f.read()
    f.close()
    # THE REST IS UP TO YOU
    json_data = json.loads(file_data)
    for employee in json_data:
        id = int(employee["employee_id"])
        f_name = str(employee["first_name"])
        l_name = str(employee["last_name"])
        job = int(employee["job_id"])
        date = str(employee["hire_date"])
        sal = int(employee["salary"])
        cur.execute("""INSERT OR IGNORE INTO employees(employee_id, first_name,last_name, job_id,hire_date, salary)VALUES(?, ?, ?, ?, ?, ?)""",(id, f_name, l_name, job, date, sal))
    conn.commit()

# TASK 2: GET JOB AND HIRE_DATE INFORMATION
def job_and_hire_date(cur, conn):
    cur.execute("SELECT Employees.hire_date, Jobs.job_title FROM Employees JOIN Jobs ON Employees.job_id=Jobs.job_id")
    job = cur.fetchone()[1]
    conn.commit()
    return job

# TASK 3: IDENTIFY PROBLEMATIC SALARY DATA
# Apply JOIN clause to match individual employees
def problematic_salary(cur, conn):
    cur.execute("SELECT Employees.first_name, Employees.last_name FROM Employees JOIN Jobs ON Jobs.job_id = Employees.job_id WHERE Employees.salary < Jobs.min_salary OR Employees.salary > Jobs.max_salary")
    lst = []
    for row in cur:
        lst.append(row)
    return lst

# TASK 4: VISUALIZATION
def visualization_salary_data(cur, conn):
    cur.execute("SELECT Jobs.job_title, Employees.salary FROM Jobs JOIN Employees ON Jobs.job_id = Employees.job_id")
    employee_data = cur.fetchall()
    cur.execute("SELECT job_title, min_salary, max_salary from Jobs")
    job_data = cur.fetchall()

    job_salaries = {}
    for employee in employee_data:
        job_id = employee[0]
        salary = employee[1]
        if job_id not in job_salaries:
            job_salaries[job_id] = [salary]
        else:
            job_salaries[job_id].append(salary)
    
    print(job_salaries)

    job_ranges = {}
    for job in job_data:
        job_ranges[job[0]] = (job[1], job[2])
    
    x = [employee[0] for employee in employee_data]
    y = [employee[1] for employee in employee_data]

    plt.scatter(x, y)

    for job_id, salary_range in job_ranges.items():
        plt.scatter(job_id, salary_range[0], color='red', marker='x')
        plt.scatter(job_id, salary_range[1], color='red', marker='x')

    plt.show()


class TestDiscussion12(unittest.TestCase):
    def setUp(self) -> None:
        self.cur, self.conn = setUpDatabase('HR.db')

    def test_create_employee_table(self):
        self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='employees'")
        table_check = self.cur.fetchall()[0][0]
        self.assertEqual(table_check, 1, "Error: 'employees' table was not found")
        self.cur.execute("SELECT * FROM employees")
        count = len(self.cur.fetchall())
        self.assertEqual(count, 13)

    def test_job_and_hire_date(self):
        self.assertEqual('President', job_and_hire_date(self.cur, self.conn))

    def test_problematic_salary(self):
        sal_list = problematic_salary(self.cur, self.conn)
        self.assertIsInstance(sal_list, list)
        self.assertEqual(sal_list[0], ('Valli', 'Pataballa'))
        self.assertEqual(len(sal_list), 4)


def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('HR.db')
    create_employee_table(cur, conn)

    add_employee("employee.json",cur, conn)

    job_and_hire_date(cur, conn)

    wrong_salary = (problematic_salary(cur, conn))
    print(wrong_salary)

    visualization_salary_data(cur, conn)

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)

