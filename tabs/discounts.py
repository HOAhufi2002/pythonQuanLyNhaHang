import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.db import get_db_connection
import decimal
class DiscountsTab:
    def __init__(self, tabControl):
        self.frame = ttk.Frame(tabControl)
        tabControl.add(self.frame, text='Ưu đãi')
        self.create_widgets()
        self.load_discounts()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'DiscountCode', 'Description', 'DiscountAmount', 'ValidFrom', 'ValidTo'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('DiscountCode', text='Mã giảm giá')
        self.tree.heading('Description', text='Mô tả')
        self.tree.heading('DiscountAmount', text='Số tiền giảm')
        self.tree.heading('ValidFrom', text='Hiệu lực từ')
        self.tree.heading('ValidTo', text='Hiệu lực đến')

        self.tree.column('ID', width=30)
        self.tree.column('DiscountCode', width=100)
        self.tree.column('Description', width=200)
        self.tree.column('DiscountAmount', width=100)
        self.tree.column('ValidFrom', width=150)
        self.tree.column('ValidTo', width=150)

        self.tree.pack(expand=True, fill='both')

        self.form_frame = ttk.Frame(self.frame)
        self.form_frame.pack(pady=10)

        ttk.Label(self.form_frame, text="Mã giảm giá:").grid(row=0, column=0, padx=5, pady=5)
        self.discountcode_entry = ttk.Entry(self.form_frame)
        self.discountcode_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Mô tả:").grid(row=1, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(self.form_frame)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Số tiền giảm:").grid(row=2, column=0, padx=5, pady=5)
        self.discountamount_entry = ttk.Entry(self.form_frame)
        self.discountamount_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Hiệu lực từ:").grid(row=3, column=0, padx=5, pady=5)
        self.validfrom_entry = ttk.Entry(self.form_frame)
        self.validfrom_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Hiệu lực đến:").grid(row=4, column=0, padx=5, pady=5)
        self.validto_entry = ttk.Entry(self.form_frame)
        self.validto_entry.grid(row=4, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.form_frame, text="Thêm", command=self.add_discount)
        self.add_button.grid(row=5, column=0, padx=5, pady=5)

        self.update_button = ttk.Button(self.form_frame, text="Sửa", command=self.update_discount)
        self.update_button.grid(row=5, column=1, padx=5, pady=5)

        self.delete_button = ttk.Button(self.form_frame, text="Xóa", command=self.delete_discount)
        self.delete_button.grid(row=5, column=2, padx=5, pady=5)

        self.tree.bind('<ButtonRelease-1>', self.select_item)

    def load_discounts(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM DiscountsAndOffers WHERE IsDeleted = 0")
        rows = cursor.fetchall()
        for row in rows:
            formatted_row = (row[0], row[1], row[2], str(row[3]), row[4].strftime('%Y-%m-%d'), row[5].strftime('%Y-%m-%d'))
            self.tree.insert('', 'end', values=formatted_row)
        connection.close()

    def select_item(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.discountcode_entry.delete(0, tk.END)
            self.discountcode_entry.insert(0, values[1])
            self.description_entry.delete(0, tk.END)
            self.description_entry.insert(0, values[2])
            self.discountamount_entry.delete(0, tk.END)
            self.discountamount_entry.insert(0, values[3])
            self.validfrom_entry.delete(0, tk.END)
            self.validfrom_entry.insert(0, values[4])
            self.validto_entry.delete(0, tk.END)
            self.validto_entry.insert(0, values[5])

    def add_discount(self):
        discountcode = self.discountcode_entry.get()
        description = self.description_entry.get()
        discountamount = self.discountamount_entry.get()
        validfrom = self.validfrom_entry.get()
        validto = self.validto_entry.get()

        if discountcode and description and discountamount and validfrom and validto:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Discounts (DiscountCode, Description, DiscountAmount, ValidFrom, ValidTo, IsDeleted) VALUES (?, ?, ?, ?, ?, 0)", 
                           (discountcode, description, decimal.Decimal(discountamount), validfrom, validto))
            connection.commit()
            connection.close()
            self.load_discounts()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")

    def update_discount(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[0]
            discountcode = self.discountcode_entry.get()
            description = self.description_entry.get()
            discountamount = self.discountamount_entry.get()
            validfrom = self.validfrom_entry.get()
            validto = self.validto_entry.get()

            if discountcode and description and discountamount and validfrom and validto:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute("UPDATE Discounts SET DiscountCode = ?, Description = ?, DiscountAmount = ?, ValidFrom = ?, ValidTo = ? WHERE ID = ?", 
                               (discountcode, description, decimal.Decimal(discountamount), validfrom, validto, item_id))
                connection.commit()
                connection.close()
                self.load_discounts()
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")

    def delete_discount(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[0]
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("UPDATE Discounts SET IsDeleted = 1 WHERE ID = ?", (item_id,))
            connection.commit()
            connection.close()
            self.load_discounts()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục để xóa")
