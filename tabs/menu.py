import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.db import get_db_connection
import decimal

class MenuTab:
    def __init__(self, tabControl):
        self.frame = ttk.Frame(tabControl)
        tabControl.add(self.frame, text='Menu Food')
        self.create_widgets()
        self.load_menu_items()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Category', 'ItemName', 'Description', 'Price'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Category', text='Loại')
        self.tree.heading('ItemName', text='Tên món')
        self.tree.heading('Description', text='Mô tả')
        self.tree.heading('Price', text='Giá')

        self.tree.column('ID', width=30)
        self.tree.column('Category', width=100)
        self.tree.column('ItemName', width=150)
        self.tree.column('Description', width=250)
        self.tree.column('Price', width=70)

        self.tree.pack(expand=True, fill='both')

        self.form_frame = ttk.Frame(self.frame)
        self.form_frame.pack(pady=10)

        ttk.Label(self.form_frame, text="Loại:").grid(row=0, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(self.form_frame)
        self.category_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Tên món:").grid(row=1, column=0, padx=5, pady=5)
        self.itemname_entry = ttk.Entry(self.form_frame)
        self.itemname_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Mô tả:").grid(row=2, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(self.form_frame)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Giá:").grid(row=3, column=0, padx=5, pady=5)
        self.price_entry = ttk.Entry(self.form_frame)
        self.price_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.form_frame, text="Thêm", command=self.add_menu_item)
        self.add_button.grid(row=4, column=0, padx=5, pady=5)

        self.update_button = ttk.Button(self.form_frame, text="Sửa", command=self.update_menu_item)
        self.update_button.grid(row=4, column=1, padx=5, pady=5)

        self.delete_button = ttk.Button(self.form_frame, text="Xóa", command=self.delete_menu_item)
        self.delete_button.grid(row=4, column=2, padx=5, pady=5)

        self.tree.bind('<ButtonRelease-1>', self.select_item)

    def load_menu_items(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM MenuItems WHERE IsDeleted = 0")
        rows = cursor.fetchall()
        for row in rows:
            formatted_row = (row[0], row[1], row[2], row[3], str(row[4]))
            self.tree.insert('', 'end', values=formatted_row)
        connection.close()

    def select_item(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, values[1])
            self.itemname_entry.delete(0, tk.END)
            self.itemname_entry.insert(0, values[2])
            self.description_entry.delete(0, tk.END)
            self.description_entry.insert(0, values[3])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, values[4])

    def add_menu_item(self):
        category = self.category_entry.get()
        itemname = self.itemname_entry.get()
        description = self.description_entry.get()
        price = self.price_entry.get()

        if category and itemname and description and price:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO MenuItems (Category, ItemName, Description, Price, IsDeleted) VALUES (?, ?, ?, ?, 0)", 
                           (category, itemname, description, decimal.Decimal(price)))
            connection.commit()
            connection.close()
            self.load_menu_items()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")

    def update_menu_item(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[0]
            category = self.category_entry.get()
            itemname = self.itemname_entry.get()
            description = self.description_entry.get()
            price = self.price_entry.get()

            if category and itemname and description and price:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute("UPDATE MenuItems SET Category = ?, ItemName = ?, Description = ?, Price = ? WHERE ID = ?", 
                               (category, itemname, description, decimal.Decimal(price), item_id))
                connection.commit()
                connection.close()
                self.load_menu_items()
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")

    def delete_menu_item(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[0]
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("UPDATE MenuItems SET IsDeleted = 1 WHERE ID = ?", (item_id,))
            connection.commit()
            connection.close()
            self.load_menu_items()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục để xóa")
