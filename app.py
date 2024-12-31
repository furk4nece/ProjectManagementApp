import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import datetime


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Management")

        self.root.geometry("850x600")
        self.selected_project_id = None
        self.selected_employee_id = None
        self.selected_task_id = None

        self.create_widgets()

    def add_task(self):
        task_name = self.task_name_entry.get()
        status = self.status_combobox.get()
        task_id = self.task_id_entry.get()
        person_day = self.person_day_entry.get()
        project_name = self.project_id_combobox.get() 
        project_id = None
        employee_name = self.employee_id_combobox.get() 
        employee_id = None
        
        for project in self.projects:
            if project[2] == project_name: 
                project_id = project[0] 
                break
       
        for employee in self.employees:
            if employee[1] == employee_name: 
                employee_id = employee[0] 
                break
    
        if not task_id or not task_name or not project_name or not employee_name or not status:
            messagebox.showerror("Error", "All fields are required.")
            return

        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Tasks (id, task_name, project_id, employee_id, status, person_day) VALUES (%s, %s, %s, %s, %s, %s)", 
                (task_id, task_name if task_name else None, project_id, employee_id, status if status else None, person_day if person_day else None)
            )
            conn.commit()
            messagebox.showinfo("Success", "Task added successfully.")
            self.refresh_task_list()
            self.refresh_project_combobox()
            self.refresh_employee_combobox()
            self.check_and_extend_task_due_dates()
            self.refresh_project_list()
            self.task_id_entry.delete(0, tk.END)
            self.task_name_entry.delete(0, tk.END)
            self.project_id_combobox.set("") 
            self.employee_id_combobox.set("")
            self.delay_combobox.set("")
            self.status_combobox.set("")
            self.person_day_entry.delete(0, tk.END)


        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            conn.close()


   

    def add_employee(self):
        name = self.employee_name_entry.get()
        position = self.employee_position_entry.get()
        employee_id = self.employee_id_entry.get()

        if not employee_id or not name or not position :
            messagebox.showerror("Error", "All fields are required.")
            return

        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Employees (id, name, position) VALUES (%s, %s, %s)", 
                           (employee_id, name if name else None, position if position else None))
            conn.commit()
            messagebox.showinfo("Success", "Employee added successfully.")
            self.refresh_employee_list()
            self.refresh_employee_combobox()
            self.employee_name_entry.delete(0, tk.END)
            self.employee_position_entry.delete(0, tk.END)
            self.employee_id_entry.delete(0, tk.END)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", "ID already exists.")
        finally:
            conn.close()
        
    def add_project(self):
        project_id = self.project_id_entry.get() 
        name = self.project_name_entry.get()
        start_date = self.project_start_entry.get()
        end_date = self.project_end_entry.get()
    
        if not project_id or not name or not start_date or not end_date :
            messagebox.showerror("Error", "All fields are required.")
            return
        
        

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM Projects WHERE id=%s", (project_id,))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showerror("Error", "ID already exists.")
                return
            else : 
                cursor.execute(
                "INSERT INTO Projects (id, name, start_date, end_date) VALUES (%s, %s, %s, %s)", 
                (project_id, name if name else None, start_date if start_date else None, end_date if end_date else None)
                )
            conn.commit()
            messagebox.showinfo("Success", "Project added successfully.")

            self.check_and_extend_task_due_dates()
            self.refresh_project_list()
            self.refresh_project_combobox()
            self.delay_combobox.set("")
            self.project_id_entry.delete(0, tk.END)
            self.project_name_entry.delete(0, tk.END)
            self.project_start_entry.delete(0, tk.END)
            self.project_end_entry.delete(0, tk.END)

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()



    def update_project(self):
        selected = self.project_listbox.curselection()
        
        if not selected:
            messagebox.showerror("Error", "No project selected.")
            return

        project_id = self.project_listbox.get(selected[0]).split(',')[0].split(':')[1].strip()

        name = self.project_name_entry.get()
        start_date = self.project_start_entry.get()
        end_date = self.project_end_entry.get()

        if not project_id:
            messagebox.showerror("Error", "ID required.")
            return

        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, start_date, end_date FROM Projects WHERE id=%s", (project_id,))
        project = cursor.fetchone()
        new_project_name = name if name else project[0]  
        new_project_start = start_date if start_date else project[1]  
        new_project_end = end_date if end_date else project[2] 
        
        try:
            cursor.execute("UPDATE Projects SET name=%s, start_date=%s, end_date=%s WHERE id=%s", 
                           (new_project_name if new_project_name else "", new_project_start if new_project_start else None, new_project_end if new_project_end else None, project_id ))
            conn.commit()
            messagebox.showinfo("Success", "Project updated successfully.")
            self.project_end_entry.delete(0, tk.END)
            self.project_start_entry.delete(0, tk.END)
            self.project_name_entry.delete(0, tk.END)
            self.check_and_extend_task_due_dates()
            self.refresh_project_list()
            self.refresh_project_combobox()
            self.delay_combobox.set("")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    
    
    def delete_project(self):
        selected = self.project_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No project selected.")
            return

        project_id = self.project_listbox.get(selected[0]).split(',')[0].split(':')[1].strip()

        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Projects WHERE id=%s", (project_id,))
            conn.commit()
            messagebox.showinfo("Success", "Project deleted successfully.")
            self.refresh_project_list()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def create_widgets(self):
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)
        self.create_project_tab()
        self.create_employee_tab()
        self.create_task_tab()
        self.refresh_project_combobox()

    


    def create_project_tab(self):
        self.project_tab = tk.Frame(self.tabs, bg="#f0f0f0")
        self.tabs.add(self.project_tab, text="Projects")

        self.project_listbox = tk.Listbox(self.project_tab, height=6, width=80, selectmode=tk.SINGLE)
        self.project_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.project_id_entry = self.create_labeled_entry(self.project_tab, "Project ID", 1, 0)
        self.project_name_entry = self.create_labeled_entry(self.project_tab, "Project Name", 2, 0)
        self.project_start_entry = self.create_labeled_entry(self.project_tab, "Start Date (YYYY-MM-DD)", 3, 0)
        self.project_end_entry = self.create_labeled_entry(self.project_tab, "End Date (YYYY-MM-DD)", 4, 0)

        self.project_listbox.bind("<Double-1>", self.open_project_detail)

        self.delay_label = tk.Label(self.project_tab, text="Select Delay: ", bg="#f0f0f0")
        self.delay_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.delay_combobox = ttk.Combobox(self.project_tab, values=["1 Week", "2 Weeks", "3 Weeks", "1 Month"], state="readonly")
        self.delay_combobox.grid(row=5, column=1, padx=10, pady=10)

        
        self.add_project_button = self.create_button(self.project_tab, "Add Project", self.add_project, 7, 0)
        self.update_project_button = self.create_button(self.project_tab, "Update Project", self.update_project, 8, 0)
        self.delete_project_button = self.create_button(self.project_tab, "Delete Project", self.delete_project, 9, 0)

        self.refresh_project_list()
    
    def open_employee_details(self, event):
        selected_employee = self.employee_listbox.curselection()
        if not selected_employee:
            messagebox.showerror("Error", "No employee selected.")
            return

        employee_id = self.employee_listbox.get(selected_employee[0]).split(',')[0].split(':')[1].strip()


        detail_window = tk.Toplevel(self.task_tab)
        detail_window.title(f"Employee Details - {employee_id}")


        conn = self.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT task_name, p.name AS project_name, t.status, t.person_day
            FROM Tasks t
            JOIN Projects p ON t.project_id = p.id
            WHERE t.employee_id = %s
        """, (employee_id,))


        tasks = cursor.fetchall()

        if not tasks:
            messagebox.showinfo("Info", "No tasks found for this employee.")
            conn.close()
            return

        task_listbox = tk.Listbox(detail_window, width=100, height=15)
        task_listbox.pack(padx=10, pady=10)
        for task in tasks :
            task_listbox.insert(tk.END, f"Project Name : {task[1]},  Task Name : {task[0]},  Status : {task[2]},  Person-Day : {task[3]}")
        
        conn.close()

      

    def open_project_detail(self, event):
        selected_project = self.project_listbox.curselection()
        if not selected_project:
            return

        project_info = self.project_listbox.get(selected_project[0])
       
        project_window = tk.Toplevel(self.root)
        project_window.title("Project Detail")
      
        project_details = project_info.split(", ")
        project_id = project_details[0].split(":")[1].strip()
        project_name = project_details[1].split(":")[1].strip()
        project_start_date = project_details[2].split(":")[1].strip()
        project_end_date = project_details[3].split(":")[1].strip()

        details_text = f"Project ID: {project_id}\nProject Name: {project_name}\nStart Date: {project_start_date}\nEnd Date: {project_end_date}"

        label = tk.Label(project_window, text=details_text, padx=10, pady=10)
        label.pack()

        task_listbox = tk.Listbox(project_window, height=6, width=70)
        task_listbox.pack(padx=10, pady=10)

        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            SELECT T.task_name, T.status, E.name 
            FROM Tasks T
            LEFT JOIN Employees E ON T.employee_id = E.id
            WHERE T.project_id = %s
            """, (project_id,))
            tasks = cursor.fetchall()
            for task in tasks:
                task_name = task[0]
                task_status = task[1]
                employee_name = task[2] if task[2] else "There is no employee attend" 
                task_listbox.insert(tk.END, f"Task Name: {task_name}, Status: {task_status}, Employee: {employee_name}")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
            self.refresh_task_list()
        finally:
            conn.close()

        close_button = tk.Button(project_window, text="Close", command=project_window.destroy)
        close_button.pack(pady=10)


    def create_employee_tab(self):
        self.employee_tab = tk.Frame(self.tabs, bg="#f0f0f0")
        self.tabs.add(self.employee_tab, text="Employees")

        self.employee_listbox = tk.Listbox(self.employee_tab, height=6, width=80, selectmode=tk.SINGLE)
        self.employee_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.employee_id_entry = self.create_labeled_entry(self.employee_tab, "Employee ID", 1, 0)
        self.employee_name_entry = self.create_labeled_entry(self.employee_tab, "Name", 2, 0)
        self.employee_position_entry = self.create_labeled_entry(self.employee_tab, "Position", 3, 0)

        self.employee_listbox.bind("<Double-1>", self.open_employee_details)

        self.add_employee_button = self.create_button(self.employee_tab, "Add Employee", self.add_employee, 5, 0)
        self.update_employee_button = self.create_button(self.employee_tab, "Update Employee", self.update_employee, 6, 0)
        self.delete_employee_button = self.create_button(self.employee_tab, "Delete Employee", self.delete_employee, 7, 0)

        self.refresh_employee_list()

    def display_employee_projects_and_tasks(self):
        selected_employee = self.employee_listbox.curselection()
        if not selected_employee:
            messagebox.showerror("Error", "No employee selected.")
            return

        employee_id = self.employee_listbox.get(selected_employee[0]).split(',')[0].split(':')[1].strip()

        conn = self.get_db_connection()
        cursor = conn.cursor()

        # Çalışanın projelerini al
        cursor.execute("""
            SELECT p.id, p.project_name, t.task_name 
            FROM Projects p
            JOIN Tasks t ON p.id = t.project_id
            WHERE t.employee_id = %s
        """, (employee_id,))
        projects_tasks = cursor.fetchall()

        if not projects_tasks:
            messagebox.showinfo("No Projects", "This employee is not assigned to any projects.")
            return

        # Seçilen çalışanın projeleri ve görevleriyle ilgili listeyi güncelle
        self.employee_projects_listbox.delete(0, tk.END)
        for project, task in projects_tasks:
            self.employee_projects_listbox.insert(tk.END, f"Project ID: {project[0]}, Project Name: {project[1]}, Task: {task[2]}")

        conn.close()

    def create_task_tab(self):
        self.task_tab = tk.Frame(self.tabs, bg="#f0f0f0")
        self.tabs.add(self.task_tab, text="Tasks")

        self.task_listbox = tk.Listbox(self.task_tab, height=6, width=100, selectmode=tk.SINGLE)
        self.task_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.task_id_entry = self.create_labeled_entry(self.task_tab, "Task ID", 1, 0)
        self.task_name_entry = self.create_labeled_entry(self.task_tab, "Task Name", 2, 0)
        
        project_names = [project[2] for project in self.projects]

        project_label = tk.Label(self.task_tab, text="Select Project:")
        project_label.grid(row=3, column=0, padx=10, pady=10, sticky="w") 
        self.project_id_combobox = ttk.Combobox(self.task_tab, values=project_names, state="readonly")
        self.project_id_combobox.grid(row=3, column=1, padx=10, pady=10) 
       
        employee_names = [employee[1] for employee in self.employees]
        employee_label = tk.Label(self.task_tab, text="Select Employees:")
        employee_label.grid(row=4, column=0, padx=10, pady=10, sticky="w") 
        self.employee_id_combobox = ttk.Combobox(self.task_tab, values=employee_names, state="readonly")
        self.employee_id_combobox.grid(row=4, column=1, padx=10, pady=10) 

        self.status_label = tk.Label(self.task_tab, text="Task Status:", bg="#f0f0f0")
        self.status_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.status_combobox = ttk.Combobox(self.task_tab, values=["TAMAMLANDI", "DEVAM EDIYOR", "TAMAMLANACAK"], state="readonly")
        self.status_combobox.grid(row=5, column=1, padx=10, pady=10)

        self.person_day_entry = self.create_labeled_entry(self.task_tab, "Person-Day", 6, 0)

        self.add_task_button = self.create_button(self.task_tab, "Add Task", self.add_task, 8, 0)
        self.update_task_button = self.create_button(self.task_tab, "Update Task", self.update_task, 9, 0)
        self.delete_task_button = self.create_button(self.task_tab, "Delete Task", self.delete_task, 10, 0)

        self.refresh_task_list()



    
    def update_task(self):
        selected_task = self.task_listbox.curselection()
        if not selected_task:
            messagebox.showerror("Error", "No task selected.")
            return

        task_id = self.task_listbox.get(selected_task[0]).split(',')[0].split(':')[1].strip()
        task_name = self.task_name_entry.get()
        status = self.status_combobox.get()
        person_day = self.person_day_entry.get()
        project_name = self.project_id_combobox.get() 
        project_id = None
        employee_name = self.employee_id_combobox.get() 
        employee_id = None
        
        for project in self.projects:
            if project[2] == project_name: 
                project_id = project[0] 
                break
       
        for employee in self.employees:
            if employee[1] == employee_name: 
                employee_id = employee[0] 
                break

        if not task_id:
            messagebox.showerror("Error", "ID required.")
            return

        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT task_name, project_id, employee_id, status, person_day FROM Tasks WHERE id=%s", (task_id,))
        task = cursor.fetchone()

        new_task_name = task_name if task_name else task[0]   
        new_task_prject_id = project_id if project_id else task[1] 
        new_task_employee_id = employee_id if employee_id else task[2]
        new_task_status = status if status else task[3]
        new_person_day = person_day if person_day else task[4]

        try:
    
            cursor.execute("SELECT COUNT(*) FROM Tasks WHERE id=%s", (task_id,))
            count = cursor.fetchone()[0]

            if count == 0:
                messagebox.showerror("Error", "ID does not exist.")
                return

        
            cursor.execute("UPDATE Tasks SET task_name=%s, project_id=%s, employee_id=%s, status=%s, person_day=%s WHERE id=%s", 
                        (new_task_name if new_task_name else None , new_task_prject_id if new_task_prject_id else None, 
                         new_task_employee_id if new_task_employee_id else None,
                          new_task_status if new_task_status else None, new_person_day if new_person_day else None, task_id))
            conn.commit()
            messagebox.showinfo("Success", "Task updated successfully.")
            self.check_and_extend_task_due_dates()
            self.refresh_task_list()
            self.refresh_project_combobox()
            self.refresh_project_list()
            self.refresh_employee_combobox()
            self.person_day_entry.delete(0, tk.END)
            self.task_id_entry.delete(0, tk.END)
            self.task_name_entry.delete(0, tk.END)
            self.project_id_combobox.set("") 
            self.employee_id_combobox.set("")
            self.delay_combobox.set("")
            
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()
    
    def get_task_status_options(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW COLUMNS FROM Tasks LIKE 'status'")
        column_info = cursor.fetchone()
        if column_info:
            enum_values = column_info[1] 
            enum_values = enum_values.strip('enum()').split(',')
            enum_values = [value.strip("'") for value in enum_values]  
            return enum_values
        return []
    

    


    def create_labeled_entry(self, parent, label, row, column, **kwargs):
        label_widget = tk.Label(parent, text=label, bg="#f0f0f0")
        label_widget.grid(row=row, column=column, padx=10, pady=5, sticky="w")
        entry_widget = tk.Entry(parent, **kwargs)
        entry_widget.grid(row=row, column=column + 1, padx=10, pady=5)
        return entry_widget


    def create_button(self, parent, text, command, row, column):
        button_widget = tk.Button(parent, text=text, command=command)
        button_widget.grid(row=row, column=column, padx=10, pady=5)

    def get_db_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="qqasw123",
            database="project_management"
        )
    
    

    def update_employee(self):
        selected = self.employee_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No employee selected.")
            return

        employee_id = self.employee_listbox.get(selected[0]).split(',')[0].split(':')[1].strip()
        name = self.employee_name_entry.get()
        position = self.employee_position_entry.get()

        if not employee_id:
            messagebox.showerror("Error", "All fields are required.")
            return

        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, position FROM Employees WHERE id=%s", (employee_id,))
        employee = cursor.fetchone()
        
        new_employee_name = name if name else employee[0] 
        new_employee_position = position if position else employee[1]

        try:
            cursor.execute("UPDATE Employees SET name=%s, position=%s WHERE id=%s", (new_employee_name, new_employee_position, employee_id))
            conn.commit()
            messagebox.showinfo("Success", "Employee updated successfully.")
            self.refresh_employee_list()
            self.refresh_employee_combobox()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def delete_task(self):
        selected_task = self.task_listbox.curselection()
        if not selected_task:
            messagebox.showerror("Error", "No task selected.")
            return

        task_id = self.task_listbox.get(selected_task[0]).split(',')[0].split(':')[1].strip()

        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Tasks WHERE id=%s", (task_id,))
            conn.commit()
            messagebox.showinfo("Success", "Task deleted successfully.")
            self.refresh_task_list()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()


    def delete_employee(self):
        selected = self.employee_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No employee selected.")
            return

        employee_id = self.employee_listbox.get(selected[0]).split(',')[0].split(':')[1].strip()

        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Employees WHERE id=%s", (employee_id,))
            conn.commit()
            messagebox.showinfo("Success", "Employee deleted successfully.")
            self.refresh_employee_list()
            self.refresh_employee_combobox()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()



    def check_and_extend_task_due_dates(self):
        today = datetime.date.today()
        selected_delay = self.delay_combobox.get() 
        delay_days = 0
        
        if selected_delay == "1 Week":
            delay_days = 7
        elif selected_delay == "2 Weeks":
            delay_days = 14
        elif selected_delay == "3 Weeks":
            delay_days = 21
        elif selected_delay == "1 Month":
            delay_days = 30 
        else:
            delay_days = 7

        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, project_id, status FROM Tasks")
            tasks = cursor.fetchall()
            
            cursor.execute("SELECT id, end_date FROM Projects")
            projects = cursor.fetchall()

            for task in tasks:
                task_status = task[2]  
                task_project_id = task[1]
                
                if task_status == 'TAMAMLANDI':
                    continue 

                for project in projects:
                    project_id = project[0]
                    project_end_date = project[1]
                    
                    if task_project_id == project_id and task_status != 'TAMAMLANDI' and project_end_date < today:
                        new_end_date = today + datetime.timedelta(days=delay_days)
                        cursor.execute("UPDATE Projects SET end_date=%s WHERE id=%s", (new_end_date, project_id))
                        conn.commit()
                        messagebox.showinfo("Success", f"Project ID {project_id} teslim tarihi {new_end_date} olarak güncellendi.")
                        break

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    
    
    def refresh_project_combobox(self):
        project_names = [project[2] for project in self.projects]
        self.project_id_combobox['values'] = project_names

    def refresh_employee_combobox(self):
        employee_names = [employee[1] for employee in self.employees]
        self.employee_id_combobox['values'] = employee_names


    def refresh_project_list(self):
        self.project_listbox.delete(0, tk.END)
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Projects")
        self.projects = cursor.fetchall()
        for project in self.projects:
            self.project_listbox.insert(tk.END, f"Project ID: {project[0]}, Project Name: {project[2]}, Start Date: {project[3]}, End Date: {project[4]}")
        conn.close()

    def refresh_employee_list(self):
        self.employee_listbox.delete(0, tk.END)
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Employees")
        self.employees = cursor.fetchall()
        for employee in self.employees:
            self.employee_listbox.insert(tk.END, f"ID: {employee[0]}, Name: {employee[1]}, Position: {employee[2]}")
        conn.close()

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tasks")
        tasks = cursor.fetchall()

        for task in tasks:
            self.task_listbox.insert(tk.END, f"ID: {task[0]}, Name: {task[3]}, Project ID: {task[1]}, Status : {task[4]}, Person-Day : {task[5]}")   
        conn.close()


root = tk.Tk()
app = Application(root)
root.mainloop()


