import mysql.connector

def create_db():
   
    mydatabase = mysql.connector.connect(
        host='127.0.0.1',  # MySQL Host (localhost)
        user='root',       # MySQL User Name (root)
        password='YOUR DATABASE PASSWORD', # MySQL Password
        database='project_management'  # Database Name 
    )

    cursor = mydatabase.cursor()

    # Projects tablosu oluşturma
    cursor.execute('''CREATE TABLE IF NOT EXISTS Projects (
                        id INT PRIMARY KEY,
                        name VARCHAR(255),
                        start_date DATE,
                        end_date DATE''')

    # Employees tablosu oluşturma
    cursor.execute('''CREATE TABLE IF NOT EXISTS Employees (
                        id INT PRIMARY KEY,
                        name VARCHAR(255),
                        position VARCHAR(255))''')

    # Tasks tablosu oluşturma
    cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks (
                        id INT PRIMARY KEY,
                        project_id INT,
                        employee_id INT,
                        name VARCHAR(255),
                        status ENUM("TAMAMLANDI","DEVAM EDIYOR","TAMAMLANACAK"),
                        peson_day INT,
                        FOREIGN KEY (project_id) REFERENCES Projects(id),
                        FOREIGN KEY (employee_id) REFERENCES Employees(id))''')

    
    mydatabase.commit()
    mydatabase.close()

create_db()
