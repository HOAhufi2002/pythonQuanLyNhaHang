import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.db import get_db_connection
import datetime
import csv

class OrdersTab:
    def __init__(self, tabControl):
        self.frame = ttk.Frame(tabControl)
        tabControl.add(self.frame, text='orders')
        self.create_widgets()
        self.load_orders()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'CustomerName', 'OrderDate', 'TotalAmount', 'PaymentMethod', 'PaymentDate', 'Status'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('CustomerName', text='Tên khách hàng')
        self.tree.heading('OrderDate', text='Ngày đặt hàng')
        self.tree.heading('TotalAmount', text='Tổng số tiền')
        self.tree.heading('PaymentMethod', text='Phương thức thanh toán')
        self.tree.heading('PaymentDate', text='Ngày thanh toán')
        self.tree.heading('Status', text='Trạng thái')

        self.tree.column('ID', width=30)
        self.tree.column('CustomerName', width=100)
        self.tree.column('OrderDate', width=150)
        self.tree.column('TotalAmount', width=100)
        self.tree.column('PaymentMethod', width=150)
        self.tree.column('PaymentDate', width=150)
        self.tree.column('Status', width=100)

        self.tree.pack(expand=True, fill='both')

        self.form_frame = ttk.Frame(self.frame)
        self.form_frame.pack(pady=10)

        ttk.Label(self.form_frame, text="Trạng thái:").grid(row=0, column=0, padx=5, pady=5)
        self.status_combobox = ttk.Combobox(self.form_frame, values=["Pending", "In Progress", "Completed"])
        self.status_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.update_button = ttk.Button(self.form_frame, text="Cập nhật trạng thái", command=self.update_order_status)
        self.update_button.grid(row=0, column=2, padx=5, pady=5)

        self.tree.bind('<ButtonRelease-1>', self.select_item)
        self.tree.bind('<Double-1>', self.show_order_details)
        self.load_orders()

    def load_orders(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT o.ID, c.CustomerName, o.OrderDate, o.TotalAmount, p.PaymentMethod, p.PaymentDate, k.Status
            FROM Orders o
            JOIN KitchenFunctions k ON o.ID = k.OrderID
            JOIN Payments p ON p.OrderID = o.ID
            JOIN Customers c ON c.ID = o.CustomerID
            WHERE o.IsDeleted = 0
        """)
        rows = cursor.fetchall()
        for row in rows:
            formatted_row = (row[0], row[1], row[2].strftime('%Y-%m-%d %H:%M:%S'), str(row[3]), row[4], row[5].strftime('%Y-%m-%d %H:%M:%S'), row[6])
            self.tree.insert('', 'end', values=formatted_row)
        connection.close()

    def select_item(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, 'values')
            self.status_combobox.set(values[6])

    def update_order_status(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[0]
            status = self.status_combobox.get()

            if status:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute("UPDATE KitchenFunctions SET Status = ? WHERE OrderID = ?", (status, item_id))
                connection.commit()
                connection.close()
                self.load_orders()
                messagebox.showinfo("Thông báo", "Cập nhật trạng thái thành công!")
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn trạng thái")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một đơn hàng")

    def show_order_details(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[0]

            details_window = tk.Toplevel(self.frame)
            details_window.title("Chi tiết hóa đơn")

            details_tree = ttk.Treeview(details_window, columns=('ItemName', 'Category', 'Description', 'Quantity', 'Price'), show='headings')
            details_tree.heading('ItemName', text='Tên món')
            details_tree.heading('Category', text='Loại')
            details_tree.heading('Description', text='Mô tả')
            details_tree.heading('Quantity', text='Số lượng')
            details_tree.heading('Price', text='Giá')

            details_tree.column('ItemName', width=150)
            details_tree.column('Category', width=100)
            details_tree.column('Description', width=250)
            details_tree.column('Quantity', width=100)
            details_tree.column('Price', width=100)

            details_tree.pack(expand=True, fill='both')

            export_button = ttk.Button(details_window, text="Xuất hóa đơn", command=lambda: self.export_invoice(item_id, details_tree))
            export_button.pack(pady=10)

            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT m.ItemName, m.Category, m.Description, od.Quantity, od.Price
                FROM OrderDetails od
                JOIN Orders o ON od.OrderID = o.ID
                JOIN MenuItems m ON m.ID = od.MenuItemID
                WHERE o.ID = ? AND o.IsDeleted = 0
            """, (item_id,))
            rows = cursor.fetchall()
            for row in rows:
                formatted_row = (row[0], row[1], row[2], row[3], str(row[4]))
                details_tree.insert('', 'end', values=formatted_row)
            connection.close()

    def export_invoice(self, order_id, details_tree):
        filename = f"invoice_{order_id}.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Tên món', 'Loại', 'Mô tả', 'Số lượng', 'Giá'])
            for row_id in details_tree.get_children():
                row = details_tree.item(row_id)['values']
                writer.writerow(row)
        messagebox.showinfo("Thông báo", f"Hóa đơn đã được xuất ra file {filename}")
