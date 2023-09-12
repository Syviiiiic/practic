import tkinter as tk
from tkinter import messagebox
import psycopg2

class Employee:
    def __init__(self, id, first_name, last_name, phone):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone

class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title('List of Employes')
        self.root.geometry('400x300')

        self.create_table()

        self.add_button = tk.Button(self.root, text='Add', command=self.open_add_employee_window)  
        self.add_button.pack()

        self.delete_button = tk.Button(self.root, text='Delete', command=self.delete_employee)  
        self.delete_button.pack()

        self.edit_button = tk.Button(self.root, text='Edit', command=self.edit_employee)  
        self.edit_button.pack()

        self.list_box = tk.Listbox(self.root, width=40, height=10)
        self.list_box.pack()

        self.update_employee_listbox()

    def create_table(self):
        conn = self.connect_to_database()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                phone VARCHAR(15)
            )
        ''')
        conn.commit()
        conn.close()


    def connect_to_database(self):
        
        return psycopg2.connect(
            dbname='todo_employees',
            user='postgres',
            password='12321',
            host='localhost',
            port='5432'
            )
        # except Exception as _ex:
        #     print('Gavno!')
        # finally:
        #     if connection:
        #         connection.close()
        #         print('Connection closed')

        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         'SELECT version();'
        #     )
        #     print(f'Server version: {cursor.fetchone()}')

    def show_employees(self):
        conn = self.connect_to_database()
        cur = conn.cursor()
        cur.execute('SELECT * FROM employees')
        employees = cur.fetchall()
        conn.close()
        return employees
    

    def add_employee(self, first_name, last_name, phone):
        conn = self.connect_to_database()
        cur = conn.cursor()
        cur.execute('INSERT INTO employees (first_name, last_name, phone) VALUES (%s, %s, %s)', (first_name, last_name, phone))
        conn.commit()
        conn.close()

    
    def delete_employee(self):
        selected_index = self.list_box.curselection()
        if selected_index:
            employee_id = self.list_box.get(selected_index[0]).split(':')[1].strip(', Name')
            conn = self.connect_to_database()
            cur = conn.cursor()
            cur.execute('DELETE FROM employees WHERE id = %s', (employee_id,))
            conn.commit()
            conn.close()
            self.update_employee_listbox()

    
    def edit_employee(self):
        selected_index = self.list_box.curselection()
        if selected_index:
            self.add_edit_employee_window = tk.Toplevel(self.root)
            self.add_edit_employee_window.title('Edit employee')
            self.first_name_label = tk.Label(self.add_edit_employee_window, text='Name:')
            
            self.first_name_label.pack()
            self.first_name_entry = tk.Entry(self.add_edit_employee_window, )
            
            self.first_name_entry.pack()

            self.last_name_label = tk.Label(self.add_edit_employee_window, text='Surname:')
            self.last_name_label.pack()
            self.last_name_entry = tk.Entry(self.add_edit_employee_window)
            self.last_name_entry.pack()

            self.phone_label = tk.Label(self.add_edit_employee_window, text='Phone:')
            self.phone_label.pack()
            self.phone_entry = tk.Entry(self.add_edit_employee_window)
            self.phone_entry.pack()

            self.save_button = tk.Button(self.add_edit_employee_window, text='Save', command=self.save_edited_employee)
            self.save_button.pack()





    def update_employee_listbox(self):
        employees = self.show_employees()
        self.list_box.delete(0, tk.END)
        for employee in employees:
            self.list_box.insert(tk.END, f'ID: {employee[0]}, Name: {employee[1]} {employee[2]}, Phone: {employee[3]}')


    def open_add_employee_window(self):
        self.add_employee_window = tk.Toplevel(self.root)
        self.add_employee_window.title('Add employee')

        self.first_name_label = tk.Label(self.add_employee_window, text='Name:')
        self.first_name_label.pack()
        self.first_name_entry = tk.Entry(self.add_employee_window)
        self.first_name_entry.pack()

        self.last_name_label = tk.Label(self.add_employee_window, text='Surname:')
        self.last_name_label.pack()
        self.last_name_entry = tk.Entry(self.add_employee_window)
        self.last_name_entry.pack()

        self.phone_label = tk.Label(self.add_employee_window, text='Phone:')
        self.phone_label.pack()
        self.phone_entry = tk.Entry(self.add_employee_window)
        self.phone_entry.pack()

        self.save_button = tk.Button(self.add_employee_window, text='Save', command=self.save_employee)
        self.save_button.pack()


    def save_edited_employee(self):
        pass

    def save_employee(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        if first_name and last_name and phone:
            self.add_employee(first_name, last_name, phone)
            self.add_employee_window.destroy()
            self.update_employee_listbox()
        else:
            messagebox.showerror('Error', 'Enter all info!')



if __name__ == '__main__':
    root = tk.Tk()
    app = EmployeeApp(root=root)
    root.mainloop()


