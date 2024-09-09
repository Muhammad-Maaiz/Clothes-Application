from flet import *
from PIL import Image as PILImage
import io
import base64
from backend import *

def show_signup_page(page: Page):
    page.clean()

    def handle_signup(e):
        full_name = full_name_field.value
        username = username_field.value
        email = email_field.value
        password = password_field.value

        if not full_name or not username or not email or not password:
            page.snack_bar = SnackBar(Text("Please fill in all fields."), bgcolor=colors.RED)
            page.snack_bar.open = True
            page.update()
            return

        signup_result = user.signup(full_name, username, email, password)
        
        if signup_result == "email_exists":
            page.snack_bar = SnackBar(Text("Email already exists. Please use a different email."), bgcolor=colors.RED)
        elif signup_result == "password_exists":
            page.snack_bar = SnackBar(Text("Password already exists. Please choose a different password."), bgcolor=colors.RED)
        elif signup_result == "username_exists":
            page.snack_bar = SnackBar(Text("Username already exists. Please choose another."), bgcolor=colors.RED)
        else:
            page.snack_bar = SnackBar(Text("Sign up successful! Please log in."), bgcolor=colors.GREEN)
            show_login_page(page)

        page.snack_bar.open = True
        page.update()

    title_container = Container(
        content=ResponsiveRow(
            [
                Text(value="Welcome to ClothesVerve", style="headlineMedium", size=30, weight="bold", font_family="Lucida Handwriting", text_align="center", color=colors.WHITE)
            ],
            alignment=MainAxisAlignment.CENTER
        ),
        bgcolor=colors.BLUE,
        padding=10
    )

    full_name_field = TextField(label="Full Name", width=350)
    username_field = TextField(label="Username", width=350)
    email_field = TextField(label="Email", width=350)
    password_field = TextField(label="Password", password=True, can_reveal_password=True, width=350)

    registration_form = Column(
        [
            Text(value="Sign Up", style="headlineMedium", text_align="center", font_family="Lucida Handwriting",weight="Bold"),
            Container(height=10),
            full_name_field,
            Container(height=10),
            username_field,
            Container(height=10),
            email_field,
            Container(height=10),
            password_field,
            Container(height=10),
            ElevatedButton(text="Sign Up", width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=handle_signup),
            Container(height=10),
            ElevatedButton(text="Back to Login", width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=lambda e: show_login_page(page))
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )

    page.add(Container(
        content=Column(
            [
                title_container,
                Container(height=80),
                registration_form,
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        ),
        alignment=alignment.center,
    ))

def show_login_page(page: Page):
    page.clean()

    def handle_login(e):
        username = username_field.value
        password = password_field.value

        if not username or not password:
            page.snack_bar = SnackBar(Text("Please fill in all fields."), bgcolor=colors.RED)
            page.snack_bar.open = True
            page.update()
            return

        if user.login(username, password):
            snack_bar = SnackBar(Text("Login successful!"), bgcolor=colors.GREEN)
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            show_home_page(page, username)
        else:
            snack_bar = SnackBar(Text("Invalid username or password. Please sign up if you don't have an account."), bgcolor=colors.RED)
            page.overlay.append(snack_bar)
            page.update()
            snack_bar.open = True
            page.update()

    title_container = Container(
        content=ResponsiveRow(
            [
                Text(value="Welcome to ClothesVerve", style="headlineMedium", size=30, weight="bold", font_family="Lucida Handwriting", text_align="center", color=colors.WHITE)
            ],
            alignment=MainAxisAlignment.CENTER
        ),
        bgcolor=colors.BLUE,
        padding=10
    )

    username_field = TextField(label="Username", width=350)
    password_field = TextField(label="Password", password=True, can_reveal_password=True, width=350)

    login_form = Column(
        [
            Text(value="Login", style="headlineMedium", text_align="center", font_family="Lucida Handwriting",weight="Bold"),
            Container(height=20),
            username_field,
            Container(height=10),
            password_field,
            Container(height=5),
            TextButton(text="Forget Password?", on_click=lambda e: click_forget_password(page)),
            Container(height=5),
            ElevatedButton(text="Login", width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=handle_login),
            Container(height=20),
            Text(value="Don't have an account?", size=16, text_align="center"),
            ElevatedButton(text="Sign Up", width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=lambda _: show_signup_page(page)),
            Container(height=10),
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )

    page.add(Container(
        content=Column(
            [
                title_container,
                Container(height=80),
                login_form,
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        ),
        alignment=alignment.center,
    ))


def click_forget_password(page: Page):
    page.clean()

    def handle_forget_password(e):
        email = email_field.value

        if not email:
            page.snack_bar = SnackBar(Text("Please enter your email."), bgcolor=colors.RED)
            page.snack_bar.open = True
            page.update()
            return

        result = user.forget_password(email)
        if result == "email_not_found":
            page.snack_bar = SnackBar(Text("Email not found."), bgcolor=colors.RED)
        else:
            page.snack_bar = SnackBar(Text("Email found! Please enter a new password."), bgcolor=colors.GREEN)
            new_password_page(page, email) 

        page.snack_bar.open = True
        page.update()

    title_container = Container(
        content=ResponsiveRow(
            [
                Text(value="Welcome to ClothesVerve", style="headlineMedium", size=30, weight="bold", font_family="Lucida Handwriting", text_align="center", color=colors.WHITE)
            ],
            alignment=MainAxisAlignment.CENTER
        ),
        bgcolor=colors.BLUE,
        padding=10
    )

    email_field = TextField(label="Enter email address", width=350)

    forget_password_form = Column(
        [
            Text(value="Forgot Password", style="headlineMedium", text_align="center", font_family="Lucida Handwriting",weight="Bold"),
            Container(height=20),
            Text(value="Enter your email address", style="headlineMedium", text_align="center"),
            Container(height=10),
            email_field,
            Container(height=10),
            ElevatedButton(text="Continue",width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=handle_forget_password),
            Container(height=10),
            ElevatedButton(text="Back to Login",width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=lambda e: show_login_page(page)),
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )

    page.add(Container(
        content=Column(
            [
                title_container,
                Container(height=100),
                forget_password_form,
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        ),
        alignment=alignment.center,
    ))

def new_password_page(page: Page, email: str):
    page.clean()

    def handle_reset_password(e):
        new_password = password_field.value
        confirm_password = confirm_password_field.value

        result = user.reset_password(email, new_password, confirm_password)
        
        if result == "empty_fields":
            page.snack_bar = SnackBar(Text("Please fill in all fields."), bgcolor=colors.RED)
        elif result == "password_mismatch":
            page.snack_bar = SnackBar(Text("Passwords do not match."), bgcolor=colors.RED)
        elif result == "password_updated":
            page.snack_bar = SnackBar(Text("Password Reset successfully!"), bgcolor=colors.GREEN)
            show_login_page(page)

        page.snack_bar.open = True
        page.update()

    title_container = Container(
        content=ResponsiveRow(
            [
                Text(value="Welcome to ClothesVerve", style="headlineMedium", size=30, weight="bold", font_family="Lucida Handwriting", text_align="center", color=colors.WHITE)
            ],
            alignment=MainAxisAlignment.CENTER
        ),
        bgcolor=colors.BLUE,
        padding=10
    )

    password_field = TextField(label="Create new password", password=True, can_reveal_password=True, width=350)
    confirm_password_field = TextField(label="Confirm your password", password=True, can_reveal_password=True, width=350)

    reset_password_form = Column(
        [
            Text(value="New Password", style="headlineMedium", text_align="center", font_family="Lucida Handwriting",weight="Bold"),
            Container(height=20),
            password_field,
            Container(height=10),
            confirm_password_field,
            Container(height=10),
            ElevatedButton(text="Reset Password", width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=handle_reset_password),
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )

    page.add(Container(
        content=Column(
            [
                title_container,
                Container(height=120),
                reset_password_form,
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        ),
        alignment=alignment.center,
    ))

def get_user_full_name(username):
    result = user.get_user_by_username(username)
    return result['full_name'] if result else "User"


def get_user_id(username):
    result = user.get_user_by_username(username)
    return result['user_id'] if result else None


def show_home_page(page: Page, username: str):
    previous_page = {"category": None}

    def search_clothes(e):
        query = search.value.strip().lower()

        if not query:
            page.snack_bar = SnackBar(
                Text("Please enter a search query before searching.", color=colors.WHITE),
                bgcolor=colors.RED
            )
            page.snack_bar.open = True
            page.update()
            return

        clothes_data = admin.get_all_clothes()

        search_results = [
            clothes for clothes in clothes_data
            if query in clothes['name'].lower() or query in clothes['brand_name'].lower()
        ]

        if search_results:
            clothes_grid = []
            row = Row(alignment=MainAxisAlignment.CENTER, spacing=30)

            for i, clothes in enumerate(search_results):
                image = Image(src_base64=base64.b64encode(clothes['image']).decode('utf-8'), width=300, height=300)
                clothes_name = Text(value=f"{clothes['name']}", weight="bold")
                clothes_price = Text(value=f"{clothes['selling_price']}", weight="bold")
                view_clothes_button = ElevatedButton(
                    text="View Clothes",
                    bgcolor=colors.YELLOW_300,
                    color=colors.BLACK,
                    on_click=lambda e, clothes=clothes: show_clothes_details(clothes)
                )

                clothes_info = Column(
                    [
                        image,
                        clothes_name,
                        clothes_price,
                        view_clothes_button
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER
                )
                clothes_container = Container(content=clothes_info, width=300, padding=10, border_radius=10, bgcolor=colors.WHITE70)
                row.controls.append(clothes_container)

                if (i + 1) % 4 == 0:
                    clothes_grid.append(row)
                    row = Row(alignment=MainAxisAlignment.CENTER, spacing=30)

            if row.controls:
                clothes_grid.append(row)

            scrollable_content = Column(
                controls=[
                    title_container,
                    tabs_searchbar_back,
                    Container(
                        content=Text(value=f"SEARCH RESULT : {query.upper()}", color=colors.BLACK, size=20, weight="bold"),
                        alignment=alignment.center, 
                        padding=10
                    ),
                    *clothes_grid,
                ],
                scroll=ScrollMode.AUTO,  
                alignment=MainAxisAlignment.START,
                expand=True
            )
        else:
            scrollable_content = Column(
                controls=[
                    title_container,
                    tabs_searchbar_back,
                    Container(
                        content=Text(value="SEARCH RESULT NOT FOUND", color=colors.BLACK, size=20, weight="bold"),
                        alignment=alignment.center,
                        padding=10
                    ),
                ],
                alignment=MainAxisAlignment.START,
                expand=True
            )

        page.clean()
        page.add(scrollable_content)
        page.update()

    def display_clothes_by_category(category=None):
        clothes_data = admin.get_all_clothes() 

        if category:
            clothes_data = [clothes for clothes in clothes_data if clothes['category'].lower() == category.lower()]

        clothes_grid = []
        row = Row(alignment=MainAxisAlignment.CENTER, spacing=30)

        for i, clothes in enumerate(clothes_data):
            image = Image(src_base64=base64.b64encode(clothes['image']).decode('utf-8'), width=300, height=300)
            clothes_name = Text(value=f"{clothes['name']}", weight="bold")
            clothes_price = Text(value=f"{clothes['selling_price']}", weight="bold")
            view_clothes_button = ElevatedButton(
                text="View Clothes",
                bgcolor=colors.YELLOW_300,
                color=colors.BLACK,
                on_click=lambda e, c=clothes: show_clothes_details(c),
            )

            clothes_info = Column(
                [
                    image,
                    clothes_name,
                    clothes_price,
                    view_clothes_button
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER
            )
            clothes_container = Container(content=clothes_info, width=300, padding=10, border_radius=10, bgcolor=colors.WHITE70)
            row.controls.append(clothes_container)

            if (i + 1) % 4 == 0:
                clothes_grid.append(row)
                row = Row(alignment=MainAxisAlignment.CENTER, spacing=30)

        if row.controls:
            clothes_grid.append(row)

        scrollable_content = Column(
            controls=[
                title_container,
                tabs_searchbar_back,
                img_row,
                *clothes_grid,  
            ],
            scroll=ScrollMode.AUTO, 
            alignment=MainAxisAlignment.START,
            expand=True
        )

        page.clean()
        page.add(scrollable_content)
        page.update()

    def display_cart_items(user_id):
        cart_items = user.cart

        if cart_items:
            cart_grid = []
            row = Row(alignment=MainAxisAlignment.CENTER, spacing=30)

            for i, item in enumerate(cart_items):
                image = Image(src_base64=item['clothes_img'], width=300, height=300)
                clothes_name = Text(value=f"Name: {item['clothes_name']}", weight="bold")
                clothes_price = Text(value=f"Price: {item['clothes_price']}", weight="bold")
                clothes_size = Text(value=f"Size: {item['clothes_size']}", weight="bold")
                clothes_brand = Text(value=f"Quantity: {item['clothes_quantity']}", weight="bold")
                remove_from_cart = ElevatedButton(
                    text="Remove",
                    bgcolor=colors.RED_400,
                    color=colors.BLACK,
                    on_click=lambda e, item=item: remove_item_from_cart(item)
                )

                cart_item_info = Column(
                    [
                        image,
                        clothes_name,
                        clothes_price,
                        clothes_brand,
                        clothes_size,
                        remove_from_cart
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER
                )
                cart_item_container = Container(content=cart_item_info, width=300, padding=10, border_radius=10, bgcolor=colors.WHITE70)
                row.controls.append(cart_item_container)

                if (i + 1) % 4 == 0:
                    cart_grid.append(row)
                    row = Row(alignment=MainAxisAlignment.CENTER, spacing=30)

            if row.controls:
                cart_grid.append(row)

            user_id = get_user_id(username)
            checkout_button = ElevatedButton(
                text="Checkout",
                bgcolor=colors.BLUE,
                color=colors.WHITE,
                width=350,
                on_click=lambda e: on_checkout_click(user_id,user_id)  

            )

            cart_grid.append(Row(controls=[checkout_button], alignment=MainAxisAlignment.CENTER))

            scrollable_content = Column(
                controls=[
                    title_container,
                    tabs_searchbar_back,
                    *cart_grid,
                ],
                scroll=ScrollMode.AUTO, 
                alignment=MainAxisAlignment.START,
                expand=True
            )

        else:
            no_cart_message = Container(
                content=Text("NO CART ADDED", size=20, color=colors.BLACK, weight="bold"),
                alignment=alignment.center,  
                padding=10
            )

            scrollable_content = Column(
                controls=[
                    title_container,
                    tabs_searchbar_back,
                    no_cart_message  
                ],
                alignment=MainAxisAlignment.START,
                expand=True
            )

        page.clean()
        page.add(scrollable_content)
        page.update()

    def remove_item_from_cart(item):
        user.cart.remove(item)
        user_info = get_user_full_name(username)
        if user_info:
            user_id = get_user_id(username) 
            display_cart_items(user_id) 
        else:
            print("User not found")


    def on_checkout_click(e, user_id):
        page.clean()

        user_id = get_user_id(username)

        user.checkout(user_id)

        bill_data = user.generate_bill(user_id)

        page.bgcolor = colors.WHITE

        title_container = Container(
            content=ResponsiveRow(
                [
                    Text(value=f"Your Bill", style="headlineMedium", size=30, weight="bold", font_family="Lucida Handwriting", text_align="center", color=colors.WHITE)
                ],
                alignment=MainAxisAlignment.CENTER
            ),
            bgcolor=colors.BLUE,
            padding=10
        )

        customer_info = Text(f"Name: {bill_data['full_name']}\nContact: {bill_data['email']}\n"f"Day: {bill_data['day']}\nDate: {bill_data['date']}\nTime: {bill_data['time']}",size=18)

        table_header = Row([
            Container(Text("Item Name", size=18, weight="bold"), width=150),
            Container(Text("Brand", size=18, weight="bold"), width=100),
            Container(Text("Size", size=18, weight="bold"), width=50),
            Container(Text("Quantity", size=18, weight="bold"), width=100),
            Container(Text("Price", size=18, weight="bold"), width=100),
            Container(Text("Total", size=18, weight="bold"), width=100),
        ], alignment=MainAxisAlignment.SPACE_AROUND, spacing=2)

        table_rows = []
        for item in bill_data["cart"]:
            row = Row([
                Container(Text(item['clothes_name']), width=150),
                Container(Text(item['clothes_brand']), width=100),
                Container(Text(item['clothes_size']), width=50),
                Container(Text(str(item['clothes_quantity'])), width=100),
                Container(Text(str(f"${item['clothes_price']:.2f}")), width=100),
                Container(Text(str(f"${item['clothes_quantity'] * item['clothes_price']:.2f}")), width=100),
            ], alignment=MainAxisAlignment.SPACE_AROUND, spacing=2)
            table_rows.append(row)

        total_display = Column([
            Text(f"Subtotal: ${bill_data['subtotal']:.2f}", size=18),
            Text(f"Tax (5%): ${bill_data['tax']:.2f}", size=18),
            Text(f"Grand Total: ${bill_data['grand_total']:.2f}", size=20, weight="bold"),
        ], alignment=MainAxisAlignment.END, spacing=10)

        footer = Container(
            content=Text("Thank you for shopping with us!", size=18),
            alignment=alignment.center,
            padding=padding.only(top=20)
        )

        back_button = Container(
            content=ElevatedButton(
                text="Back",
                bgcolor=colors.BLUE,
                color=colors.WHITE,
                width=350,
                on_click=lambda e: display_cart_items(user_id)
            ),
            alignment=alignment.center  
        )
        
        scrollable_content = Container(
            content=Column(
                controls=[
                    title_container,
                    Container(height=20),
                    customer_info,
                    Container(height=10),
                    table_header,
                    *table_rows,
                    Container(height=10),
                    total_display,
                    Container(height=10),
                    footer,
                    Container(height=10),
                    back_button,
                ],
                alignment=MainAxisAlignment.START,
                scroll=ScrollMode.AUTO, 
            ),
            expand=True,
            padding=10,
        )

        page.add(scrollable_content)

        page.update()

    def show_clothes_details(clothes):
        page.clean()
        previous_page["category"] = tabs.tabs[tabs.selected_index].text

        quantity = 1

        def increment(e):
            nonlocal quantity
            quantity += 1
            quantity_text.value = str(quantity)
            page.update()

        def decrement(e):
            nonlocal quantity
            if quantity > 1:
                quantity -= 1
                quantity_text.value = str(quantity)
                page.update()

        def add_to_cart(e):
            selected_size = size_group.value

            if not selected_size:
                snack_bar = SnackBar(Text("Please select a size before adding to cart.", color=colors.WHITE), bgcolor=colors.RED)
                page.overlay.append(snack_bar)
                snack_bar.open = True
            else:
                success = user.add_to_cart(
                    clothes_img=base64.b64encode(clothes['image']).decode('utf-8'), 
                    clothes_id=clothes['id'],
                    clothes_name=clothes['name'],
                    clothes_price=clothes['selling_price'],
                    clothes_category=clothes['category'],
                    clothes_brand=clothes['brand_name'],
                    clothes_size=selected_size,
                    clothes_quantity=quantity
                )

                if success:
                    snack_bar = SnackBar(Text("Clothes added to cart successfully!", color=colors.WHITE), bgcolor=colors.GREEN)
                else:
                    snack_bar = SnackBar(Text("Item already added to cart!", color=colors.WHITE), bgcolor=colors.RED)
                
                page.overlay.append(snack_bar)
                snack_bar.open = True

            page.update()

        quantity_text = Text(str(quantity), size=20)

        clothes_image = Image(
            src_base64=base64.b64encode(clothes['image']).decode('utf-8'),
            width=500,
            height=500
        )

        size_group = RadioGroup(
            content=Row(
                [
                    Radio(value="S", label="Small"),
                    Radio(value="M", label="Medium"),
                    Radio(value="L", label="Large"),
                    Radio(value="XL", label="Extra Large"),
                ]
            )
        )

        clothes_details = Column(
            [
                Text(value=f"Name: {clothes['name']}", size=20, weight="bold"),
                Container(height=10),
                Text(value=f"Price: {clothes['selling_price']}", size=20, weight="bold"),
                Container(height=10),
                Text(value=f"Brand: {clothes['brand_name']}", size=20, weight="bold"),
                Container(height=10),
                Text(value=f"Category: {clothes['category']}", size=20, weight="bold"),
                Container(height=10),
                Text(value="Select Size:", size=20, weight="bold"),
                size_group,
                Container(height=10),
                Text(value="Select Quantity:", size=20, weight="bold"),
                Row(
                    [
                        IconButton(icon=icons.REMOVE, icon_color=colors.BLACK, on_click=decrement),
                        quantity_text,
                        IconButton(icon=icons.ADD, icon_color=colors.BLACK, on_click=increment),
                    ],
                    alignment="center",
                    spacing=10
                ),
                ElevatedButton(
                    text="Add to Cart",
                    bgcolor=colors.YELLOW_300,
                    color=colors.BLACK,
                    width=200,
                    on_click=add_to_cart
                )
            ],
            alignment=MainAxisAlignment.START,
            spacing=10
        )

        details_row = Row(
            [
                clothes_image,
                clothes_details
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=50
        )

        back_button = ElevatedButton(
            text="Back",
            bgcolor=colors.BLUE,
            color=colors.WHITE,
            width=350,
            on_click=lambda e: navigate_back()
        )

        title_container = Container(
            content=ResponsiveRow(
                [
                    Text(
                        value="Welcome to ClothesVerve",
                        style="headlineMedium",
                        size=30,
                        weight="bold",
                        font_family="Lucida Handwriting",
                        text_align="center",
                        color=colors.WHITE
                    )
                ],
                alignment=MainAxisAlignment.CENTER
            ),
            bgcolor=colors.BLUE,
            padding=10
        )

        page.add(Container(
            content=Column(
                [
                    title_container,
                    Container(height=10),
                    details_row,
                    Container(height=10),
                    back_button,
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            ),
            alignment=alignment.center,
        ))


    def navigate_back():
        if previous_page["category"]:
            display_clothes_by_category(previous_page["category"])
        else:
            display_clothes_by_category()

    def on_tab_change(e):
        selected_tab = tabs.tabs[e.control.selected_index].text
        if selected_tab == "HOME":
            display_clothes_by_category()
        elif selected_tab == "MENS":
            display_clothes_by_category("Mens")
        elif selected_tab == "WOMENS":
            display_clothes_by_category("Womens")
        elif selected_tab == "CHILDRENS":
            display_clothes_by_category("Children")
        elif selected_tab == "ADD TO CART":
            user_info = get_user_full_name(username)
            if user_info:
                user_id = get_user_id(username)  
                display_cart_items(user_id)      
            else:
                print("User not found")

    full_name = get_user_full_name(username)
    
    title_container = Container(
        content=ResponsiveRow(
            [
                Text(value=f"Welcome to ClothesVerve\n{full_name}", style="headlineMedium", size=30, weight="bold", font_family="Lucida Handwriting", text_align="center", color=colors.WHITE)
            ],
            alignment=MainAxisAlignment.CENTER
        ),
        bgcolor=colors.BLUE,
        padding=10
    )

    search = TextField(hint_text="Search for Brand, Clothes Name", height=40)
    search_bar = Container(
        content=Row(
            [
                search,
                IconButton(icon=icons.SEARCH, icon_size=24, bgcolor=colors.WHITE,on_click=search_clothes)
            ],
            alignment=MainAxisAlignment.START,
            spacing=2
        ),
        padding=5,
    )

    tabs = Tabs(
        selected_index=0,
        tabs=[
            Tab(text="HOME"),
            Tab(text="MENS"),
            Tab(text="WOMENS"),
            Tab(text="CHILDRENS"),
            Tab(text="ADD TO CART"),
        ],
        indicator_color=colors.BLUE,
        label_color=colors.BLUE,
        unselected_label_color=colors.BLUE,
        tab_alignment=MainAxisAlignment.CENTER,
        on_change=on_tab_change 
    )

    logout_button = ElevatedButton(text="Logout", width=150, color=colors.WHITE, bgcolor=colors.RED, on_click=lambda e: show_login_page(page))

    search_and_tabs = Row(
        [
            search_bar, 
            tabs,         
        ],
        alignment=MainAxisAlignment.START,  
        vertical_alignment=CrossAxisAlignment.CENTER,
        spacing=130,  
    )

    tabs_searchbar_back = Row(
        [
            search_and_tabs, 
            logout_button, 
        ],
        alignment=MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=CrossAxisAlignment.CENTER,
    )

    img = Image(
        src="homepage.jpg",
        width=1340,
        height=800,
        fit=ImageFit.CONTAIN,
    )
    img_row = Row(
        [
            img,
        ],
        alignment=MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=CrossAxisAlignment.CENTER,
        height=200
    )

    display_clothes_by_category()

def main(page: Page):
    page.title = "Clothes Application"
    page.auto_scale = True
    page.window.always_on_top = True
    page.window.width = 2000
    page.window.height = 900
    page.adaptive = True

    db = Database()
    global admin
    admin = Admin(db)
    global user
    user = User(db)

    show_login_page(page)

app(target=main)