import random
import sqlite3
from pathlib import Path

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.factory import Factory
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField

# Database / password checks (stubbed or your existing logic)
from .my_lib import DatabaseManager
from .secure_password import encrypt_password, check_password

Window.size = (440, 800)

class LoginScreenReal(Screen):
    current_user = None
    current_user_email = None
    current_user_type = None

    def try_login(self):
        """Example logic for user login check."""
        self.ids.passwd.error = False
        self.ids.passwd.helper_text = ""

        username = self.ids.uname.text
        password1 = self.ids.passwd.text
        query = f"SELECT * FROM user WHERE username='{username}'"
        db = DatabaseManager(name='login.sql')
        result = db.search(query)
        db.close()

        if len(result) == 1:
            # Suppose password is in column index 2
            hashed_pass = result[0][3]
            if check_password(user_password=password1, hashed_password=hashed_pass):
                LoginScreenReal.current_user = username
                LoginScreenReal.current_user_email = result[0][1]
                LoginScreenReal.current_user_type = result[0][4]
                # Go back to CartScreen if we were trying to check out
                if MainApp._return_to_cart:
                    MainApp._return_to_cart = False
                    self.manager.current = "CartScreen"
                else:
                    self.manager.current = "MainScreen"
                return

        # If invalid:
        self.ids.passwd.error = True
        self.ids.passwd.helper_text = "Invalid username or password"

class RegisterScreen(Screen):
    def register(self):
        """Simple example for user registration."""
        username = self.ids.username.text
        email = self.ids.email.text
        password = self.ids.password.text
        password2 = self.ids.confirm_password.text

        db = DatabaseManager(name="login.sql")

        # Check if user exists
        query = f"SELECT * FROM user WHERE username='{username}' OR email='{email}'"
        results = db.search(query)
        if results:
            self.ids.username.error = True
            self.ids.username.helper_text = "Username or email already exists"
            db.close()
            return

        # Check for empty fields
        if not username or not email or not password:
            self.ids.username.error = True
            self.ids.username.helper_text = "Please fill in all fields"
            db.close()
            return

        # Check password match
        if password != password2:
            self.ids.password.error = True
            self.ids.password.helper_text = "Passwords do not match"
            db.close()
            return

        # If OK, insert user
        insert_query = f"""
        INSERT INTO user(username, email, password)
        VALUES ('{username}', '{email}', '{encrypt_password(password)}');
        """
        db.run_save(query=insert_query)
        db.close()
        self.manager.current = "LoginScreen"

class LoginScreen(Screen):
    """Placeholder second login screen, if needed."""
    pass

class HeritageCategoryCard(Factory.MDCard):
    """Category card that acts like a button."""
    # We'll add a small method in the KV file that calls app.select_category(self)

class HeritageFoodCard(Factory.MDCard):
    """Pizza item card with 'Add to cart' button."""
    pass

class AddPizzaCard(Factory.MDCard):
    """Pizza item card with 'Add to cart' button."""
    pass

class OrderItemRow(MDCard):
    order_data = ListProperty()

    def __init__(self, order_data, **kwargs):
        # Convert the incoming order_data to a list and pad it if necessary
        padded_data = list(order_data)
        if len(padded_data) < 7:
            defaults = ["Unknown", "Unknown", "Unknown", "Unknown", 0, "Unknown", "Awaiting"]
            padded_data += defaults[len(padded_data):]
        # Pass the padded data to the parent initializer via kwargs
        kwargs["order_data"] = padded_data
        super().__init__(**kwargs)
        print("DEBUG: Order data:", self.order_data)
        self.menu = None

    def on_order_data(self, instance, value):
        # Ensure that any later updates to order_data are also padded correctly.
        if len(value) < 7:
            defaults = ["Unknown", "Unknown", "Unknown", "Unknown", 0, "Unknown", "Awaiting"]
            padded = list(value) + defaults[len(value):]
            # Only update if there’s a change to prevent recursion.
            if padded != value:
                self.order_data = padded

    def open_status_menu(self):
        if not self.menu:
            menu_items = [
                {
                    "text": "Awaiting",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x="Awaiting": self.set_status(x)
                },
                {
                    "text": "Done",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x="Done": self.set_status(x)
                },
            ]
            self.menu = MDDropdownMenu(
                caller=self.ids.status_dropdown,
                items=menu_items,
                width_mult=4,
            )
        self.menu.open()

    def set_status(self, new_status):
        self.ids.status_dropdown.text = new_status
        self.menu.dismiss()
        # Update the order status in the database using order_data[0] as order_id
        App.get_running_app().root.get_screen("AdminOrdersScreen").update_order_status(self.order_data[0], new_status)


class AdminOrdersScreen(Screen):
    def on_pre_enter(self, *args):
        self.load_orders()

    def load_orders(self):
        container = self.ids.orders_list
        container.clear_widgets()
        # Query orders sorted with newest first (assuming order_id autoincrements)
        db = DatabaseManager(name="orders.sql")
        query = """
            SELECT order_id, user_id, user_email, item_name, item_price, ticket_number, status 
            FROM orders 
            ORDER BY order_id DESC
        """
        orders = db.search(query)
        db.close()
        for order in orders:
            order_card = OrderItemRow(order_data=order)
            container.add_widget(order_card)

    def update_order_status(self, order_id, new_status):
        # Update the status in orders.sql and reload the orders list
        db = DatabaseManager(name="orders.sql")
        query = f"UPDATE orders SET status = '{new_status}' WHERE order_id = {order_id}"
        db.run_save(query)
        db.close()
        self.load_orders()

class MainScreen(Screen):

    def on_pre_enter(self, *args):
        """Populate the pizza list each time we navigate here."""
        self.add_pizza_dialog = None
        self.load_menu()


    def load_menu(self):
        # menu_items = [
        #     {
        #         "name": "Chorizo Fresh",
        #         "desc": "Spicy chicken chorizo, peppers, mozzarella, tomato sauce",
        #         "price": 295,
        #         "image": "pizza.png"
        #     },
        #     {
        #         "name": "Cheese",
        #         "desc": "Mozzarella, cheddar, parmesan, alfredo sauce",
        #         "price": 295,
        #         "image": "pizza.png"
        #     },
        #     {
        #         "name": "Ham and Cheese",
        #         "desc": "Ham, extra mozzarella, alfredo sauce",
        #         "price": 295,
        #         "image": "pizza.png"
        #     },
        #     {
        #         "name": "Double Chicken",
        #         "desc": "Double chicken, mozzarella, alfredo sauce",
        #         "price": 395,
        #         "image": "pizza.png"
        #     },
        # ]
        db = DatabaseManager(name="menu.sql")
        query = "SELECT name, description, price, image FROM menu"
        menu_items = db.search(query)
        db.close()
        print("DEBUG: Loading menu...")

        container = self.ids.menu_list
        container.clear_widgets()

        for name, description, price, image in menu_items:
            card = HeritageFoodCard()
            card.ids.pizza_name.text = name
            card.ids.pizza_desc.text = description
            card.ids.pizza_price.text = f"from {price} JPY"
            card.ids.pizza_image.source = image

            card.item_data = {
                "name": name,
                "desc": description,
                "price": price,
                "image": image,
                "quantity": 1,
                "size": "Medium 30cm"
            }
            # Attach a callback so tapping the card = "Add to Cart" flow
            card.bind(on_release=self.add_to_cart)
            container.add_widget(card)

        if LoginScreenReal.current_user_type == "admin":
            container.add_widget(AddPizzaCard())

        print("DEBUG: Loaded", len(container.children), "food cards")

    def show_add_pizza_dialog(self):
        """Show a pop-up dialog to add a new pizza."""
        if not self.add_pizza_dialog:
            self.pizza_name = MDTextField(hint_text="Pizza Name")
            self.pizza_desc = MDTextField(hint_text="Description")
            self.pizza_price = MDTextField(hint_text="Price", input_type="number")
            self.pizza_image = MDTextField(hint_text="Image Filename", text=f"{Path(__file__).parent}/assets/images/pizza.png")

            self.add_pizza_dialog = MDDialog(
                title="Add New Pizza",
                type="custom",
                content_cls=MDBoxLayout(
                    orientation="vertical",
                    spacing=10,
                    adaptive_height=True,
                ),
                buttons=[
                    MDRaisedButton(text="Cancel", on_release=lambda x: self.add_pizza_dialog.dismiss()),
                    MDRaisedButton(text="Add", on_release=self.add_pizza_to_db),
                ],
            )

            # Add input fields dynamically
            self.add_pizza_dialog.content_cls.add_widget(self.pizza_name)
            self.add_pizza_dialog.content_cls.add_widget(self.pizza_desc)
            self.add_pizza_dialog.content_cls.add_widget(self.pizza_price)
            self.add_pizza_dialog.content_cls.add_widget(self.pizza_image)

        self.add_pizza_dialog.open()

    def add_pizza_to_db(self, *args):
        """Insert new pizza into the database and refresh menu."""
        name = self.pizza_name.text.strip()
        description = self.pizza_desc.text.strip()
        price = self.pizza_price.text.strip()
        image = self.pizza_image.text.strip()

        if not name or not description or not price:
            return  # Don't allow empty fields

        db = DatabaseManager(name="menu.sql")
        query = f"""
        INSERT INTO menu (name, description, price, image)
        VALUES ('{name}', '{description}', {price}, '{image}')
        """
        db.run_save(query)
        db.close()

        self.load_menu()  # Refresh menu
        self.add_pizza_dialog.dismiss()



    def add_to_cart(self, card):
        app = MDApp.get_running_app()
        item = card.item_data.copy()  # copy the dict
        item["size"] = "Medium 30cm"
        item["quantity"] = 1
        app.cart.append(item)
        print("Added to cart:", item)

        # Update total in the corner
        self.update_total_button()

    def update_total_button(self):
        app = MDApp.get_running_app()
        total = sum(i["price"] * i["quantity"] for i in app.cart)
        self.ids.total_price_btn.text = f"{total} JPY"



class CartScreen(Screen):
    """Shows items in the cart and allows checkout."""
    def on_pre_enter(self, *args):
        self.refresh_cart()

    def refresh_cart(self):
        container = self.ids.cart_list
        container.clear_widgets()

        app = MDApp.get_running_app()
        total_price = 0
        for it in app.cart:
            total_price += it["price"] * it["quantity"]

        self.ids.cart_header.text = f"{len(app.cart)} items for {total_price} JPY"
        self.ids.checkout_btn.text = f"Proceed to checkout ({total_price} JPY)"

        for item in app.cart:
            row = Factory.CartItemRow()
            row.item_data = item
            row.ids.pizza_name.text = item["name"]
            row.ids.pizza_desc.text = item["size"]
            row.ids.pizza_price.text = f"{item['price'] * item['quantity']} JPY"
            row.ids.pizza_qty.text = str(item["quantity"])
            # row.ids.pizza_img.source = item["image"]
            container.add_widget(row)

    def update_cart_item(self, row, action):
        """Called when plus/minus or Change is pressed."""
        item = row.item_data
        if action == "minus" and item["quantity"] > 1:
            item["quantity"] -= 1
        elif action == "plus":
            item["quantity"] += 1
        elif action == "change":
            # Open size dialog
            content = Factory.SizeQuantityContent()
            content.ids.size_spinner.text = item["size"]
            content.ids.qty_spinner.text = str(item["quantity"])

            self.dialog = MDDialog(
                title=f"Change {item['name']}",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        text_color=(1, 0.4, 0, 1),
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="OK",
                        text_color=(1, 0.4, 0, 1),
                        on_release=lambda x: self.confirm_change(row, content)
                    )
                ]
            )
            self.dialog.open()
            return  # Don't refresh yet

        self.refresh_cart()

    def proceed_to_checkout(self):
        app = MDApp.get_running_app()
        # If user not logged in, prompt login
        if not LoginScreenReal.current_user:
            MainApp._return_to_cart = True
            self.manager.current = "LoginScreen"
            return

        # If logged in:
        # 1) Generate random 2-digit ticket number
        ticket_num = random.randint(10, 99)  # e.g. 27

        # 2) Save order to database
        db = sqlite3.connect("orders.sql")
        cursor = db.cursor()
        menu_db = sqlite3.connect("menu.sql")
        menu_cursor = menu_db.cursor()

        user_email = LoginScreenReal.current_user_email
        login_db = sqlite3.connect("login.sql")
        log_cursor = login_db.cursor()
        log_cursor.execute("SELECT id FROM user WHERE email=?", (user_email,))
        row = cursor.fetchone()
        login_db.close()
        user_id = row[0] if row else None  # fallback to 0 if not found


        for item in app.cart:
            menu_cursor.execute("SELECT price FROM menu WHERE name=?", (item["name"],))
            row = menu_cursor.fetchone()
            official_price = row[0] if row else item["price"]  # fallback to cart price if not found

            cursor.execute("""
                            INSERT INTO orders(user_id, user_email, item_name, item_price, ticket_number, status)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                user_id,
                user_email,
                item["name"],
                official_price,  # store official menu price
                f"#{ticket_num}",
                "Awaiting"
            ))

        db.commit()
        db.close()
        menu_db.close()

        # Clear cart
        app.cart.clear()

        # 3) Show checkout complete screen
        checkout_screen = self.manager.get_screen("CheckoutCompleteScreen")
        checkout_screen.ids.ticket_label.text = f"#{ticket_num}"
        self.manager.current = "CheckoutCompleteScreen"

    def add_extra_item(self, name, price):
        """Called when user taps an ExtraItemCard in 'Add to your order?'"""
        app = MDApp.get_running_app()
        item = {
            "name": name,
            "desc": "1 pcs",
            "price": price,
            "quantity": 1,
            "size": "",
            "image": ""
        }
        app.cart.append(item)
        self.refresh_cart()

    def confirm_change(self, row, content):
        size = content.ids.size_spinner.text
        qty = int(content.ids.qty_spinner.text)
        row.item_data["size"] = size
        row.item_data["quantity"] = qty
        self.dialog.dismiss()
        self.refresh_cart()

class CheckoutCompleteScreen(Screen):
    pass


class MainApp(MDApp):
    # We'll keep the cart in the app class
    cart = []
    # A flag to see if we need to return to the cart after login
    _return_to_cart = False
    add_pizza_dialog = None

    def build(self):
        self.create_database(query="""CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password VARCHAR(256),
            type TEXT DEFAULT 'user'
        );
        """, name="login.sql")
        path1= str(Path(__file__).parent) +"/assets/images/pizza.png"

        self.create_database("""CREATE TABLE IF NOT EXISTS menu(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE not null,
            description TEXT not null,
            price REAL not null,
            image TEXT DEFAULT path1
        );
        """, name="menu.sql")

        self.create_database(query="""CREATE TABLE IF NOT EXISTS orders(
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_email TEXT,
            item_name TEXT,
            item_price REAL,
            ticket_number TEXT,
            status TEXT DEFAULT 'Awaiting'
        );
        """, name="orders.sql")

        kv_path = self.get_kv_file_path()
        return Builder.load_file(kv_path)

    def get_kv_file_path(self):
        """Get the path to the pizza.kv file"""
        # First try current directory
        if Path("pizza.kv").exists():
            return "pizza.kv"

        # Then try package directory
        package_dir = Path(__file__).parent
        kv_file = package_dir / "pizza.kv"
        if kv_file.exists():
            return str(kv_file)

        # Fallback
        return "pizza.kv"

    def create_database(self, query, name):
        db = DatabaseManager(name=name)
        db.run_save(query=query)
        db.close()

    def on_start(self):
        # Go straight to main screen
        self.root.current = "MainScreen"

    def open_location(self):
        # Check if current user is admin; using LoginScreenReal.current_user_type
        if LoginScreenReal.current_user_type == "admin":
            self.root.current = "AdminOrdersScreen"
        else:
            # For non-admin users, you might show a location popup or do nothing.
            pass

    def select_category(self, card_widget):
        """Toggle categories to orange when pressed."""
        # Reset all categories to default
        cat_layout = card_widget.parent
        for c in cat_layout.children:
            c.md_bg_color = (0.15, 0.15, 0.15, 1)
        # Highlight the selected card
        card_widget.md_bg_color = (1, 0.4, 0, 1)



class SizeQuantityContent(MDBoxLayout):
    """Content for the 'size & quantity' dialog."""
    pass

def on_resize(instance, width, height):
    max_width, max_height = 440, 800
    if width > max_width or height > max_height:
        Window.size = (max_width, max_height)

Window.bind(on_resize=on_resize)

if __name__ == "__main__":
    MainApp().run()
