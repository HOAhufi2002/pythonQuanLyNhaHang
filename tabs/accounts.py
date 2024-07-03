import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.db import get_db_connection
from tabs.orders import OrdersTab

class AccountsTab:
    def __init__(self, tabControl):
        self.frame = ttk.Frame(tabControl)
        tabControl.add(self.frame, text='Tài khoản')
        self.create_widgets()
        self.load_accounts()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Username', 'FullName', 'Email', 'Role'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Username', text='Tên đăng nhập')
        self.tree.heading('FullName', text='Họ tên')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Role', text='Quyền')

        self.tree.column('ID', width=30)
        self.tree.column('Username', width=100)
        self.tree.column('FullName', width=150)
        self.tree.column('Email', width=150)
        self.tree.column('Role', width=100)

        self.tree.pack(expand=True, fill='both')

        self.form_frame = ttk.Frame(self.frame)
        self.form_frame.pack(pady=10)

        ttk.Label(self.form_frame, text="Tên đăng nhập:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(self.form_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(self.form_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Họ tên:").grid(row=2, column=0, padx=5, pady=5)
        self.fullname_entry = ttk.Entry(self.form_frame)
        self.fullname_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)
        self.email_entry = ttk.Entry(self.form_frame)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Quyền:").grid(row=4, column=0, padx=5, pady=5)
        self.role_combobox = ttk.Combobox(self.form_frame, values=["Admin", "Staff"])
        self.role_combobox.grid(row=4, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.form_frame, text="Thêm", command=self.add_account)
        self.add_button.grid(row=5, column=0, padx=5, pady=5)

        self.update_button = ttk.Button(self.form_frame, text="Sửa", command=self.update_account)
        self.update_button.grid(row=5, column=1, padx=5, pady=5)

        self.delete_button = ttk.Button(self.form_frame, text="Xóa", command=self.delete_account)
        self.delete_button.grid(row=5, column=2, padx=5, pady=5)

        self.tree.bind('<ButtonRelease-1>', self.select_item)

    def load_accounts(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT ID, Username, FullName, Email, Role FROM Accounts WHERE IsDeleted = 0")
        rows = cursor.fetchall()
        for row in rows:
            formatted_row = (row[0], row[1], row[2], row[3], row[4])
            self.tree.insert('', 'end', values=formatted_row)
        connection.close()

    def select_item(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, values[1])
            self.fullname_entry.delete(0, tk.END)
            self.fullname_entry.insert(0, values[2])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, values[3])
            self.role_combobox.set(values[4])

    def add_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        fullname = self.fullname_entry.get()
        email = self.email_entry.get()
        role = self.role_combobox.get()

        if username and password and fullname and email and role:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Accounts (Username, PasswordHash, FullName, Email, Role, IsDeleted) VALUES (?, ?, ?, ?, ?, 0)", 
                           (username, password, fullname, email, role))
            connection.commit()
            connection.close()
            self.load_accounts()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")

    def update_account(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[0]
            username = self.username_entry.get()
            password = self.password_entry.get()
            fullname = self.fullname_entry.get()
            email = self.email_entry.get()
            role = self.role_combobox.get()

            if username and fullname and email and role:
                connection = get_db_connection()
                cursor = connection.cursor()
                if password:
                    cursor.execute("UPDATE Accounts SET Username = ?, PasswordHash = ?, FullName = ?, Email = ?, Role = ? WHERE ID = ?", 
                                   (username, password, fullname, email, role, item_id))
                else:
                    cursor.execute("UPDATE Accounts SET Username = ?, FullName = ?, Email = ?, Role = ? WHERE ID = ?", 
                                   (username, fullname, email, role, item_id))
                connection.commit()
                connection.close()
                self.load_accounts()
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")

    def delete_account(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[0]
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("UPDATE Accounts SET IsDeleted = 1 WHERE ID = ?", (item_id,))
            connection.commit()
            connection.close()
            self.load_accounts()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một tài khoản để xóa")
