import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.db import get_db_connection

class KitchenTab:
    def __init__(self, tabControl):
        self.frame = ttk.Frame(tabControl)
        tabControl.add(self.frame, text='Kitchen Function')
        self.create_widgets()
        self.load_kitchen_tasks()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'TaskName', 'Description', 'Status', 'AssignedTo'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('TaskName', text='Tên công việc')
        self.tree.heading('Description', text='Mô tả')
        self.tree.heading('Status', text='Trạng thái')
        self.tree.heading('AssignedTo', text='Giao cho')

        self.tree.column('ID', width=30)
        self.tree.column('TaskName', width=150)
        self.tree.column('Description', width=300)
        self.tree.column('Status', width=100)
        self.tree.column('AssignedTo', width=100)

        self.tree.pack(expand=True, fill='both')

        self.form_frame = ttk.Frame(self.frame)
        self.form_frame.pack(pady=10)

        ttk.Label(self.form_frame, text="Tên công việc:").grid(row=0, column=0, padx=5, pady=5)
        self.taskname_entry = ttk.Entry(self.form_frame)
        self.taskname_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Mô tả:").grid(row=1, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(self.form_frame)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Trạng thái:").grid(row=2, column=0, padx=5, pady=5)
        self.status_entry = ttk.Entry(self.form_frame)
        self.status_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Giao cho:").grid(row=3, column=0, padx=5, pady=5)
        self.assignedto_entry = ttk.Entry(self.form_frame)
        self.assignedto_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.form_frame, text="Thêm", command=self.add_task)
        self.add_button.grid(row=4, column=0, padx=5, pady=5)

        self.update_button = ttk.Button(self.form_frame, text="Sửa", command=self.update_task)
        self.update_button.grid(row=4, column=1, padx=5, pady=5)

        self.delete_button = ttk.Button(self.form_frame, text="Xóa", command=self.delete_task)
        self.delete_button.grid(row=4, column=2, padx=5, pady=5)

        self.tree.bind('<ButtonRelease-1>', self.select_item)

    def load_kitchen_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM KitchenFunctions WHERE IsDeleted = 0")
        rows = cursor.fetchall()
        for row in rows:
            formatted_row = (row[0], row[1], row[2], row[3], row[4])
            self.tree.insert('', 'end', values=formatted_row)
        connection.close()

    def select_item(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.taskname_entry.delete(0, tk.END)
            self.taskname_entry.insert(0, values[1])
            self.description_entry.delete(0, tk.END)
            self.description_entry.insert(0, values[2])
            self.status_entry.delete(0, tk.END)
            self.status_entry.insert(0, values[3])
            self.assignedto_entry.delete(0, tk.END)
            self.assignedto_entry.insert(0, values[4])

    def add_task(self):
        taskname = self.taskname_entry.get()
        description = self.description_entry.get()
        status = self.status_entry.get()
        assignedto = self.assignedto_entry.get()

        if taskname and description and status and assignedto:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO KitchenFunctions (TaskName, Description, Status, AssignedTo, IsDeleted) VALUES (?, ?, ?, ?, 0)", 
                           (taskname, description, status, assignedto))
            connection.commit()
            connection.close()
            self.load_kitchen_tasks()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")

    def update_task(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[0]
            taskname = self.taskname_entry.get()
            description = self.description_entry.get()
            status = self.status_entry.get()
            assignedto = self.assignedto_entry.get()

            if taskname and description and status and assignedto:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute("UPDATE KitchenFunctions SET TaskName = ?, Description = ?, Status = ?, AssignedTo = ? WHERE ID = ?", 
                               (taskname, description, status, assignedto, item_id))
                connection.commit()
                connection.close()
                self.load_kitchen_tasks()
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")

    def delete_task(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[0]
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("UPDATE KitchenFunctions SET IsDeleted = 1 WHERE ID = ?", (item_id,))
            connection.commit()
            connection.close()
            self.load_kitchen_tasks()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục để xóa")
