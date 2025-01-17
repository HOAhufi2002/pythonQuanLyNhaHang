USE [nhahang]
GO
/****** Object:  Table [dbo].[Accounts]    Script Date: 03/07/2024 5:58:45 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Accounts](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Username] [nvarchar](50) NOT NULL,
	[PasswordHash] [nvarchar](256) NOT NULL,
	[FullName] [nvarchar](100) NULL,
	[Email] [nvarchar](100) NULL,
	[Role] [nvarchar](50) NULL,
	[IsDeleted] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Customers]    Script Date: 03/07/2024 5:58:46 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Customers](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[CustomerName] [nvarchar](100) NULL,
	[PhoneNumber] [nvarchar](15) NULL,
	[IsDeleted] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[DiscountsAndOffers]    Script Date: 03/07/2024 5:58:46 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[DiscountsAndOffers](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[DiscountCode] [nvarchar](50) NULL,
	[Description] [nvarchar](255) NULL,
	[DiscountAmount] [decimal](10, 2) NULL,
	[ValidFrom] [datetime] NULL,
	[ValidTo] [datetime] NULL,
	[IsDeleted] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[KitchenFunctions]    Script Date: 03/07/2024 5:58:46 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[KitchenFunctions](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[OrderID] [int] NULL,
	[Status] [nvarchar](50) NULL,
	[StartTime] [datetime] NULL,
	[EndTime] [datetime] NULL,
	[IsDeleted] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[MenuItems]    Script Date: 03/07/2024 5:58:46 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[MenuItems](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Category] [nvarchar](50) NULL,
	[ItemName] [nvarchar](100) NULL,
	[Description] [nvarchar](255) NULL,
	[Price] [decimal](10, 2) NULL,
	[IsDeleted] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[OrderDetails]    Script Date: 03/07/2024 5:58:46 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[OrderDetails](
	[OrderID] [int] NOT NULL,
	[MenuItemID] [int] NOT NULL,
	[Quantity] [int] NULL,
	[Price] [decimal](10, 2) NULL,
	[IsDeleted] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[OrderID] ASC,
	[MenuItemID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Orders]    Script Date: 03/07/2024 5:58:46 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Orders](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[AccountID] [int] NULL,
	[OrderDate] [datetime] NULL,
	[TotalAmount] [decimal](10, 2) NULL,
	[IsDeleted] [bit] NULL,
	[CustomerID] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Payments]    Script Date: 03/07/2024 5:58:46 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Payments](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[OrderID] [int] NULL,
	[PaymentDate] [datetime] NULL,
	[Amount] [decimal](10, 2) NULL,
	[PaymentMethod] [nvarchar](50) NULL,
	[IsDeleted] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Reports]    Script Date: 03/07/2024 5:58:46 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Reports](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[ReportName] [nvarchar](100) NULL,
	[ReportDate] [datetime] NULL,
	[ReportData] [nvarchar](max) NULL,
	[IsDeleted] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[Accounts] ON 

INSERT [dbo].[Accounts] ([ID], [Username], [PasswordHash], [FullName], [Email], [Role], [IsDeleted]) VALUES (1, N'admin', N'123', N'a', N'nguyenvana@example.com', N'Admin', 0)
INSERT [dbo].[Accounts] ([ID], [Username], [PasswordHash], [FullName], [Email], [Role], [IsDeleted]) VALUES (2, N'nv', N'123', N'b', N'lethib@example.com', N'Admin', 0)
INSERT [dbo].[Accounts] ([ID], [Username], [PasswordHash], [FullName], [Email], [Role], [IsDeleted]) VALUES (3, N'1', N'1', N'1', N'1', N'Staff', 1)
INSERT [dbo].[Accounts] ([ID], [Username], [PasswordHash], [FullName], [Email], [Role], [IsDeleted]) VALUES (4, N'a', N'a', N'a', N'a', N'Admin', 1)
INSERT [dbo].[Accounts] ([ID], [Username], [PasswordHash], [FullName], [Email], [Role], [IsDeleted]) VALUES (5, N'hoaminh', N'123', N'nguyen minh hoa', N'nguyenvana@example.com', N'Admin', 1)
INSERT [dbo].[Accounts] ([ID], [Username], [PasswordHash], [FullName], [Email], [Role], [IsDeleted]) VALUES (6, N'nhanvien1', N'nhanvien1', N'123', N'123@gmail.com', N'Staff', 1)
SET IDENTITY_INSERT [dbo].[Accounts] OFF
GO
SET IDENTITY_INSERT [dbo].[Customers] ON 

INSERT [dbo].[Customers] ([ID], [CustomerName], [PhoneNumber], [IsDeleted]) VALUES (2, N'1', N'1', 0)
INSERT [dbo].[Customers] ([ID], [CustomerName], [PhoneNumber], [IsDeleted]) VALUES (3, N'hoa', N'035380349', 0)
INSERT [dbo].[Customers] ([ID], [CustomerName], [PhoneNumber], [IsDeleted]) VALUES (4, N'hoa', N'035380349', 0)
INSERT [dbo].[Customers] ([ID], [CustomerName], [PhoneNumber], [IsDeleted]) VALUES (5, N'1', N'1', 0)
INSERT [dbo].[Customers] ([ID], [CustomerName], [PhoneNumber], [IsDeleted]) VALUES (6, N'1', N'1', 0)
INSERT [dbo].[Customers] ([ID], [CustomerName], [PhoneNumber], [IsDeleted]) VALUES (7, N'1', N'1', 0)
INSERT [dbo].[Customers] ([ID], [CustomerName], [PhoneNumber], [IsDeleted]) VALUES (8, N'1', N'1', 0)
INSERT [dbo].[Customers] ([ID], [CustomerName], [PhoneNumber], [IsDeleted]) VALUES (9, N'1', N'1', 0)
INSERT [dbo].[Customers] ([ID], [CustomerName], [PhoneNumber], [IsDeleted]) VALUES (10, N'Luân', N'035839092', 0)
INSERT [dbo].[Customers] ([ID], [CustomerName], [PhoneNumber], [IsDeleted]) VALUES (11, N'h', N'1', 0)
INSERT [dbo].[Customers] ([ID], [CustomerName], [PhoneNumber], [IsDeleted]) VALUES (12, N'Khach hang 1', N'035380342', 0)
SET IDENTITY_INSERT [dbo].[Customers] OFF
GO
SET IDENTITY_INSERT [dbo].[DiscountsAndOffers] ON 

INSERT [dbo].[DiscountsAndOffers] ([ID], [DiscountCode], [Description], [DiscountAmount], [ValidFrom], [ValidTo], [IsDeleted]) VALUES (1, N'Giam10', N'Gi?m 10% cho t?t c? don hàng', CAST(10000.00 AS Decimal(10, 2)), CAST(N'2024-07-01T00:00:00.000' AS DateTime), CAST(N'2024-07-31T00:00:00.000' AS DateTime), 0)
INSERT [dbo].[DiscountsAndOffers] ([ID], [DiscountCode], [Description], [DiscountAmount], [ValidFrom], [ValidTo], [IsDeleted]) VALUES (2, N'ChaoMung5', N'Gi?m 5% cho don hàng d?u tiên', CAST(5000.00 AS Decimal(10, 2)), CAST(N'2024-07-01T00:00:00.000' AS DateTime), CAST(N'2024-12-31T00:00:00.000' AS DateTime), 0)
INSERT [dbo].[DiscountsAndOffers] ([ID], [DiscountCode], [Description], [DiscountAmount], [ValidFrom], [ValidTo], [IsDeleted]) VALUES (3, N'MuaHe20', N'Gi?m 20% cho món d?c bi?t mùa hè', CAST(20000.00 AS Decimal(10, 2)), CAST(N'2024-06-01T00:00:00.000' AS DateTime), CAST(N'2024-08-31T00:00:00.000' AS DateTime), 0)
SET IDENTITY_INSERT [dbo].[DiscountsAndOffers] OFF
GO
SET IDENTITY_INSERT [dbo].[KitchenFunctions] ON 

INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (1, 1, N'Ðang chu?n b?', CAST(N'2024-07-03T03:26:26.870' AS DateTime), CAST(N'2024-07-03T03:56:26.870' AS DateTime), 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (2, 2, N'Ðã s?n sàng', CAST(N'2024-07-03T03:26:26.870' AS DateTime), CAST(N'2024-07-03T03:46:26.870' AS DateTime), 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (3, 5, N'Pending', NULL, NULL, 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (4, 6, N'Pending', NULL, NULL, 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (5, 6, N'Pending', NULL, NULL, 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (6, 7, N'Pending', NULL, NULL, 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (7, 8, N'Pending', NULL, NULL, 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (8, 8, N'Pending', NULL, NULL, 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (9, 9, N'Pending', NULL, NULL, 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (10, 10, N'Pending', NULL, NULL, 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (11, 11, N'Pending', NULL, NULL, 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (12, 11, N'Pending', NULL, NULL, 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (13, 12, N'Pending', NULL, NULL, 1)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (14, 12, N'Pending', NULL, NULL, 1)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (15, 13, N'In Progress', NULL, NULL, 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (16, 14, N'Pending', NULL, NULL, 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (17, 14, N'Pending', NULL, NULL, 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (18, 14, N'Pending', NULL, NULL, 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (19, 15, N'In Progress', NULL, NULL, 0)
INSERT [dbo].[KitchenFunctions] ([ID], [OrderID], [Status], [StartTime], [EndTime], [IsDeleted]) VALUES (20, 15, N'In Progress', NULL, NULL, 0)
SET IDENTITY_INSERT [dbo].[KitchenFunctions] OFF
GO
SET IDENTITY_INSERT [dbo].[MenuItems] ON 

INSERT [dbo].[MenuItems] ([ID], [Category], [ItemName], [Description], [Price], [IsDeleted]) VALUES (1, N'mon chinh', N'ga nuong', N'ga nuong mui ot', CAST(150000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[MenuItems] ([ID], [Category], [ItemName], [Description], [Price], [IsDeleted]) VALUES (2, N'mon khai vi', N'Salad Caesar', N'sa lad', CAST(70000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[MenuItems] ([ID], [Category], [ItemName], [Description], [Price], [IsDeleted]) VALUES (3, N'mon trang mieng 1', N'banh cheese', N'chess kem', CAST(55000.00 AS Decimal(10, 2)), 1)
INSERT [dbo].[MenuItems] ([ID], [Category], [ItemName], [Description], [Price], [IsDeleted]) VALUES (4, N'mon chinh', N'kaka', N'kakaa', CAST(300.00 AS Decimal(10, 2)), 1)
INSERT [dbo].[MenuItems] ([ID], [Category], [ItemName], [Description], [Price], [IsDeleted]) VALUES (5, N'mon trang mieng 1 1', N'banh cheese', N'chess kem', CAST(55000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[MenuItems] ([ID], [Category], [ItemName], [Description], [Price], [IsDeleted]) VALUES (6, N'mon trang mieng 1', N'banh kem 2', N'chess kem', CAST(55000.00 AS Decimal(10, 2)), 0)
SET IDENTITY_INSERT [dbo].[MenuItems] OFF
GO
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (1, 1, 2, CAST(300000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (2, 2, 1, CAST(70000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (2, 3, 3, CAST(165000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (5, 2, 1, CAST(70000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (6, 2, 1, CAST(70000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (6, 5, 1, CAST(55000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (7, 5, 1, CAST(55000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (8, 2, 1, CAST(70000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (8, 3, 1, CAST(55000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (9, 3, 1, CAST(55000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (10, 1, 1, CAST(150000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (11, 2, 1, CAST(70000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (11, 3, 1, CAST(55000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (12, 1, 1, CAST(150000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (12, 3, 1, CAST(55000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (13, 2, 2, CAST(70000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (14, 1, 1, CAST(150000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (14, 2, 1, CAST(70000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (14, 3, 1, CAST(55000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (15, 1, 2, CAST(150000.00 AS Decimal(10, 2)), 0)
INSERT [dbo].[OrderDetails] ([OrderID], [MenuItemID], [Quantity], [Price], [IsDeleted]) VALUES (15, 2, 1, CAST(70000.00 AS Decimal(10, 2)), 0)
GO
SET IDENTITY_INSERT [dbo].[Orders] ON 

INSERT [dbo].[Orders] ([ID], [AccountID], [OrderDate], [TotalAmount], [IsDeleted], [CustomerID]) VALUES (1, 1, CAST(N'2024-07-03T03:25:19.720' AS DateTime), CAST(120000.00 AS Decimal(10, 2)), 1, NULL)
INSERT [dbo].[Orders] ([ID], [AccountID], [OrderDate], [TotalAmount], [IsDeleted], [CustomerID]) VALUES (2, 2, CAST(N'2024-07-03T03:25:19.720' AS DateTime), CAST(85000.00 AS Decimal(10, 2)), 1, NULL)
INSERT [dbo].[Orders] ([ID], [AccountID], [OrderDate], [TotalAmount], [IsDeleted], [CustomerID]) VALUES (5, 1, CAST(N'2024-07-03T16:40:38.000' AS DateTime), CAST(70000.00 AS Decimal(10, 2)), 1, 2)
INSERT [dbo].[Orders] ([ID], [AccountID], [OrderDate], [TotalAmount], [IsDeleted], [CustomerID]) VALUES (6, 1, CAST(N'2024-07-03T16:44:40.000' AS DateTime), CAST(125000.00 AS Decimal(10, 2)), 1, 3)
INSERT [dbo].[Orders] ([ID], [AccountID], [OrderDate], [TotalAmount], [IsDeleted], [CustomerID]) VALUES (7, 1, CAST(N'2024-07-03T16:45:46.000' AS DateTime), CAST(55000.00 AS Decimal(10, 2)), 1, 4)
INSERT [dbo].[Orders] ([ID], [AccountID], [OrderDate], [TotalAmount], [IsDeleted], [CustomerID]) VALUES (8, 1, CAST(N'2024-07-03T16:46:25.000' AS DateTime), CAST(125000.00 AS Decimal(10, 2)), 1, 5)
INSERT [dbo].[Orders] ([ID], [AccountID], [OrderDate], [TotalAmount], [IsDeleted], [CustomerID]) VALUES (9, 1, CAST(N'2024-07-03T16:46:54.000' AS DateTime), CAST(55000.00 AS Decimal(10, 2)), 1, 6)
INSERT [dbo].[Orders] ([ID], [AccountID], [OrderDate], [TotalAmount], [IsDeleted], [CustomerID]) VALUES (10, 1, CAST(N'2024-07-03T16:59:21.000' AS DateTime), CAST(150000.00 AS Decimal(10, 2)), 1, 7)
INSERT [dbo].[Orders] ([ID], [AccountID], [OrderDate], [TotalAmount], [IsDeleted], [CustomerID]) VALUES (11, 1, CAST(N'2024-07-03T17:00:06.000' AS DateTime), CAST(125000.00 AS Decimal(10, 2)), 1, 8)
INSERT [dbo].[Orders] ([ID], [AccountID], [OrderDate], [TotalAmount], [IsDeleted], [CustomerID]) VALUES (12, 1, CAST(N'2024-07-03T17:00:33.000' AS DateTime), CAST(205000.00 AS Decimal(10, 2)), 1, 9)
INSERT [dbo].[Orders] ([ID], [AccountID], [OrderDate], [TotalAmount], [IsDeleted], [CustomerID]) VALUES (13, 1, CAST(N'2024-07-03T17:14:41.000' AS DateTime), CAST(140000.00 AS Decimal(10, 2)), 0, 10)
INSERT [dbo].[Orders] ([ID], [AccountID], [OrderDate], [TotalAmount], [IsDeleted], [CustomerID]) VALUES (14, 1, CAST(N'2024-07-03T17:17:59.000' AS DateTime), CAST(275000.00 AS Decimal(10, 2)), 0, 11)
INSERT [dbo].[Orders] ([ID], [AccountID], [OrderDate], [TotalAmount], [IsDeleted], [CustomerID]) VALUES (15, 1, CAST(N'2024-07-03T17:45:21.000' AS DateTime), CAST(370000.00 AS Decimal(10, 2)), 0, 12)
SET IDENTITY_INSERT [dbo].[Orders] OFF
GO
SET IDENTITY_INSERT [dbo].[Payments] ON 

INSERT [dbo].[Payments] ([ID], [OrderID], [PaymentDate], [Amount], [PaymentMethod], [IsDeleted]) VALUES (1, 1, CAST(N'2024-07-03T03:25:54.237' AS DateTime), CAST(120000.00 AS Decimal(10, 2)), N'Th? tín d?ng', 0)
INSERT [dbo].[Payments] ([ID], [OrderID], [PaymentDate], [Amount], [PaymentMethod], [IsDeleted]) VALUES (2, 2, CAST(N'2024-07-03T03:25:54.237' AS DateTime), CAST(85000.00 AS Decimal(10, 2)), N'Ti?n m?t', 0)
INSERT [dbo].[Payments] ([ID], [OrderID], [PaymentDate], [Amount], [PaymentMethod], [IsDeleted]) VALUES (3, 5, CAST(N'2024-07-03T16:40:38.000' AS DateTime), CAST(70000.00 AS Decimal(10, 2)), N'Thẻ tín dụng', 0)
INSERT [dbo].[Payments] ([ID], [OrderID], [PaymentDate], [Amount], [PaymentMethod], [IsDeleted]) VALUES (4, 6, CAST(N'2024-07-03T16:44:40.000' AS DateTime), CAST(125000.00 AS Decimal(10, 2)), N'Tiền mặt', 0)
INSERT [dbo].[Payments] ([ID], [OrderID], [PaymentDate], [Amount], [PaymentMethod], [IsDeleted]) VALUES (5, 7, CAST(N'2024-07-03T16:45:46.000' AS DateTime), CAST(55000.00 AS Decimal(10, 2)), N'Tiền mặt', 0)
INSERT [dbo].[Payments] ([ID], [OrderID], [PaymentDate], [Amount], [PaymentMethod], [IsDeleted]) VALUES (6, 8, CAST(N'2024-07-03T16:46:25.000' AS DateTime), CAST(125000.00 AS Decimal(10, 2)), N'Thẻ tín dụng', 0)
INSERT [dbo].[Payments] ([ID], [OrderID], [PaymentDate], [Amount], [PaymentMethod], [IsDeleted]) VALUES (7, 9, CAST(N'2024-07-03T16:46:54.000' AS DateTime), CAST(55000.00 AS Decimal(10, 2)), N'Thẻ tín dụng', 0)
INSERT [dbo].[Payments] ([ID], [OrderID], [PaymentDate], [Amount], [PaymentMethod], [IsDeleted]) VALUES (8, 10, CAST(N'2024-07-03T16:59:21.000' AS DateTime), CAST(150000.00 AS Decimal(10, 2)), N'Tiền mặt', 0)
INSERT [dbo].[Payments] ([ID], [OrderID], [PaymentDate], [Amount], [PaymentMethod], [IsDeleted]) VALUES (9, 11, CAST(N'2024-07-03T17:00:06.000' AS DateTime), CAST(125000.00 AS Decimal(10, 2)), N'Tiền mặt', 0)
INSERT [dbo].[Payments] ([ID], [OrderID], [PaymentDate], [Amount], [PaymentMethod], [IsDeleted]) VALUES (10, 12, CAST(N'2024-07-03T17:00:33.000' AS DateTime), CAST(205000.00 AS Decimal(10, 2)), N'Thẻ tín dụng', 1)
INSERT [dbo].[Payments] ([ID], [OrderID], [PaymentDate], [Amount], [PaymentMethod], [IsDeleted]) VALUES (11, 13, CAST(N'2024-07-03T17:14:41.000' AS DateTime), CAST(140000.00 AS Decimal(10, 2)), N'Thẻ tín dụng', 0)
INSERT [dbo].[Payments] ([ID], [OrderID], [PaymentDate], [Amount], [PaymentMethod], [IsDeleted]) VALUES (12, 14, CAST(N'2024-07-03T17:17:59.000' AS DateTime), CAST(275000.00 AS Decimal(10, 2)), N'Tiền mặt', 0)
INSERT [dbo].[Payments] ([ID], [OrderID], [PaymentDate], [Amount], [PaymentMethod], [IsDeleted]) VALUES (13, 15, CAST(N'2024-07-03T17:45:21.000' AS DateTime), CAST(370000.00 AS Decimal(10, 2)), N'Tiền mặt', 0)
SET IDENTITY_INSERT [dbo].[Payments] OFF
GO
SET IDENTITY_INSERT [dbo].[Reports] ON 

INSERT [dbo].[Reports] ([ID], [ReportName], [ReportDate], [ReportData], [IsDeleted]) VALUES (1, N'Báo cáo bán hàng hàng tháng', CAST(N'2024-07-03T03:26:10.050' AS DateTime), N'D? li?u bán hàng trong tháng', 0)
INSERT [dbo].[Reports] ([ID], [ReportName], [ReportDate], [ReportData], [IsDeleted]) VALUES (2, N'Báo cáo t?n kho', CAST(N'2024-07-03T03:26:10.050' AS DateTime), N'Tình tr?ng t?n kho hi?n t?i', 0)
INSERT [dbo].[Reports] ([ID], [ReportName], [ReportDate], [ReportData], [IsDeleted]) VALUES (3, N'Hi?u su?t nhân viên', CAST(N'2024-07-03T03:26:10.050' AS DateTime), N'Ch? s? hi?u su?t c?a nhân viên', 0)
SET IDENTITY_INSERT [dbo].[Reports] OFF
GO
ALTER TABLE [dbo].[Accounts] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[Customers] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[DiscountsAndOffers] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[KitchenFunctions] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[MenuItems] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[OrderDetails] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[Orders] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[Payments] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[Reports] ADD  DEFAULT ((0)) FOR [IsDeleted]
GO
ALTER TABLE [dbo].[KitchenFunctions]  WITH CHECK ADD FOREIGN KEY([OrderID])
REFERENCES [dbo].[Orders] ([ID])
GO
ALTER TABLE [dbo].[OrderDetails]  WITH CHECK ADD FOREIGN KEY([MenuItemID])
REFERENCES [dbo].[MenuItems] ([ID])
GO
ALTER TABLE [dbo].[OrderDetails]  WITH CHECK ADD FOREIGN KEY([OrderID])
REFERENCES [dbo].[Orders] ([ID])
GO
ALTER TABLE [dbo].[Orders]  WITH CHECK ADD FOREIGN KEY([AccountID])
REFERENCES [dbo].[Accounts] ([ID])
GO
ALTER TABLE [dbo].[Orders]  WITH CHECK ADD  CONSTRAINT [FK_Orders_Customers] FOREIGN KEY([CustomerID])
REFERENCES [dbo].[Customers] ([ID])
GO
ALTER TABLE [dbo].[Orders] CHECK CONSTRAINT [FK_Orders_Customers]
GO
ALTER TABLE [dbo].[Payments]  WITH CHECK ADD FOREIGN KEY([OrderID])
REFERENCES [dbo].[Orders] ([ID])
GO
ALTER TABLE [dbo].[Accounts]  WITH CHECK ADD CHECK  (([Role]='Staff' OR [Role]='Admin'))
GO
