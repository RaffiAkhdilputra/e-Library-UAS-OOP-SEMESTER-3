import io, urllib.request, webbrowser, abc, account
import customtkinter as ctk
import tkinter as tk
from google_books_api import *
from PIL import Image, ImageTk
from abc import abstractmethod

logged_account = None

class App(abc.ABC):
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.after(100, self.root.focus_force)

    @abstractmethod
    def widgets(self):
        pass

    @abstractmethod
    def run(self):
        pass

class Main(App):
    def __init__(self):
        self.max_cards = 10
        self.cursor = 0
        self.username = None
        self.books = None

        self.root = ctk.CTk()
        self.root.resizable(False, False)
        self.root.iconbitmap("logo.ico")
        self.root.title("e-Library")

        self.login_widget()

    def login_widget(self):
        self.root.geometry("500x250")

        # Clear Frames
        for widget in self.root.winfo_children():
            widget.destroy()

        # Login Frame
        login_frame = ctk.CTkFrame(self.root)
        login_frame.pack(padx=3, pady=3, fill="both", expand=True)

        entry_frame = ctk.CTkFrame(login_frame)
        entry_frame.pack(padx=3, pady=3, fill="both", expand=True)
        entry_frame.columnconfigure((0, 1), weight=1, uniform="column")
        entry_frame.rowconfigure((0, 1), weight=1, uniform="row")

        self.login_button_frame = ctk.CTkFrame(login_frame)
        self.login_button_frame.pack(padx=3, pady=3, fill="both", expand=True)
        self.login_button_frame.columnconfigure((0, 1), weight=1, uniform="column")
        self.login_button_frame.rowconfigure((0), weight=1, uniform="row")

        # Login Frame Content
        username_label = ctk.CTkLabel(entry_frame, text="Username\t:")
        username_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.username_entry = ctk.CTkEntry(entry_frame, placeholder_text="Enter your username")
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        password_label = ctk.CTkLabel(entry_frame, text="Password\t:")
        password_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.password_entry = ctk.CTkEntry(entry_frame, placeholder_text="Enter your password", show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.login_button = ctk.CTkButton(self.login_button_frame, text="Login", command=self.login)
        self.login_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.register_button = ctk.CTkButton(self.login_button_frame, text="Register", command=self.register)
        self.register_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    def login(self):
        _access, _message = account.verify_login(self.username_entry.get(), self.password_entry.get())

        if not _access:
            warning = ctk.CTkLabel(self.login_button_frame, text=_message, text_color="red")
            warning.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        else:
            self.username = self.username_entry.get()
            print(f"Logged in as: {self.username}")
            self.widgets()

    def register(self):
        self.root.geometry("500x400")

        for widget in self.root.winfo_children():
            widget.destroy()

        self.register_widget()

    def register_widget(self):
        self.register_frame = ctk.CTkFrame(self.root)
        self.register_frame.pack(padx=3, pady=3, fill="both", expand=True)

        entry_frame = ctk.CTkFrame(self.register_frame)
        entry_frame.pack(padx=3, pady=3, fill="both", expand=True)
        entry_frame.columnconfigure((0, 1), weight=1, uniform="column")
        entry_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform="row")

        button_frame = ctk.CTkFrame(self.register_frame)
        button_frame.pack(padx=3, pady=3, fill="both", expand=True)
        button_frame.columnconfigure((0, 1), weight=1, uniform="column")

        # Email
        email_label = ctk.CTkLabel(entry_frame, text="Email\t\t:")
        email_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.email_entry = ctk.CTkEntry(entry_frame, placeholder_text="Enter your email")
        self.email_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # First Name
        firstName_label = ctk.CTkLabel(entry_frame, text="First Name\t:")
        firstName_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.firstName_entry = ctk.CTkEntry(entry_frame, placeholder_text="Enter your name")
        self.firstName_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Last Name
        lastName_label = ctk.CTkLabel(entry_frame, text="Last Name\t:")
        lastName_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.lastName_entry = ctk.CTkEntry(entry_frame, placeholder_text="Enter your last name")
        self.lastName_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Tempat dan Tanggal Lahir
        self.tanggal_var = ctk.StringVar(value="1")
        self.bulan_var = ctk.StringVar(value="January")
        self.tahun_var = ctk.StringVar(value="2000")

        tempat_label = ctk.CTkLabel(entry_frame, text="Tempat\t\t:")
        tempat_label.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        self.tempat_menu = ctk.CTkEntry(entry_frame, placeholder_text="Masukkan Tempat Lahir")
        self.tempat_menu.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        tanggal_label = ctk.CTkLabel(entry_frame, text="Tanggal\t\t:")
        tanggal_label.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        self.tanggal_menu = ctk.CTkOptionMenu(entry_frame, values=[str(i) for i in range(1, 32)], variable=self.tanggal_var)
        self.tanggal_menu.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        bulan_label = ctk.CTkLabel(entry_frame, text="Bulan\t\t:")
        bulan_label.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")
        self.bulan_menu = ctk.CTkOptionMenu(entry_frame, values=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], variable=self.bulan_var)
        self.bulan_menu.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        tahun_label = ctk.CTkLabel(entry_frame, text="Tahun\t\t:")
        tahun_label.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")
        self.tahun_menu = ctk.CTkOptionMenu(entry_frame, values=[str(i) for i in range(1980, 2026)], variable=self.tahun_var)
        self.tahun_menu.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        # Password
        password_label = ctk.CTkLabel(entry_frame, text="Password\t:")
        password_label.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")
        self.password_entry = ctk.CTkEntry(entry_frame, placeholder_text="Enter your password", show="*")
        self.password_entry.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

        confirm_password_label = ctk.CTkLabel(entry_frame, text="Confirm Password\t:")
        confirm_password_label.grid(row=8, column=0, padx=5, pady=5, sticky="nsew")
        self.confirm_password_entry = ctk.CTkEntry(entry_frame, placeholder_text="Confirm your password", show="*")
        self.confirm_password_entry.grid(row=8, column=1, padx=5, pady=5, sticky="ew")

        # Buttons
        register_button = ctk.CTkButton(button_frame, text="Register", command=self.register_user)
        register_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=self.login_widget)
        cancel_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def register_user(self):
        if self.password_entry.get() == self.confirm_password_entry.get():
            tempat = self.tempat_menu.get()
            tanggal = self.tanggal_var.get()
            bulan = self.bulan_var.get()
            tahun = self.tahun_var.get()

            print(
                self.email_entry.get(),
                self.firstName_entry.get(),
                self.lastName_entry.get(),
                tempat, tanggal, bulan, tahun,
                self.confirm_password_entry.get()
            )

            # tambah akun baru
            account.add_new_account(self.email_entry.get(), self.confirm_password_entry.get(), self.firstName_entry.get(), self.lastName_entry.get(), tempat, tanggal, bulan, tahun)

            _access, _message = account.verify_login(self.email_entry.get(), self.confirm_password_entry.get())

            if _access:
                self.username = self.email_entry.get()
                self.widgets()
            else:
                print(_message)
        else:
            for widget in self.register_frame.winfo_children():
                if widget.winfo_class() == "CTkLabel":
                    widget.destroy()

            message = ctk.CTkLabel(self.register_frame, text="Password and Confirm Password do not match", text_color="red")
            message.pack(pady=5, fill="x", expand=True)

    def widgets(self):
        self.root.geometry("800x600")

        # Clear Frames
        for widget in self.root.winfo_children():
            widget.destroy()

        # Frames
        top_frame = ctk.CTkFrame(self.root)
        top_frame.pack(padx=3, pady=3, fill="x", expand=False)

        self.middle_frame = ctk.CTkScrollableFrame(self.root)
        self.middle_frame.pack(padx=3, pady=3, fill="both", expand=True)
        self.middle_frame.columnconfigure((0, 1), weight=1, uniform="column")

        bottom_frame = ctk.CTkFrame(self.root, height=50)
        bottom_frame.pack(padx=3, pady=3, fill="x", expand=False)

        # Top Frame Content
        self.search_entry = ctk.CTkEntry(top_frame, placeholder_text="Search for a book", width=250)
        self.search_entry.pack(pady=5)

        self.search_button = ctk.CTkButton(top_frame, text="Search", command=self.search_books, width=250)
        self.search_button.pack(pady=5)
        self.search_entry.bind("<Return>", lambda event: self.search_books())
        self.search_entry.bind("ctrl+A", lambda event: self.search_entry.select_range(0, tk.END))

        # Bottom Frame Content
        self.previous_button = ctk.CTkButton(bottom_frame, text="Previous", command=self.previous, state="disabled")
        self.previous_button.pack(side="left", padx=5, pady=5)

        self.next_button = ctk.CTkButton(bottom_frame, text="Next", command=self.next, state="disabled")
        self.next_button.pack(side="left", padx=5, pady=5)

        self.profile_button = ctk.CTkButton(bottom_frame, text="Profile", command= lambda: self.open_profile(self.username))
        self.profile_button.pack(side="right", padx=5, pady=5)

    def search_books(self):
        query = self.search_entry.get()
        if not query.strip():
            print("Search query is empty.")
            return

        self.books = get_book(query)
        if not self.books or "items" not in self.books:
            print("No books found.")
            return

        self.cursor = 0
        self.previous_button.configure(state="disabled")
        self.next_button.configure(state="normal")
        self.generate_card()

    def generate_card(self):
        for widget in self.middle_frame.winfo_children():
            widget.destroy()

        self.cards = []
        end_index = min(self.cursor + self.max_cards, len(self.books["items"]))

        for i in range(self.cursor, end_index):
            book = self.books["items"][i]

            # Get book ID
            try:
                book_id = book.get("id", "Unknown ID")
            except Exception as e:
                print(f"Error fetching book ID: {e}")
                continue

            # Get thumbnail
            image_url = book["volumeInfo"].get("imageLinks", {}).get("smallThumbnail", "")
            photo = None
            if image_url:
                try:
                    with urllib.request.urlopen(image_url) as u:
                        raw_data = u.read()
                    image = Image.open(io.BytesIO(raw_data))
                    photo = ImageTk.PhotoImage(image)
                except Exception as e:
                    print(f"Error fetching or opening image: {e}")

            # Get book details
            title = book["volumeInfo"].get("title", "Unknown Title")
            page = book["volumeInfo"].get("pageCount", "N/A")

            # Create card
            card = ctk.CTkFrame(self.middle_frame, height=200, border_color="black", border_width=1, corner_radius=16)
            card.grid(row=(i - self.cursor) // 2, column=(i - self.cursor) % 2, padx=3, pady=3, sticky="nsew")
            card.columnconfigure(0, weight=1, uniform="column")
            card.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform="row")

            # Add image to card
            if photo:
                image_label = ctk.CTkLabel(card, image=photo, text="")
                image_label.image = photo 
                image_label.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky="sew")

            # Add details to card
            title_label = ctk.CTkLabel(card, text=title, wraplength=180)
            title_label.grid(row=2, column=0, padx=5, pady=5, sticky="sew")
            page_label = ctk.CTkLabel(card, text=f"Pages: {page}")
            page_label.grid(row=3, column=0, padx=5, pady=5, sticky="sew")
            view_button = ctk.CTkButton(card, text="View", command= lambda b = book, id = book_id: self.open_description(b, id, self.username))
            view_button.grid(row=4, column=0, padx=5, pady=5, sticky="sew")

            self.cards.append(card)

        if self.cursor + self.max_cards >= len(self.books["items"]):
            self.next_button.configure(state="disabled")
        if self.cursor == 0 or self.cursor - self.max_cards < 0:
            self.previous_button.configure(state="disabled")
        else:
            self.previous_button.configure(state="normal")

    def next(self):
        if self.cursor + self.max_cards < len(self.books["items"]):
            self.cursor += self.max_cards
            self.generate_card()

    def previous(self):
        if self.cursor - self.max_cards >= 0:
            self.cursor -= self.max_cards
            self.generate_card()

    def open_description(self, book, book_id, logged_account):
        Description(self.root, book, book_id, logged_account)

    def open_profile(self, logged_account):
        Profile(self.root, logged_account)

    def run(self):
        self.root.mainloop()

    def logout(self):
        self.root.destroy()

class Description(ctk.CTkToplevel):
    def __init__(self, master, book, book_id, logged_account, *args, **kwargs):
        super().__init__(master)
        self.book = book
        self.book_id = book_id
        self.logged_account = logged_account

        self.after(100, self.focus_force)
        self.title("Book Description")
        self.geometry("500x600")
        
        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.container.pack(padx=3, pady=3, fill="both", expand=True)

        # Get book thumbnail
        image_url = self.book["volumeInfo"].get("imageLinks", {}).get("smallThumbnail", "")
        photo = None
        if image_url:
            try:
                with urllib.request.urlopen(image_url) as u:
                    raw_data = u.read()
                image = Image.open(io.BytesIO(raw_data))
                photo = ImageTk.PhotoImage(image)
            except Exception as e:
                print(f"Error fetching or opening image: {e}")

        # Add image to description
        if photo:
            image_label = ctk.CTkLabel(self.container, image=photo, text="")
            image_label.image = photo 
            image_label.pack(pady=10)

        # Display book details
        title = self.book["volumeInfo"].get("title", "Unknown Title")
        author = self.book["volumeInfo"].get("authors", ["Unknown Author"])
        page = self.book["volumeInfo"].get("pageCount", "N/A")
        description = self.book["volumeInfo"].get("description", "No description available.")
        read_links = self.book["accessInfo"].get("webReaderLink", "No links available.")
        
        title_label = ctk.CTkLabel(self.container, text=title, font=("Arial", 16, "bold"), wraplength=380)
        title_label.pack(pady=10)

        author_label = ctk.CTkLabel(self.container, text=f"Author: {', '.join(author)}", wraplength=380)
        author_label.pack(pady=5)

        page_label = ctk.CTkLabel(self.container, text=f"Pages: {page}", wraplength=380)
        page_label.pack(pady=5)

        description_text = ctk.CTkTextbox(self.container, wrap="word", height=200)
        description_text.insert("1.0", description)
        description_text.configure(state="disabled")
        description_text.pack(pady=10, padx=10, fill="both", expand=True)

        save_button = ctk.CTkButton(self.container, text="Save To Bookshelf", command=self.save)
        save_button.pack(padx=10, pady=10, fill = "x", expand=True)

        read_links_button = ctk.CTkButton(self.container, text="Read Online", command=lambda: webbrowser.open(read_links))
        read_links_button.pack(padx=10, pady=10, fill = "x", expand=True)

    def save(self):
        account.add_book_to_bookshelf(self.logged_account, self.book["volumeInfo"]["industryIdentifiers"][0]["identifier"])
        account.save_changes()

class Profile(ctk.CTkToplevel):
    def __init__(self, master, logged_account, *args, **kwargs):
        super().__init__(master)
        self.logged_account = account.get_user(logged_account)

        self.title("Profile")
        self.iconbitmap("logo.ico")
        self.after(100, self.focus_force)

        self.widget()

    def widget(self):
        self.geometry("500x400")
        for widget in self.winfo_children():
            widget.destroy()

        # Frame
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(padx=3, pady=3, fill="both", expand=True)

        # Display account details
        email_label = ctk.CTkLabel(container, text=f"Email\t\t\t: {self.logged_account['email']}", wraplength=380, anchor="nw")
        email_label.pack(side="top", padx=10, pady=3, fill = "x", expand=True)

        name_label = ctk.CTkLabel(container, text=f"Nama\t\t\t: {self.logged_account['content']['firstName']} {self.logged_account['content']['lastName']}", wraplength=380, anchor="nw")
        name_label.pack(side="top", padx=10, pady=3, fill = "x", expand=True)

        lahir_label = ctk.CTkLabel(container, 
                                   text=f"Tempat, Tanggal Lahir\t: {self.logged_account['content']['tempat']}, {self.logged_account['content']['tanggalLahir']} {self.logged_account['content']['bulanLahir']} {self.logged_account['content']['tahunLahir']}", wraplength=380, anchor="nw")
        lahir_label.pack(side="top", padx=10, pady=3, fill = "x", expand=True)

        akun_dibuat = ctk.CTkLabel(container, text=f"Akun dibuat\t\t: {self.logged_account['content']['tanggalDibuat']}", wraplength=380, anchor="nw")
        akun_dibuat.pack(side="top", padx=10, pady=3, fill = "x", expand=True)

        # Button Frame
        button_container = ctk.CTkFrame(container, fg_color="transparent")
        button_container.pack(side="top", pady=3, fill = "both", expand=True)
        button_container.columnconfigure((0, 1), weight=1, uniform="column")
        button_container.rowconfigure((0), weight=1, uniform="row")

        # Add buttons to the container
        change_password_button = ctk.CTkButton(button_container, text="Edit Profile", command=self.edit_profile)
        change_password_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        bookshelf_button = ctk.CTkButton(button_container, text="Bookshelf", command=self.bookshelf)
        bookshelf_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        edit_profile = ctk.CTkButton(button_container, text="Change Password", command=self.change_password)
        edit_profile.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        logout_button = ctk.CTkButton(button_container, text="Logout", command=self.logout)
        logout_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def edit_profile(self):
        self.geometry("700x200")
        self.resizable(False, False)

        for widget in self.winfo_children():
            widget.destroy()

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(padx=3, pady=3, fill="both", expand=True)
        container.columnconfigure((0, 1), weight=1, uniform="column")

        email_label = ctk.CTkLabel(container, text=f"Email\t\t\t: {self.logged_account['email']}", wraplength=380, anchor="nw", height=20)
        email_label.grid(row=0, column=0, columnspan=2, padx=10, pady=3, sticky="nsew")

        name_label = ctk.CTkLabel(container, text=f"Nama\t\t\t: {self.logged_account['content']['firstName']} {self.logged_account['content']['lastName']}", wraplength=380, anchor="nw", height=20)
        name_label.grid(row=1, column=0, padx=10, pady=3, sticky="nsew")

        lahir_label = ctk.CTkLabel(container, 
                                   text=f"Tempat, Tanggal Lahir\t: {self.logged_account['content']['tempat']}, {self.logged_account['content']['tanggalLahir']} {self.logged_account['content']['bulanLahir']} {self.logged_account['content']['tahunLahir']}", wraplength=380, anchor="nw", height=20)
        lahir_label.grid(row=2, column=0, padx=10, pady=3, sticky="nsew")

        # buttons
        edit_name_button = ctk.CTkButton(container, text="Edit", command=self.edit_name)
        edit_name_button.grid(row=1, column=1, padx=10, pady=10, sticky="nse")

        edit_tempat_tanggal_lahir_button = ctk.CTkButton(container, text="Edit", command=self.edit_tempat_tanggal_lahir)
        edit_tempat_tanggal_lahir_button.grid(row=2, column=1, padx=10, pady=10, sticky="nse")

        back_button = ctk.CTkButton(container, text="Back", command=self.back)
        back_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
    def edit_name(self):
        edit_window(self, self.logged_account, "nama")

    def edit_tempat_tanggal_lahir(self):
        edit_window(self, self.logged_account, "Tempat, Tanggal Lahir")

    def bookshelf(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.geometry("700x500")
        self.resizable(False, True)
        self.title("Bookshelf")

        bookshelf = account.get_bookshelf(self.logged_account["email"])

        container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        container.pack(side="top", padx=3, pady=3, fill="both", expand=True)
        container.columnconfigure((0, 1), weight=1, uniform="column")

        if not bookshelf:
            _message = ctk.CTkLabel(container, text="Bookshelf is empty.", wraplength=380)
            _message.grid(row=0, column=0, columnspan=2, padx=10, pady=3, sticky="nsew")
        else:
            for i, book_id in enumerate(bookshelf):
                try:
                    book_data = get_book(book_id, max=1)["items"][0]
                    title = book_data["volumeInfo"].get("title", "Unknown Title")
                    pages = book_data["volumeInfo"].get("pageCount", "Unknown Pages")
                    penulis = book_data["volumeInfo"].get("authors", ["Unknown Penulis"])[0]
                    publisher = book_data["volumeInfo"].get("publisher", "Unknown Publisher")

                    image_url = book_data["volumeInfo"].get("imageLinks", {}).get("smallThumbnail", "")
                    photo = None
                    if image_url:
                        try:
                            with urllib.request.urlopen(image_url) as u:
                                raw_data = u.read()
                            image = Image.open(io.BytesIO(raw_data))
                            photo = ImageTk.PhotoImage(image)
                        except Exception as e:
                            print(f"Error fetching or opening image: {e}")

                    card = ctk.CTkFrame(container, border_color="black", corner_radius=10)
                    card.grid(row=i, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
                    card.columnconfigure((0, 1), weight=1, uniform="column")
                    card.rowconfigure((0, 1, 2, 3), weight=1, uniform="row")

                    if photo:
                        image_label = ctk.CTkLabel(card, image=photo, text="")
                        image_label.image = photo
                        image_label.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="nsew")

                    # Details
                    title_label = ctk.CTkLabel(card, text=title, font=("Arial", 14, "bold"), wraplength=250, anchor="nw")
                    title_label.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

                    page_label = ctk.CTkLabel(card, text=f"Pages: {pages}", wraplength=250, anchor="nw")
                    page_label.grid(row=1, column=1, padx=10, pady=3, sticky="nw")

                    penulis_label = ctk.CTkLabel(card, text=f"Penulis: {penulis}", wraplength=250, anchor="nw")
                    penulis_label.grid(row=2, column=1, padx=10, pady=3, sticky="nw")

                    publisher_label = ctk.CTkLabel(card, text=f"Publisher: {publisher}", wraplength=250, anchor="nw")
                    publisher_label.grid(row=3, column=1, padx=10, pady=5, sticky="nw")
                    
                    # Buttons
                    remove_button = ctk.CTkButton(card, text="Remove", command=lambda b_id=book_id: account.remove_book_from_bookshelf(self.logged_account["email"], b_id))
                    remove_button.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

                    view_button = ctk.CTkButton(card, text="View", command=lambda b=book_data, b_id=book_id: self.open_description(b, b_id, self.logged_account["email"]))
                    view_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

                except Exception as e:
                    print(f"Error loading book data: {e}")

        refresh_button = ctk.CTkButton(self, text="Refresh", command=self.bookshelf)
        refresh_button.pack(side="top", padx=10, pady=10, fill = "x", expand=False)

        back_button = ctk.CTkButton(self, text="Back", command=self.back)
        back_button.pack(side="top", padx=10, pady=10, fill = "x", expand=False)
    
    def open_description(self, book, book_id, logged_account):
        Description(self, book, book_id, logged_account)

    def change_password(self):
        ChangePasswordWindow(self, self.logged_account)

    def back(self):
        self.widget()

    def logout(self):
        self.destroy()
        self.master.destroy()

class edit_window(ctk.CTkToplevel):
    def __init__(self, master, logged_account, target, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.logged_account = logged_account
        self.target = target
        self.after(100, self.focus_force)

        self.resizable(False, False)
        self.title(f"Edit {target}")

        frame = ctk.CTkFrame(self)
        frame.pack(padx=3, pady=3, fill="both", expand=True)
        frame.columnconfigure((0, 1), weight=1, uniform="column")

        if target == "Tempat, Tanggal Lahir":
            self.geometry("400x300")
            frame.rowconfigure((0, 1, 2, 3, 4), weight=1, uniform="row")

            # Tempat dan Tanggal Lahir
            self.tanggal_var = ctk.StringVar(value="1")
            self.bulan_var = ctk.StringVar(value="January")
            self.tahun_var = ctk.StringVar(value="2000")

            tempat_label = ctk.CTkLabel(frame, text="Tempat\t\t:")
            tempat_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
            self.tempat_menu = ctk.CTkEntry(frame, placeholder_text="Masukkan Tempat Lahir")
            self.tempat_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

            tanggal_label = ctk.CTkLabel(frame, text="Tanggal\t\t:")
            tanggal_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
            self.tanggal_menu = ctk.CTkOptionMenu(frame, values=[str(i) for i in range(1, 32)], variable=self.tanggal_var)
            self.tanggal_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

            bulan_label = ctk.CTkLabel(frame, text="Bulan\t\t:")
            bulan_label.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
            self.bulan_menu = ctk.CTkOptionMenu(frame, values=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], variable=self.bulan_var)
            self.bulan_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

            tahun_label = ctk.CTkLabel(frame, text="Tahun\t\t:")
            tahun_label.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
            self.tahun_menu = ctk.CTkOptionMenu(frame, values=[str(i) for i in range(1980, 2026)], variable=self.tahun_var)
            self.tahun_menu.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

            cancel_button = ctk.CTkButton(frame, text="Cancel", command=self.destroy)
            cancel_button.grid(row=4, column=0, padx=3, pady=3, sticky="ew")

            save_button = ctk.CTkButton(frame, text="Save", command=self.save)
            save_button.grid(row=4, column=1, padx=3, pady=3, sticky="ew")
        
        else:
            self.geometry("400x100")
            frame.rowconfigure((0, 1, 2), weight=1, uniform="row")

            firstName_label = ctk.CTkLabel(frame, text=f"First Name\t:")
            firstName_label.grid(row=0, column=0, padx=3, pady=3, sticky="ew")

            self.firstName_entry = ctk.CTkEntry(frame, placeholder_text="Enter your first name")
            self.firstName_entry.grid(row=0, column=1, padx=3, pady=3, sticky="ew")

            lastName_label = ctk.CTkLabel(frame, text="Last Name\t:")
            lastName_label.grid(row=1, column=0, padx=3, pady=3, sticky="ew")

            self.lastName_label = ctk.CTkEntry(frame, placeholder_text="Enter your last name")
            self.lastName_label.grid(row=1, column=1, padx=3, pady=3, sticky="ew")

            cancel_button = ctk.CTkButton(frame, text="Cancel", command=self.destroy)
            cancel_button.grid(row=2, column=0, padx=3, pady=3, sticky="ew")

            save_button = ctk.CTkButton(frame, text="Save", command=self.save)
            save_button.grid(row=2, column=1, padx=3, pady=3, sticky="ew")

    def save(self):
        if self.target == "Tempat, Tanggal Lahir":
            account.edit_tempat_tanggal_lahir(self.logged_account["email"], self.tempat_menu.get(), self.tanggal_var.get(), self.bulan_var.get(), self.tahun_var.get())
        else:
            account.edit_nama(self.logged_account["email"], self.firstName_entry.get(), self.lastName_label.get())
        
        self.destroy()
        account.save_changes()

class ChangePasswordWindow(ctk.CTkToplevel):
    def __init__(self, master, logged_account, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.logged_account = logged_account
        self.geometry("400x100")
        self.after(100, self.focus_force)

        frame = ctk.CTkFrame(self)
        frame.pack(padx=3, pady=3, fill="both", expand=True)
        frame.columnconfigure((0, 1), weight=1, uniform="column")
        frame.rowconfigure((0, 1, 2), weight=1, uniform="row")

        for widget in frame.winfo_children():
            widget.destroy()

        password_label = ctk.CTkLabel(frame, text="Password\t:")
        password_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Enter your password", show="*")
        self.password_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        cancel_button = ctk.CTkButton(frame, text="Cancel", command=self.destroy)
        cancel_button.grid(row=1, column=0, padx=3, pady=3, sticky="ew")

        continue_button = ctk.CTkButton(frame, text="Continue", command=self.check_password)
        continue_button.grid(row=1, column=1, padx=3, pady=3, sticky="ew")

    def check_password(self):
        _ = account.check_password(self.password_entry.get().encode('utf-8'), self.logged_account["hashed"])

        if _:
            self.destroy()
            ChangePasswordWindow(self.master, self.logged_account)
        else:
            ctk.CTkLabel(self, text="Wrong password").pack()

if __name__ == "__main__":
    app = Main()
    app.run()
