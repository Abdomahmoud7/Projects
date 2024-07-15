import tkinter as tk
from tkinter import messagebox, ttk, VERTICAL, END
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkComboBox, CTkFrame, CTkImage
from PIL import Image
import pymysql


# Database
class Database:
    def __init__(self):
        self.connect_database()

    def connect_database(self):
        global mycursor, conn
        try:
            conn = pymysql.connect(host='localhost', user='root', password='1234')
            mycursor = conn.cursor()
        except:
            messagebox.showerror("Error", 'Something went wrong, Please open MySQL app before running again')
            return

        mycursor.execute('CREATE DATABASE IF NOT EXISTS employee_data')
        mycursor.execute('USE employee_data')
        mycursor.execute(
            'CREATE TABLE IF NOT EXISTS data (Id VARCHAR(20), Name VARCHAR(50), Phone VARCHAR(15), Role VARCHAR(50), Gender VARCHAR(20), Salary DECIMAL(10, 2))')

    def insert(self, id, name, phone, role, gender, salary):
        mycursor.execute('INSERT INTO data VALUES (%s, %s, %s, %s, %s, %s)',
                         (id, name, phone, role, gender, salary))
        conn.commit()

    def id_exists(self, id):
        mycursor.execute('SELECT COUNT(*) FROM data WHERE id=%s', id)
        result = mycursor.fetchone()
        return result[0] > 0

    def fetch_employees(self):
        mycursor.execute('SELECT * FROM data')
        result = mycursor.fetchall()
        return result

    def update(self, id, new_name, new_phone, new_role, new_gender, new_salary):
        mycursor.execute(
            'UPDATE data SET name=%s, phone=%s, role=%s, gender=%s, salary=%s WHERE id=%s',
            (new_name, new_phone, new_role, new_gender, new_salary, id))
        conn.commit()

    def delete(self, id):
        mycursor.execute('DELETE FROM data WHERE id=%s', id)
        conn.commit()

    def search(self, option, value):
        mycursor.execute(f'SELECT * FROM data WHERE {option}=%s', value)
        result = mycursor.fetchall()
        return result

    def deleteall_records(self):
        mycursor.execute('TRUNCATE TABLE data')
        conn.commit()

#Login
class LoginApp:
    def __init__(self, root, switch_app_callback):
        self.root = root
        self.switch_app_callback = switch_app_callback
        self.setup_login_ui()

    def setup_login_ui(self):
        self.root.title("Login Page")
        self.root.geometry("930x478")
        self.root.resizable(0, 0)
        image = CTkImage(Image.open(r"D:\Project Employee Management System\cover.jpg"), size=(930, 478))
        imageLabel = CTkLabel(self.root, image=image, text='')
        imageLabel.place(x=0, y=0)

        heading_label = CTkLabel(self.root, text="Employee Management System",
                                 bg_color="#FAFAFA", font=('Goudy Old Style', 20, 'bold'), text_color='dark blue')
        heading_label.place(x=20, y=100)

        self.username_entry = CTkEntry(self.root, placeholder_text='Enter Your Username', width=180)
        self.username_entry.place(x=50, y=150)

        self.password_entry = CTkEntry(self.root, placeholder_text='Enter Your Password', width=180, show='*')
        self.password_entry.place(x=50, y=200)

        login_button = CTkButton(self.root, text='Login', cursor='hand2', command=self.login)
        login_button.place(x=70, y=250)

    def login(self):
        if self.username_entry.get() == '' or self.password_entry.get() == '':
            messagebox.showerror('Error', 'All fields are required')
        elif self.username_entry.get() == 'abdo' and self.password_entry.get() == '1234':
            messagebox.showinfo('Success', 'Login is successful')
            self.switch_app_callback()
        else:
            messagebox.showerror('Error', 'Wrong credentials')

# Employee
class EMSApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.setup_ems_ui()

    def setup_ems_ui(self):
        self.root.title("Employee Management System")
        self.root.geometry('990x580+100+100')
        self.root.resizable(False, False)
        self.root.configure(fg_color='#161C30')
        logo = CTkImage(Image.open(r"D:\Project Employee Management System\cover2.png"), size=(990, 158))
        logoLabel = CTkLabel(self.root, image=logo, text='')
        logoLabel.grid(row=0, column=0, columnspan=2)

        self.left_frame = CTkFrame(self.root, fg_color='#161C30')
        self.left_frame.grid(row=1, column=0)

        self.setup_left_frame()

        self.right_frame = CTkFrame(self.root)
        self.right_frame.grid(row=1, column=1)

        self.setup_right_frame()

        self.button_frame = CTkFrame(self.root, fg_color='#161C30')
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.setup_button_frame()

        self.treeview_data()
        self.root.bind('<ButtonRelease>', self.selection)

    def setup_left_frame(self):
        id_label = CTkLabel(self.left_frame, text='Id', font=('arial', 18, 'bold'), text_color='white')
        id_label.grid(row=0, column=0, padx=20, pady=15, sticky='w')
        self.id_entry = CTkEntry(self.left_frame, font=('arial', 15, 'bold'), width=180)
        self.id_entry.grid(row=0, column=1)

        name_label = CTkLabel(self.left_frame, text='Name', font=('arial', 18, 'bold'), text_color='white')
        name_label.grid(row=1, column=0, padx=20, pady=15, sticky='w')
        self.name_entry = CTkEntry(self.left_frame, font=('arial', 15, 'bold'), width=180)
        self.name_entry.grid(row=1, column=1)

        phone_label = CTkLabel(self.left_frame, text='Phone', font=('arial', 18, 'bold'), text_color='white')
        phone_label.grid(row=2, column=0, padx=20, pady=15, sticky='w')
        self.phone_entry = CTkEntry(self.left_frame, font=('arial', 15, 'bold'), width=180)
        self.phone_entry.grid(row=2, column=1)

        role_label = CTkLabel(self.left_frame, text='Role', font=('arial', 18, 'bold'), text_color='white')
        role_label.grid(row=3, column=0, padx=20, pady=15, sticky='w')
        role_options = ['Web Developer', 'Cloud Architect', 'Technical Writer', 'Network Engineer', 'DevOps Engineer',
                        'Data Scientist', 'Business Analyst', 'IT Consultant', 'UX/UI Designer']

        self.role_box = CTkComboBox(self.left_frame, values=role_options, width=180,
                                    font=('arial', 15, 'bold'), state='readonly')
        self.role_box.grid(row=3, column=1)
        self.role_box.set(role_options[0])

        gender_label = CTkLabel(self.left_frame, text='Gender', font=('arial', 18, 'bold'), text_color='white')
        gender_label.grid(row=4, column=0, padx=20, pady=15, sticky='w')
        gender_options = ['Male', 'Female']
        self.gender_box = CTkComboBox(self.left_frame, values=gender_options, width=180,
                                      font=('arial', 15, 'bold'), state='readonly')
        self.gender_box.grid(row=4, column=1)
        self.gender_box.set(gender_options[0])

        salary_label = CTkLabel(self.left_frame, text='Salary', font=('arial', 18, 'bold'), text_color='white')
        salary_label.grid(row=5, column=0, padx=20, pady=15, sticky='w')
        self.salary_entry = CTkEntry(self.left_frame, font=('arial', 15, 'bold'), width=180)
        self.salary_entry.grid(row=5, column=1)

    def setup_right_frame(self):
        search_options = ['Id', 'Name', 'Phone', 'Role', 'Gender', 'Salary']
        self.search_box = CTkComboBox(self.right_frame, values=search_options, state='readonly')
        self.search_box.grid(row=0, column=0)
        self.search_box.set('Search By')

        self.search_entry = CTkEntry(self.right_frame)
        self.search_entry.grid(row=0, column=1)

        search_button = CTkButton(self.right_frame, text='Search', width=100, command=self.search_employee)
        search_button.grid(row=0, column=2)

        showall_button = CTkButton(self.right_frame, text='Show All', width=100, command=self.show_all)
        showall_button.grid(row=0, column=3, pady=5)

        self.tree = ttk.Treeview(self.right_frame, height=13)
        self.tree.grid(row=1, column=0, columnspan=4)

        self.tree['columns'] = ['Id', 'Name', 'Phone', 'Role', 'Gender', 'Salary']

        self.tree.heading('Id', text='Id')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Phone', text='Phone')
        self.tree.heading('Role', text='Role')
        self.tree.heading('Gender', text='Gender')
        self.tree.heading('Salary', text='Salary')

        self.tree.config(show='headings')

        self.tree.column('Id', width=100)
        self.tree.column('Name', width=160)
        self.tree.column('Phone', width=160)
        self.tree.column('Role', width=200)
        self.tree.column('Gender', width=100)
        self.tree.column('Salary', width=140)

        style = ttk.Style()
        style.configure('Treeview.Heading', font=('arial', 18, 'bold'))
        style.configure('Treeview', font=('arial', 15, 'bold'), rowheight=30, background='#161C30', foreground='white')

        scrollbar = ttk.Scrollbar(self.right_frame, orient=VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=1, column=4, sticky='ns')
        self.tree.config(yscrollcommand=scrollbar.set)

    def setup_button_frame(self):
        new_button = CTkButton(self.button_frame, text='New Employee', font=('arial', 15, 'bold'), width=160,
                               corner_radius=15, command=lambda: self.clear(True))
        new_button.grid(row=0, column=0, pady=5)

        add_button = CTkButton(self.button_frame, text='Add Employee', font=('arial', 15, 'bold'), width=160,
                               corner_radius=15, command=self.add_employee)
        add_button.grid(row=0, column=1, pady=5, padx=5)

        update_button = CTkButton(self.button_frame, text='Update Employee', font=('arial', 15, 'bold'), width=160,
                                  corner_radius=15, command=self.update_employee)
        update_button.grid(row=0, column=2, pady=5, padx=5)

        delete_button = CTkButton(self.button_frame, text='Delete Employee', font=('arial', 15, 'bold'), width=160,
                                  corner_radius=15, command=self.delete_employee)
        delete_button.grid(row=0, column=3, pady=5, padx=5)

        deleteall_button = CTkButton(self.button_frame, text='Delete All', font=('arial', 15, 'bold'), width=160,
                                     corner_radius=15, command=self.delete_all)
        deleteall_button.grid(row=0, column=4, pady=5, padx=5)

    def treeview_data(self):
        employees = self.db.fetch_employees()
        self.tree.delete(*self.tree.get_children())
        for employee in employees:
            self.tree.insert('', END, values=employee)

    def add_employee(self):
        if self.id_entry.get() == '' or self.phone_entry.get() == '' or self.name_entry.get() == '' or self.salary_entry.get() == '':
            messagebox.showerror("Error", 'All fields are required')
        elif self.db.id_exists(self.id_entry.get()):
            messagebox.showerror("Error", 'Id already exists')
        elif not self.id_entry.get().startswith('EMP'):
            messagebox.showerror('Error', "Invalid ID format. Use 'EMP' followed by a number (e.g., 'EMP1').")
        else:
            self.db.insert(self.id_entry.get(), self.name_entry.get(), self.phone_entry.get(),
                           self.role_box.get(), self.gender_box.get(), self.salary_entry.get())
            self.treeview_data()
            self.clear()
            messagebox.showinfo('Success', 'Data is added')

    def search_employee(self):
        if self.search_entry.get() == '':
            messagebox.showerror('Error', 'Enter value to search')
        elif self.search_box.get() == 'Search By':
            messagebox.showerror('Error', 'Please select an option')
        else:
            search_data = self.db.search(self.search_box.get(), self.search_entry.get())
            self.tree.delete(*self.tree.get_children())
            for employee in search_data:
                self.tree.insert('', END, values=employee)

    def delete_employee(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Select data to delete')
        else:
            self.db.delete(self.id_entry.get())
            self.treeview_data()
            self.clear()
            messagebox.showerror('Error', 'Data is deleted')

    def update_employee(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Select data to update')
        else:
            self.db.update(self.id_entry.get(), self.name_entry.get(), self.phone_entry.get(), self.role_box.get(),
                           self.gender_box.get(), self.salary_entry.get())
            self.treeview_data()
            self.clear()
            messagebox.showinfo('Success', 'Data is updated')

    def delete_all(self):
        result = messagebox.askyesno('Confirm', 'Do you really want to delete all the records?')
        if result:
            self.db.deleteall_records()
            self.treeview_data()

    def show_all(self):
        self.treeview_data()
        self.search_entry.delete(0, END)
        self.search_box.set('Search By')

    def selection(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear()
            self.id_entry.insert(0, row[0])
            self.name_entry.insert(0, row[1])
            self.phone_entry.insert(0, row[2])
            self.role_box.set(row[3])
            self.gender_box.set(row[4])
            self.salary_entry.insert(0, row[5])

    def clear(self, value=False):
        if value:
            self.tree.selection_remove(self.tree.focus())
        self.id_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.role_box.set('Web Developer')
        self.gender_box.set('Male')
        self.salary_entry.delete(0, END)


class MainApp:
    def __init__(self):
        self.root = CTk()
        self.db = Database()
        self.login_app = LoginApp(self.root, self.switch_to_ems)
        self.root.mainloop()

    def switch_to_ems(self):
        self.root.destroy()
        self.root = CTk()
        self.ems_app = EMSApp(self.root, self.db)
        self.root.mainloop()


if __name__ == "__main__":
    MainApp()
