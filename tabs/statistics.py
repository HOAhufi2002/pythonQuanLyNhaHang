import tkinter as tk
from tkinter import ttk, messagebox  # Thêm import messagebox
from utils.db import get_db_connection
import matplotlib.pyplot as plt
class StatisticsTab:
    def __init__(self, tabControl):
        self.frame = ttk.Frame(tabControl)
        tabControl.add(self.frame, text='Statics')
        self.create_widgets()

    def create_widgets(self):
        self.sales_stats_button = ttk.Button(self.frame, text="Thống kê số lượng sản phẩm bán nhiều nhất", command=self.show_sales_statistics)
        self.sales_stats_button.pack(pady=10)

        self.stats_tree = ttk.Treeview(self.frame, columns=('Name', 'Value'), show='headings')
        self.stats_tree.heading('Name', text='Tên sản phẩm')
        self.stats_tree.heading('Value', text='Số lượng')
        self.stats_tree.column('Name', width=200)
        self.stats_tree.column('Value', width=100)
        self.stats_tree.pack(expand=True, fill='both')

        self.plot_button = ttk.Button(self.frame, text="Vẽ biểu đồ", command=self.plot_sales_statistics)
        self.plot_button.pack(pady=10)

    def show_sales_statistics(self):
        for row in self.stats_tree.get_children():
            self.stats_tree.delete(row)

        self.sales_data = []

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT m.ItemName, SUM(od.Quantity) AS TotalSold
            FROM OrderDetails od
            JOIN MenuItems m ON od.MenuItemID = m.ID
            JOIN Orders o ON od.OrderID = o.ID
            WHERE o.IsDeleted = 0
            GROUP BY m.ItemName
            ORDER BY TotalSold DESC
        """)
        rows = cursor.fetchall()
        for row in rows:
            self.stats_tree.insert('', 'end', values=(row[0], row[1]))
            self.sales_data.append((row[0], row[1]))
        connection.close()

    def plot_sales_statistics(self):
        if not hasattr(self, 'sales_data') or not self.sales_data:
            messagebox.showwarning("Cảnh báo", "Vui lòng xem thống kê trước khi vẽ biểu đồ")
            return

        names = [item[0] for item in self.sales_data]
        values = [item[1] for item in self.sales_data]

        plt.figure(figsize=(10, 6))
        plt.bar(names, values, color='skyblue')
        plt.xlabel('Tên sản phẩm')
        plt.ylabel('Số lượng bán')
        plt.title('Thống kê số lượng sản phẩm bán nhiều nhất')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
