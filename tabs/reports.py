import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.db import get_db_connection

class ReportsTab:
    def __init__(self, tabControl):
        self.frame = ttk.Frame(tabControl)
        tabControl.add(self.frame, text='Reports')
        self.create_widgets()
        self.load_reports()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'ReportName', 'CreatedDate', 'Content'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('ReportName', text='Tên báo cáo')
        self.tree.heading('CreatedDate', text='Ngày tạo')
        self.tree.heading('Content', text='Nội dung')

        self.tree.column('ID', width=30)
        self.tree.column('ReportName', width=150)
        self.tree.column('CreatedDate', width=150)
        self.tree.column('Content', width=300)

        self.tree.pack(expand=True, fill='both')

        self.form_frame = ttk.Frame(self.frame)
        self.form_frame.pack(pady=10)

        ttk.Label(self.form_frame, text="Tên báo cáo:").grid(row=0, column=0, padx=5, pady=5)
        self.reportname_entry = ttk.Entry(self.form_frame)
        self.reportname_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Ngày tạo:").grid(row=1, column=0, padx=5, pady=5)
        self.createddate_entry = ttk.Entry(self.form_frame)
        self.createddate_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Nội dung:").grid(row=2, column=0, padx=5, pady=5)
        self.content_entry = ttk.Entry(self.form_frame)
        self.content_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.form_frame, text="Thêm", command=self.add_report)
        self.add_button.grid(row=3, column=0, padx=5, pady=5)

        self.update_button = ttk.Button(self.form_frame, text="Sửa", command=self.update_report)
        self.update_button.grid(row=3, column=1, padx=5, pady=5)

        self.delete_button = ttk.Button(self.form_frame, text="Xóa", command=self.delete_report)
        self.delete_button.grid(row=3, column=2, padx=5, pady=5)

        self.tree.bind('<ButtonRelease-1>', self.select_item)

    def load_reports(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Reports WHERE IsDeleted = 0")
        rows = cursor.fetchall()
        for row in rows:
            formatted_row = (row[0], row[1], row[2].strftime('%Y-%m-%d %H:%M:%S'), row[3])
            self.tree.insert('', 'end', values=formatted_row)
        connection.close()

    def select_item(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.reportname_entry.delete(0, tk.END)
            self.reportname_entry.insert(0, values[1])
            self.createddate_entry.delete(0, tk.END)
            self.createddate_entry.insert(0, values[2])
            self.content_entry.delete(0, tk.END)
            self.content_entry.insert(0, values[3])

    def add_report(self):
        reportname = self.reportname_entry.get()
        createddate = self.createddate_entry.get()
        content = self.content_entry.get()

        if reportname and createddate and content:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Reports (ReportName, CreatedDate, Content, IsDeleted) VALUES (?, ?, ?, 0)", 
                           (reportname, createddate, content))
            connection.commit()
            connection.close()
            self.load_reports()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")

    def update_report(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[0]
            reportname = self.reportname_entry.get()
            createddate = self.createddate_entry.get()
            content = self.content_entry.get()

            if reportname and createddate and content:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute("UPDATE Reports SET ReportName = ?, CreatedDate = ?, Content = ? WHERE ID = ?", 
                               (reportname, createddate, content, item_id))
                connection.commit()
                connection.close()
                self.load_reports()
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")

    def delete_report(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[0]
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("UPDATE Reports SET IsDeleted = 1 WHERE ID = ?", (item_id,))
            connection.commit()
            connection.close()
            self.load_reports()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục để xóa")
