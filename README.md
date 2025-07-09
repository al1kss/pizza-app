# 🍕 Pizza Ordering App

A beautiful and intuitive pizza ordering application built with KivyMD. This app features a modern interface for browsing pizza menus, managing orders, and handling user authentication with admin capabilities. (maybe I will pitch this to one pizza place, thank you SHIPWRECKEDD!!)

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![KivyMD](https://img.shields.io/badge/kivymd-v1.2.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🎨 **Material Design Interface** - Beautiful, modern UI
- 👤 **User Authentication** - Secure login/registration system with encrypted password storage
- 🍕 **Interactive Pizza Menu** - Browse through various pizza options with detailed descriptions and prices
- 🛒 **Smart Shopping Cart** - Add items to cart, modify quantities, change sizes, and manage orders
- 📱 **Responsive Design** - Optimized for mobile and desktop viewing with touch-friendly controls
- 👑 **Admin Panel** - Admin users can manage orders, update status, and add new menu items
- 🎫 **Order Tracking** - Get unique ticket numbers and track order status (Awaiting/Done)
- 💾 **Local Database** - SQLite-based storage for users, menu items, and orders
- 🔒 **Secure Passwords** - SHA256 encryption for user password protection

## 🚀 Installation

Install the pizza ordering app using pip:

```bash
pip install pizza-ordering-app
```

## 🎮 Usage

After installation, start the app by running:

```bash
pizza-app
```

### 🔧 If Command Not Found

If you get `command not found: pizza-app`, try this:

```bash
# macOS/Linux - find your Python user bin directory
python -c "import site; print(site.USER_BASE + '/bin')"
# Then run: [that_path]/pizza-app
# For me it was: /Users/m24-009/Library/Python/3.9/bin/pizza-app
```

The app will automatically:
1. Create a `.pizza_app` directory in your home folder for storing data
2. Copy all necessary assets (images, database files) to this directory
3. Initialize the database with sample menu items
4. Launch the beautiful KivyMD application

## 🔐 Getting Started

### For Customers:
1. **Register** a new account or **login** with existing credentials
2. **Browse** the pizza menu with detailed descriptions and prices
3. **Add items** to your cart and customize sizes/quantities
4. **Checkout** securely and receive a unique ticket number
5. **Track** your order status

### For Administrators:
1. Login with admin credentials (default: `admin`/`secure_password`)
2. Access the **admin panel** via tapping the location button (hidden for security reasons)
3. **View and manage** all customer orders
4. **Update order status** from "Awaiting" to "Done"
5. **Add new menu items**, via scrolling all the way down in the menu ,with custom descriptions and prices

## 📋 System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: Automatically installed with the package
  - KivyMD 1.2.0+
  - Kivy 2.2.0+
  - Passlib 1.7.4+

## 🏗️ Development

If you want to modify or contribute to the app:

1. Clone the repository:
   ```bash
   git clone https://github.com/al1kss/pizza-app.git
   cd pizza-app
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

3. Make your changes and test:
   ```bash
   pizza-app
   ```

## 🗂️ Project Structure

```
pizza_app/
├── main.py              # Main application logic and screens
├── cli.py               # Command line entry point
├── pizza.kv             # KivyMD layout and styling
├── secure_password.py   # Password encryption utilities
├── my_lib.py           # Database management class
└── assets/
    ├── images/         # App images and icons
    └── databases/      # Database schema files
```

## 🎯 Key Features Breakdown

### 🛒 Shopping Experience
- **Dynamic Menu Loading**: Menu items loaded from database with real-time updates
- **Cart Management**: Add, remove, modify quantities and sizes
- **Size Options**: Multiple pizza sizes (Small, Medium, Large)
- **Price Calculation**: Real-time total calculation with tax

### 👨‍💼 Admin Features
- **Order Management**: View all orders sorted by newest first
- **Status Updates**: Change order status with dropdown menus
- **Menu Management**: Add new pizza items with custom pricing
- **User Management**: Handle user authentication and permissions

### 🔧 Technical Features
- **SQLite Integration**: Lightweight database for local storage
- **Password Security**: Industry-standard PBKDF2 SHA256 encryption
- **Path Handling**: Smart file path resolution for cross-platform compatibility
- **Asset Management**: Automatic copying and organization of app resources


## 🛠️ Troubleshooting

### App won't start?
```bash
pip install --upgrade kivymd kivy passlib
pizza-app
```

### Database issues?
The app automatically creates fresh databases on first run. If you encounter issues, delete the `~/.pizza_app` folder and restart.

### Missing dependencies?
```bash
pip install --upgrade pizza-ordering-app
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Alikhan Abdykaimov**
- Email: 2026.alikhan.abdykaimov@uwcisak.jp
- GitHub: [@al1kss](https://github.com/al1kss)
- Project: [pizza-app](https://github.com/al1kss/pizza-app)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 🐛 Issues & Support

If you encounter any issues or have questions:
1. Check the [GitHub Issues](https://github.com/al1kss/pizza-app/issues) page
2. Create a new issue with detailed description
3. Include your Python version and operating system

## 🙏 Acknowledgments

- Built with [KivyMD](https://kivymd.readthedocs.io/) - Material Design components for Kivy
- Uses [Kivy](https://kivy.org/) framework for cross-platform GUI development
- Password security powered by [Passlib](https://passlib.readthedocs.io/)

---

Made with ❤️ and 🍕 by Alikhan Abdykaimov application built with KivyMD. This app features a modern interface for browsing pizza menus, managing orders, and handling user authentication. Readme Generated with the help of AI. Thank you!
