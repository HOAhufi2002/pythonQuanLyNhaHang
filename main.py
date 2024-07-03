
from utils.db import get_db_connection
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tabs.accounts import AccountsTab
from tabs.orders import OrdersTab
from tabs.payments import PaymentsTab
from tabs.discounts import DiscountsTab
from tabs.reports import ReportsTab
from tabs.kitchen import KitchenTab
from tabs.menu import MenuTab
from tabs.order_placement import OrderPlacementTab  # Import tab mới
from tabs.statistics import StatisticsTab  # Import tab mới

class LoginRegisterFrame(ttk.Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.on_login_success = on_login_success
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        self.login_frame = ttk.Frame(self.notebook, style="Custom.TFrame")
        self.register_frame = ttk.Frame(self.notebook, style="Custom.TFrame")
        
        self.notebook.add(self.login_frame, text='Đăng nhập')
        self.notebook.add(self.register_frame, text='Đăng ký')

        self.create_login_widgets()
        self.create_register_widgets()

    def create_login_widgets(self):
        self.login_frame.config(style='Custom.TFrame')
        
        # Thêm logo
        logo_image = Image.open('assets/1.jpg')
        logo_image = logo_image.resize((100, 100), Image.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self.login_frame, image=self.logo_img, background='white')
        logo_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        login_canvas = tk.Canvas(self.login_frame, width=300, height=300, background='white', bd=0, highlightthickness=0)
        login_canvas.grid(row=1, column=0, rowspan=4, padx=20, pady=20)
        
        login_image = Image.open('assets/1.jpg')
        login_image = login_image.resize((300, 300), Image.LANCZOS)
        self.login_img = ImageTk.PhotoImage(login_image)
        login_canvas.create_image(0, 0, anchor=tk.NW, image=self.login_img)

        login_form_frame = ttk.Frame(self.login_frame, style='Custom.TFrame')
        login_form_frame.grid(row=1, column=1, rowspan=4, padx=20, pady=20)

        ttk.Label(login_form_frame, text="Tên đăng nhập:", font=('Helvetica', 12), background='white').grid(row=0, column=0, padx=10, pady=10)
        self.login_username = ttk.Entry(login_form_frame, font=('Helvetica', 12))
        self.login_username.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(login_form_frame, text="Mật khẩu:", font=('Helvetica', 12), background='white').grid(row=1, column=0, padx=10, pady=10)
        self.login_password = ttk.Entry(login_form_frame, show="*", font=('Helvetica', 12))
        self.login_password.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = ttk.Button(login_form_frame, text="Đăng nhập", command=self.check_login)
        self.login_button.grid(row=2, columnspan=2, padx=10, pady=20)

        self.login_message = ttk.Label(login_form_frame, text="", font=('Helvetica', 10), foreground='red', background='white')
        self.login_message.grid(row=3, columnspan=2, padx=10, pady=10)

    def create_register_widgets(self):
        self.register_frame.config(style='Custom.TFrame')

        logo_image = Image.open('assets/1.jpg')
        logo_image = logo_image.resize((100, 100), Image.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self.register_frame, image=self.logo_img, background='white')
        logo_label.pack(pady=(20, 10))

        register_form_frame = ttk.Frame(self.register_frame, style='Custom.TFrame')
        register_form_frame.pack(padx=20, pady=20)

        ttk.Label(register_form_frame, text="Tên đăng nhập:", font=('Helvetica', 12), background='white').grid(row=0, column=0, padx=10, pady=10)
        self.register_username = ttk.Entry(register_form_frame, font=('Helvetica', 12))
        self.register_username.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(register_form_frame, text="Mật khẩu:", font=('Helvetica', 12), background='white').grid(row=1, column=0, padx=10, pady=10)
        self.register_password = ttk.Entry(register_form_frame, show="*", font=('Helvetica', 12))
        self.register_password.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(register_form_frame, text="Họ tên:", font=('Helvetica', 12), background='white').grid(row=2, column=0, padx=10, pady=10)
        self.register_fullname = ttk.Entry(register_form_frame, font=('Helvetica', 12))
        self.register_fullname.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(register_form_frame, text="Email:", font=('Helvetica', 12), background='white').grid(row=3, column=0, padx=10, pady=10)
        self.register_email = ttk.Entry(register_form_frame, font=('Helvetica', 12))
        self.register_email.grid(row=3, column=1, padx=10, pady=10)

        self.register_button = ttk.Button(register_form_frame, text="Đăng ký", command=self.register_user)
        self.register_button.grid(row=4, columnspan=2, padx=10, pady=20)

        self.register_message = ttk.Label(register_form_frame, text="", font=('Helvetica', 10), foreground='green', background='white')
        self.register_message.grid(row=5, columnspan=2, padx=10, pady=10)

    def check_login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        user_role, account_id = self.authenticate(username, password)
        if user_role:
            self.on_login_success(user_role, account_id)
        else:
            self.login_message.config(text="Thông tin đăng nhập không hợp lệ, vui lòng thử lại.")

    def authenticate(self, username, password):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT Role, ID FROM Accounts WHERE Username = ? AND PasswordHash = ?", (username, password))
        user = cursor.fetchone()
        connection.close()
        return (user[0], user[1]) if user else (None, None)

    def register_user(self):
        username = self.register_username.get()
        password = self.register_password.get()
        fullname = self.register_fullname.get()
        email = self.register_email.get()

        if username and password and fullname and email:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Accounts (Username, PasswordHash, FullName, Email, Role) VALUES (?, ?, ?, ?, 'Staff')", 
                           (username, password, fullname, email))
            connection.commit()
            connection.close()
            self.register_message.config(text="Đăng ký thành công!")
        else:
            self.register_message.config(text="Vui lòng điền đầy đủ thông tin.", foreground='red')

class HorizonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Horizon Restaurant Management System")
        self.geometry("1000x600")
        self.style = ttk.Style(self)
        self.style.configure('Custom.TFrame', background='white')
        self.style.configure('Accent.TButton', font=('Helvetica', 12, 'bold'), background='#007BFF', foreground='#FFFFFF')
        self.show_login()

    def show_login(self):
        self.login_frame = LoginRegisterFrame(self, self.on_login_success)
        self.login_frame.pack(expand=True, fill="both")

    def on_login_success(self, user_role, account_id):
        self.login_frame.pack_forget()
        self.tabControl = ttk.Notebook(self)
        self.tabControl.pack(expand=1, fill="both")
        self.create_tabs(user_role, account_id)

    def create_tabs(self, user_role, account_id):
        if user_role == 'Admin':
            self.accounts_tab = AccountsTab(self.tabControl)
            self.payments_tab = PaymentsTab(self.tabControl)
            self.discounts_tab = DiscountsTab(self.tabControl)
            self.reports_tab = ReportsTab(self.tabControl)
            self.kitchen_tab = KitchenTab(self.tabControl)
            self.menu_tab = MenuTab(self.tabControl)
            self.statistics_tab = StatisticsTab(self.tabControl)  # Thêm tab thống kê

        self.orders_tab = OrdersTab(self.tabControl)
        self.order_placement_tab = OrderPlacementTab(self.tabControl, account_id, self.orders_tab)  # Thêm tab mới

if __name__ == "__main__":
    app = HorizonApp()
    app.mainloop()
