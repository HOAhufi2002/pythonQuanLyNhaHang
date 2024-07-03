import tkinter as tk
from tkinter import ttk, simpledialog
from tkinter import messagebox
from utils.db import get_db_connection
import decimal
import datetime

class OrderPlacementTab:
    def __init__(self, tabControl, account_id, orders_tab):
        self.account_id = account_id  # Lưu trữ ID tài khoản
        self.orders_tab = orders_tab  # Tham chiếu đến OrdersTab để làm mới
        self.frame = ttk.Frame(tabControl)
        tabControl.add(self.frame, text='Đặt hàng')
        self.create_widgets()
        self.load_menu_items()

    def create_widgets(self):
        self.menu_tree = ttk.Treeview(self.frame, columns=('ID', 'Category', 'ItemName', 'Description', 'Price', 'Quantity'), show='headings', selectmode='extended')
        self.menu_tree.heading('ID', text='ID')
        self.menu_tree.heading('Category', text='Loại')
        self.menu_tree.heading('ItemName', text='Tên món')
        self.menu_tree.heading('Description', text='Mô tả')
        self.menu_tree.heading('Price', text='Giá')
        self.menu_tree.heading('Quantity', text='Số lượng')

        self.menu_tree.column('ID', width=30)
        self.menu_tree.column('Category', width=100)
        self.menu_tree.column('ItemName', width=150)
        self.menu_tree.column('Description', width=250)
        self.menu_tree.column('Price', width=70)
        self.menu_tree.column('Quantity', width=70)

        self.menu_tree.pack(expand=True, fill='both')

        self.form_frame = ttk.Frame(self.frame)
        self.form_frame.pack(pady=10)

        ttk.Label(self.form_frame, text="Tên khách hàng:").grid(row=0, column=0, padx=5, pady=5)
        self.customername_entry = ttk.Entry(self.form_frame)
        self.customername_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Số điện thoại:").grid(row=1, column=0, padx=5, pady=5)
        self.phonenumber_entry = ttk.Entry(self.form_frame)
        self.phonenumber_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Phương thức thanh toán:").grid(row=2, column=0, padx=5, pady=5)
        self.paymentmethod_combobox = ttk.Combobox(self.form_frame, values=["Tiền mặt", "Thẻ tín dụng", "Ví điện tử"])
        self.paymentmethod_combobox.grid(row=2, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.form_frame, text="Thêm đơn hàng", command=self.add_order)
        self.add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def load_menu_items(self):
        for row in self.menu_tree.get_children():
            self.menu_tree.delete(row)

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM MenuItems WHERE IsDeleted = 0")
        rows = cursor.fetchall()
        for row in rows:
            formatted_row = (row[0], row[1], row[2], row[3], str(row[4]), '0')  # default quantity is 0
            self.menu_tree.insert('', 'end', values=formatted_row)
        connection.close()

        self.menu_tree.bind('<ButtonRelease-1>', self.edit_quantity)

    def edit_quantity(self, event):
        selected_item = self.menu_tree.focus()
        if selected_item:
            values = self.menu_tree.item(selected_item, 'values')
            quantity = simpledialog.askstring("Nhập số lượng", f"Nhập số lượng cho {values[2]}", initialvalue=values[5])
            if quantity is not None:
                self.menu_tree.item(selected_item, values=(values[0], values[1], values[2], values[3], values[4], quantity))

    def add_order(self):
        customername = self.customername_entry.get()
        phonenumber = self.phonenumber_entry.get()
        paymentmethod = self.paymentmethod_combobox.get()
        orderdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        selected_items = [self.menu_tree.item(item, 'values') for item in self.menu_tree.get_children() if int(self.menu_tree.item(item, 'values')[5]) > 0]

        if customername and phonenumber and paymentmethod and selected_items:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # Thêm khách hàng vào bảng Customers
            cursor.execute("INSERT INTO Customers (CustomerName, PhoneNumber, IsDeleted) VALUES (?, ?, 0)",
                           (customername, phonenumber))
            cursor.execute("SELECT IDENT_CURRENT('Customers')")
            customer_id = cursor.fetchone()[0]

            # Thêm đơn hàng vào bảng Orders
            cursor.execute("INSERT INTO Orders (AccountID, OrderDate, TotalAmount, IsDeleted, CustomerID) VALUES (?, ?, ?, 0, ?)", 
                           (self.account_id, orderdate, decimal.Decimal(0), customer_id))
            cursor.execute("SELECT IDENT_CURRENT('Orders')")
            order_id = cursor.fetchone()[0]

            total_amount = 0
            for item in selected_items:
                item_id, category, itemname, description, price, quantity = item
                cursor.execute("INSERT INTO OrderDetails (OrderID, MenuItemID, Quantity, Price, IsDeleted) VALUES (?, ?, ?, ?, 0)", 
                               (order_id, item_id, int(quantity), decimal.Decimal(price)))
                total_amount += decimal.Decimal(price) * int(quantity)
                
                # Thêm vào KitchenFunctions
                cursor.execute("INSERT INTO KitchenFunctions (OrderID, Status, StartTime, EndTime, IsDeleted) VALUES (?, ?, ?, ?, 0)", 
                               (order_id, 'Pending', None, None))

            cursor.execute("UPDATE Orders SET TotalAmount = ? WHERE ID = ?", (total_amount, order_id))

            # Thêm vào bảng Payments
            cursor.execute("INSERT INTO Payments (OrderID, PaymentDate, Amount, PaymentMethod, IsDeleted) VALUES (?, ?, ?, ?, 0)",
                           (order_id, orderdate, total_amount, paymentmethod))

            connection.commit()
            connection.close()
            self.load_menu_items()
            messagebox.showinfo("Thông báo", "Đơn hàng đã được thêm thành công!")
            
            # Làm mới tab Orders
            self.orders_tab.load_orders()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin và chọn ít nhất một món ăn")
