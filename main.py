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

        self.root = ctk.CTk()
        self.root.resizable(False, False)

        self.books = None

        self.root.title("e-Library")

        self.login_widget()

    def login_widget(self): # BENERIN LOGIN DAN BUAT FITUR REGISTER (RESIZE FRAME, BUAT FORM SIMPLE SESUAI FIGMA)
        self.root.geometry("500x200")

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

        button_frame = ctk.CTkFrame(login_frame)
        button_frame.pack(padx=3, pady=3, fill="both", expand=True)
        button_frame.columnconfigure((0, 1), weight=1, uniform="column")
        entry_frame.rowconfigure((0), weight=1, uniform="row")

        # Login Frame Content
        username_label = ctk.CTkLabel(entry_frame, text="Username\t:")
        username_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.username_entry = ctk.CTkEntry(entry_frame, placeholder_text="Enter your username")
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        password_label = ctk.CTkLabel(entry_frame, text="Password\t:")
        password_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.password_entry = ctk.CTkEntry(entry_frame, placeholder_text="Enter your password", show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.login_button = ctk.CTkButton(button_frame, text="Login", command=self.login)
        self.login_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.register_button = ctk.CTkButton(button_frame, text="Register", command=self.register)
        self.register_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def login(self):
        _access, _message = account.verify_login(self.username_entry.get(), self.password_entry.get())

        if not _access:
            print(self.username_entry.get(), self.password_entry.get())
            print(_message)
        else:
            self.username = self.username_entry.get()
            print(f"Logged in as: {self.username}")
            self.widgets()

    def register(self):
        pass

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
            view_button = ctk.CTkButton(card, text="View", command=lambda b=book, b_id=book_id: self.open_description(b, b_id))
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

    def open_description(self, book, target_id):
        Description(self.root, book, target_id)

    def open_profile(self, logged_account):
        Profile(self.root, logged_account)

    def run(self):
        self.root.mainloop()

    def logout(self):
        self.root.destroy()

class Description(ctk.CTkToplevel):
    def __init__(self, master, book, target_id, *args, **kwargs):
        super().__init__(master)
        self.book = book
        self.target_id = target_id

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

        read_links_button = ctk.CTkButton(self.container, text="Read Online", command=lambda: webbrowser.open(read_links))
        read_links_button.pack(padx=10, pady=10, fill = "x", expand=True)

class Profile(ctk.CTkToplevel):
    def __init__(self, master, logged_account, *args, **kwargs):
        super().__init__(master)
        self.logged_account = account.get_user(logged_account)
        self.title("Account")

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
                                   text=f"Tempat, Tanggal Lahir\t: {self.logged_account['content']['tempat']}, {self.logged_account['content']['tanggalLahir']}/{self.logged_account['content']['bulanLahir']}/{self.logged_account['content']['tahunLahir']}", wraplength=380, anchor="nw")
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
                                   text=f"Tempat, Tanggal Lahir\t: {self.logged_account['content']['tempat']}, {self.logged_account['content']['tanggalLahir']}/{self.logged_account['content']['bulanLahir']}/{self.logged_account['content']['tahunLahir']}", wraplength=380, anchor="nw", height=20)
        lahir_label.grid(row=2, column=0, padx=10, pady=3, sticky="nsew")

        # buttons
        edit_name_button = ctk.CTkButton(container, text="Edit", command=self.edit_name)
        edit_name_button.grid(row=1, column=1, padx=10, pady=10, sticky="nse")

        edit_tempat_tanggal_lahir_button = ctk.CTkButton(container, text="Edit", command=self.edit_tempat_tanggal_lahir)
        edit_tempat_tanggal_lahir_button.grid(row=2, column=1, padx=10, pady=10, sticky="nse")

        back_button = ctk.CTkButton(container, text="Back", command=self.back)
        back_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def edit_email(self):
        _edit(self, "email")

    def edit_name(self):
        pass

    def edit_tempat_tanggal_lahir(self):
        pass

    def back(self):
        self.widget()

    def bookshelf(self):
        pass

    def change_password(self):
        pass

    def logout(self):
        self.destroy()
        self.master.destroy()

class _edit(ctk.CTkToplevel):
    def __init__(self, master, target, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.target = target
        self.geometry("500x300")

        self.title("Edit {target}")

        label = ctk.CTkLabel(self, text=f"Edit {target}")
        label.pack(side="left", padx=3, pady=3, fill="both", expand=True)

        entry = ctk.CTkEntry(self)
        entry.pack(side="left", padx=3, pady=3, fill="both", expand=True)

        button = ctk.CTkButton(self, text="Save", command=self.save)
        button.pack(padx=3, pady=3, fill="both", expand=True)

    def save(self):
        pass
    
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # TODOS
    # 1. BUAT FUNCTION SAVE CHANGE DI MAIN + DI ACCOUNT
    # 2. ISI BOOKSHELF
    # 3. BUTTON SIMPAN BUKU MASUK KE BOOKSHELF
    # 4. FITUR REGISTER

if __name__ == "__main__":
    app = Main()
    app.run()
