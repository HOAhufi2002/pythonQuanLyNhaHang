import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.db import get_db_connection
import decimal

class PaymentsTab:
    def __init__(self, tabControl):
        self.frame = ttk.Frame(tabControl)
        tabControl.add(self.frame, text='payment amount')
        self.create_widgets()
        self.load_payments()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'OrderID', 'PaymentDate', 'Amount', 'PaymentMethod'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('OrderID', text='ID đơn hàng')
        self.tree.heading('PaymentDate', text='Ngày thanh toán')
        self.tree.heading('Amount', text='Số tiền')
        self.tree.heading('PaymentMethod', text='Phương thức thanh toán')

        self.tree.column('ID', width=30)
        self.tree.column('OrderID', width=100)
        self.tree.column('PaymentDate', width=150)
        self.tree.column('Amount', width=100)
        self.tree.column('PaymentMethod', width=150)

        self.tree.pack(expand=True, fill='both')

        self.form_frame = ttk.Frame(self.frame)
        self.form_frame.pack(pady=10)

        ttk.Label(self.form_frame, text="ID đơn hàng:").grid(row=0, column=0, padx=5, pady=5)
        self.orderid_entry = ttk.Entry(self.form_frame)
        self.orderid_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Ngày thanh toán:").grid(row=1, column=0, padx=5, pady=5)
        self.paymentdate_entry = ttk.Entry(self.form_frame)
        self.paymentdate_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Số tiền:").grid(row=2, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.form_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Phương thức thanh toán:").grid(row=3, column=0, padx=5, pady=5)
        self.paymentmethod_entry = ttk.Entry(self.form_frame)
        self.paymentmethod_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.form_frame, text="Thêm", command=self.add_payment)
        self.add_button.grid(row=4, column=0, padx=5, pady=5)

        self.update_button = ttk.Button(self.form_frame, text="Sửa", command=self.update_payment)
        self.update_button.grid(row=4, column=1, padx=5, pady=5)

        self.delete_button = ttk.Button(self.form_frame, text="Xóa", command=self.delete_payment)
        self.delete_button.grid(row=4, column=2, padx=5, pady=5)

        self.tree.bind('<ButtonRelease-1>', self.select_item)

    def load_payments(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Payments WHERE IsDeleted = 0")
        rows = cursor.fetchall()
        for row in rows:
            formatted_row = (row[0], row[1], row[2].strftime('%Y-%m-%d %H:%M:%S'), str(row[3]), row[4])
            self.tree.insert('', 'end', values=formatted_row)
        connection.close()

    def select_item(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.orderid_entry.delete(0, tk.END)
            self.orderid_entry.insert(0, values[1])
            self.paymentdate_entry.delete(0, tk.END)
            self.paymentdate_entry.insert(0, values[2])
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, values[3])
            self.paymentmethod_entry.delete(0, tk.END)
            self.paymentmethod_entry.insert(0, values[4])

    def add_payment(self):
        orderid = self.orderid_entry.get()
        paymentdate = self.paymentdate_entry.get()
        amount = self.amount_entry.get()
        paymentmethod = self.paymentmethod_entry.get()

        if orderid and paymentdate and amount and paymentmethod:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Payments (OrderID, PaymentDate, Amount, PaymentMethod, IsDeleted) VALUES (?, ?, ?, ?, 0)", 
                           (orderid, paymentdate, decimal.Decimal(amount), paymentmethod))
            connection.commit()
            connection.close()
            self.load_payments()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")

    def update_payment(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[0]
            orderid = self.orderid_entry.get()
            paymentdate = self.paymentdate_entry.get()
            amount = self.amount_entry.get()
            paymentmethod = self.paymentmethod_entry.get()

            if orderid and paymentdate and amount and paymentmethod:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute("UPDATE Payments SET OrderID = ?, PaymentDate = ?, Amount = ?, PaymentMethod = ? WHERE ID = ?", 
                               (orderid, paymentdate, decimal.Decimal(amount), paymentmethod, item_id))
                connection.commit()
                connection.close()
                self.load_payments()
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")

    def delete_payment(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[0]
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("UPDATE Payments SET IsDeleted = 1 WHERE ID = ?", (item_id,))
            connection.commit()
            connection.close()
            self.load_payments()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một mục để xóa")
