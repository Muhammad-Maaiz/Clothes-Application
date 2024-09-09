from flet import *
from PIL import Image as PILImage
import io
import base64 
from backend import *

def show_admin_login_page(page: Page):
    page.clean()

    def exit_click(e):
        page.window.close()

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
                    color=colors.WHITE,
                )
            ],
            alignment=MainAxisAlignment.START,
        ),
        bgcolor=colors.BLUE,
        padding=10,
    )

    def handle_login(e):
        username = admin_username.value
        password = admin_password.value

        if not username or not password:
            page.snack_bar = SnackBar(Text("Please fill in all fields."), bgcolor=colors.RED)
            page.snack_bar.open = True
            page.update()
            return

        if username == "admin" and password == "123":
            show_admin_dashboard(page)
        else:
            if not username == "admin" and password == "123":
                error_message = "Incorrect username."
            elif username == "admin" and not password == "123":
                error_message = "Incorrect Password."
            else:
                error_message = "Incorrect username or password. Please try again."

            page.snack_bar = SnackBar(Text(error_message), bgcolor=colors.RED)
            page.snack_bar.open = True
            page.update()

    admin_username = TextField(label="Username", width=350)
    admin_password = TextField(label="Password", password=True, can_reveal_password=True, width=350)

    admin_form = Column(
        [
            Text(value="Admin Login", style="headlineMedium", text_align="center", font_family="Lucida Handwriting",weight="Bold"),
            Container(height=20),
            admin_username,
            Container(height=10),
            admin_password,
            Container(height=10),
            ElevatedButton(
                text="Login",
                width=350,
                color=colors.WHITE,
                bgcolor=colors.BLUE,
                on_click=handle_login,
            ),
            Container(height=10),
            ElevatedButton(
                text="Exit",
                width=350,
                color=colors.WHITE,
                bgcolor=colors.RED,
                on_click=exit_click
,
            ),
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    page.add(
        Container(
            content=Column(
                [
                    title_container,
                    Container(height=120),
                    admin_form,
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            ),
            alignment=alignment.center,
        )
    )

def show_admin_dashboard(page: Page):
    page.clean()
    title_container = Container(
        content=ResponsiveRow(
            [
                Text(value="Admin Dashboard", style="headlineMedium", size=30, weight="bold", font_family="Lucida Handwriting", text_align="center", color=colors.WHITE)
            ],
            alignment=MainAxisAlignment.START
        ),
        bgcolor=colors.BLUE,
        padding=10
    )
    dashboard_content = Column(
        [
            ElevatedButton(text="Add Clothes", width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=lambda e: show_add_clothes_page(page)),
            Container(height=10),
            ElevatedButton(text="View All Clothes", width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=lambda e: show_view_clothes_page(page)),
            Container(height=10),
            # ElevatedButton(text="View Users", width=350, color=colors.WHITE, bgcolor=colors.BLUE),
            # Container(height=10),
            # ElevatedButton(text="View Sales Records", width=350, color=colors.WHITE, bgcolor=colors.BLUE),
            # Container(height=10),
            # ElevatedButton(text="Calculate Profits", width=350, color=colors.WHITE, bgcolor=colors.BLUE),
            # Container(height=10),
            ElevatedButton(text="Logout", width=350, color=colors.WHITE, bgcolor=colors.RED, on_click=lambda e: show_admin_login_page(page))
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )
    page.add(Container(
        content=Column(
            [
                title_container,
                Container(height=150),
                dashboard_content,
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        ),
        alignment=alignment.center,
    ))

def show_add_clothes_page(page):
    page.clean()
    title_container = Container(
        content=ResponsiveRow(
            [
                Text(value="Add Clothes", style="headlineMedium", size=30, weight="bold", font_family="Lucida Handwriting", text_align="center", color=colors.WHITE)
            ],
            alignment=MainAxisAlignment.START
        ),
        bgcolor=colors.BLUE,
        padding=10
    )
    image_bytes = None

    def on_upload_result(e):
        nonlocal image_bytes
        if e.files:
            file_path = e.files[0].path
            with open(file_path, "rb") as f:
                image_bytes = f.read()
            image = Image(src_base64=base64.b64encode(image_bytes).decode('utf-8'), width=350, height=250)
            image_container.content = image
            page.update()

    file_picker = FilePicker(on_result=on_upload_result)
    page.overlay.append(file_picker)
    upload_button = ElevatedButton(text="Upload Image", width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=lambda _: file_picker.pick_files())
    image_container = Container(
        content=Text(value="No Image Selected", size=16, color=colors.BLACK),
        width=350,
        height=250,
        bgcolor=colors.GREY_400,
        alignment=alignment.center
    )
    clothes_name = TextField(label="Clothes Name", width=350)
    clothes_category = Dropdown(label="Category", width=350, options=[
        dropdown.Option("Mens"),
        dropdown.Option("Womens"),
        dropdown.Option("Children"),
    ])
    clothes_brand_name = TextField(label="Clothes Brand Name", width=350)
    clothes_price = TextField(label="Price", width=350)
    clothes_selling_price = TextField(label="Selling Price", width=350)
    clothes_quantity = TextField(label="Quantity", width=350)

    def handle_add_clothes(e):
        if not clothes_name.value or not clothes_category.value or not clothes_brand_name.value or not clothes_price.value or not clothes_selling_price.value or not clothes_quantity.value or not image_bytes:
            page.snack_bar = SnackBar(Text("Please fill in all fields and upload an image."), bgcolor=colors.RED)
            page.snack_bar.open = True
            page.update()
            return

        admin.add_clothes(clothes_name.value, clothes_category.value, clothes_brand_name.value, clothes_price.value, clothes_selling_price.value, clothes_quantity.value, image_bytes)

        page.snack_bar = SnackBar(Text("Clothes added successfully!"), bgcolor=colors.GREEN)
        page.snack_bar.open = True
        page.update()

        show_admin_dashboard(page)

    add_clothes_form = Column(
        [
            Text(value="Add New Clothes", style="headlineMedium", text_align="center", font_family="Lucida Handwriting",weight="Bold"),
            Container(height=10),
            image_container,
            Container(height=10),
            upload_button,
            Container(height=10),
            clothes_name,
            Container(height=10),
            clothes_category,
            Container(height=10),
            clothes_brand_name,
            Container(height=10),
            clothes_price,
            Container(height=10),
            clothes_selling_price,
            Container(height=10),
            clothes_quantity,
            Container(height=10),
            ElevatedButton(text="Add Clothes", width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=handle_add_clothes),
            Container(height=10),
            ElevatedButton(text="Back to Dashboard", width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=lambda e: show_admin_dashboard(page))
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )
    page.add(Container(
        content=Column(
            [
                title_container,
                Container(height=10),
                add_clothes_form
            ],
            scroll=ScrollMode.AUTO,
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        ),
        alignment=alignment.center,
        expand=True
    ))

def show_update_clothes_page(page: Page, clothes):
    page.clean()
    title_container = Container(
        content=ResponsiveRow(
            [
                Text(value="Update Clothes", style="headlineMedium", size=30, weight="bold", font_family="Lucida Handwriting", text_align="center", color=colors.WHITE)
            ],
            alignment=MainAxisAlignment.START
        ),
        bgcolor=colors.BLUE,
        padding=10
    )

    image_bytes = clothes['image']

    def on_upload_result(e):
        nonlocal image_bytes
        if e.files:
            file_path = e.files[0].path
            with open(file_path, "rb") as f:
                image_bytes = f.read()
            image = Image(src_base64=base64.b64encode(image_bytes).decode('utf-8'), width=350, height=250)
            image_container.content = image
            page.update()

    file_picker = FilePicker(on_result=on_upload_result)
    page.overlay.append(file_picker)
    upload_button = ElevatedButton(text="Upload Image", width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=lambda _: file_picker.pick_files())
    image = Image(src_base64=base64.b64encode(clothes['image']).decode('utf-8'), width=350, height=250)
    image_container = Container(
        content=image,
        width=350,
        height=250,
        bgcolor=colors.GREY_400,
        alignment=alignment.center
    )

    clothes_name = TextField(label="Clothes Name", width=350, value=clothes['name'])
    clothes_category = Dropdown(label="Category", width=350, value=clothes['category'], options=[
        dropdown.Option("Mens"),
        dropdown.Option("Womens"),
        dropdown.Option("Children"),
    ])
    clothes_brand_name = TextField(label="Clothes Brand Name", width=350, value=clothes['brand_name'])
    clothes_price = TextField(label="Price", width=350, value=str(clothes['price']))
    clothes_selling_price = TextField(label="Selling Price", width=350, value=str(clothes['selling_price']))
    clothes_quantity = TextField(label="Quantity", width=350, value=str(clothes['quantity']))

    def handle_update_clothes(e):
        if not clothes_name.value or not clothes_category.value or not clothes_brand_name.value or not clothes_price.value or not clothes_selling_price.value or not clothes_quantity.value or not image_bytes:
            page.snack_bar = SnackBar(Text("Please fill in all fields and upload an image."), bgcolor=colors.RED)
            page.snack_bar.open = True
            page.update()
            return

        admin.update_clothes(clothes['id'], clothes_name.value, clothes_category.value, clothes_brand_name.value, clothes_price.value, clothes_selling_price.value, clothes_quantity.value, image_bytes)

        page.snack_bar = SnackBar(Text("Clothes updated successfully!"), bgcolor=colors.GREEN)
        page.snack_bar.open = True
        page.update()

        show_view_clothes_page(page)

    update_clothes_form = Column(
        [
            Text(value="Update Clothes", style="headlineMedium", text_align="center", font_family="Lucida Handwriting",weight="Bold"),
            Container(height=10),
            image_container,
            Container(height=10),
            upload_button,
            Container(height=10),
            clothes_name,
            Container(height=10),
            clothes_category,
            Container(height=10),
            clothes_brand_name,
            Container(height=10),
            clothes_price,
            Container(height=10),
            clothes_selling_price,
            Container(height=10),
            clothes_quantity,
            Container(height=10),
            ElevatedButton(text="Update Clothes", width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=handle_update_clothes),
            Container(height=10),
            ElevatedButton(text="Back to View Clothes", width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=lambda e: show_view_clothes_page(page))
        ],
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER
    )
    page.add(Container(
        content=Column(
            [
                title_container,
                Container(height=10),
                update_clothes_form
            ],
            scroll=ScrollMode.AUTO,
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        ),
        alignment=alignment.center,
        expand=True
    ))

def show_view_clothes_page(page: Page):
    page.clean()
    title_container = Container(
        content=ResponsiveRow(
            [
                Text(value="View All Clothes", style="headlineMedium", size=30, weight="bold", font_family="Lucida Handwriting", text_align="center", color=colors.WHITE)
            ],
            alignment=MainAxisAlignment.START
        ),
        bgcolor=colors.BLUE,
        padding=10
    )
    
    clothes_data = admin.get_all_clothes()  

    clothes_grid = []
    row = Row(alignment=MainAxisAlignment.CENTER, spacing=20)
    
    for i, clothes in enumerate(clothes_data):
        image = Image(src_base64=base64.b64encode(clothes['image']).decode('utf-8'), width=200, height=150)
        clothes_info = Column(
            [
                image,
                Text(value=f"Clothes Name: {clothes['name']}"),
                Text(value=f"Clothes Category: {clothes['category']}"),
                Text(value=f"Clothes Brand: {clothes['brand_name']}"),
                Text(value=f"Clothes Price: ${clothes['price']}"),
                Text(value=f"Clothes Selling Price: ${clothes['selling_price']}"),
                Text(value=f"Clothes Quantity: {clothes['quantity']}"),
                Row(
                    [
                        IconButton(
                            icon=icons.UPDATE,
                            tooltip="Update Clothes",
                            on_click=lambda e, clothes=clothes: show_update_clothes_page(page, clothes)
                        ),
                        IconButton(
                            icon=icons.DELETE,
                            tooltip="Delete Clothes",
                            on_click=lambda e, clothes=clothes: confirm_delete_clothes(page, clothes['id'])
                        )
                    ],
                    alignment=MainAxisAlignment.END
                )
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        )
        clothes_container = Container(content=clothes_info, width=300, padding=10, border_radius=10, bgcolor=colors.GREY_300)

        row.controls.append(clothes_container)
        
        if (i + 1) % 4 == 0:
            clothes_grid.append(row)
            row = Row(alignment=MainAxisAlignment.CENTER, spacing=20)
    
    if row.controls:
        clothes_grid.append(row)

    back_button = ElevatedButton(text="Back to Dashboard", width=350, color=colors.WHITE, bgcolor=colors.BLUE, on_click=lambda e: show_admin_dashboard(page))
    
    page.add(Container(
        content=Column(
            [
                title_container,
                Container(height=10),
                Column(clothes_grid, spacing=20, alignment=MainAxisAlignment.CENTER),
                Container(height=10),
                back_button,
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            scroll=ScrollMode.AUTO
        ),
        alignment=alignment.center,
        expand=True
    ))

def confirm_delete_clothes(page: Page, clothes_id):
    def on_dialog_result(e):
        page.dialog.open = False
        page.update()
        
        if e.control.text == "OK":
            admin.delete_clothes(clothes_id)
            page.snack_bar = SnackBar(Text("Clothes deleted successfully!"), bgcolor=colors.GREEN)
            show_view_clothes_page(page)
        else:
            page.snack_bar = SnackBar(Text("Deletion cancelled."), bgcolor=colors.BLUE_ACCENT)
        
        page.snack_bar.open = True
        page.update()

    # Create the dialog
    dialog = AlertDialog(
        title=Text("Delete Confirmation"),
        content=Text("Are you sure you want to delete these clothes?"),
        actions=[
            ElevatedButton(text="Cancel", on_click=on_dialog_result),
            ElevatedButton(text="OK", on_click=on_dialog_result),
        ],
        actions_alignment=MainAxisAlignment.END,
    )
    
    page.dialog = dialog
    page.dialog.open = True
    page.update()


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

    show_admin_login_page(page)

app(target=main)