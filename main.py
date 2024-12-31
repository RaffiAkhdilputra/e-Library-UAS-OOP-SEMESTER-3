import io
import customtkinter as ctk
import tkinter as tk
from google_books_api import *
from PIL import Image, ImageTk
import urllib.request

logged_account = None

class App:

    def __init__(self):
        self.max_cards = 10
        self.cursor = 0

        self.root = ctk.CTk()
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.books = None

        self.root.title("e-Library")
        self.widgets()

    def widgets(self):
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

        # Bottom Frame Content
        self.previous_button = ctk.CTkButton(bottom_frame, text="Previous", command=self.previous, state="disabled")
        self.previous_button.pack(side="left", padx=5)

        self.next_button = ctk.CTkButton(bottom_frame, text="Next", command=self.next, state="disabled")
        self.next_button.pack(side="left", padx=5)

        self.profile_button = ctk.CTkButton(bottom_frame, text="Profile", command=self.open_profile)
        self.profile_button.pack(side="right", padx=5)

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

            # Add image to card
            if photo:
                image_label = ctk.CTkLabel(card, image=photo, text="")
                image_label.image = photo  # Keep reference to prevent garbage collection
                image_label.pack(side="top", pady=10)

            # Add details to card
            title_label = ctk.CTkLabel(card, text=title, wraplength=180)
            title_label.pack(side="top", pady=3)
            page_label = ctk.CTkLabel(card, text=f"Pages: {page}")
            page_label.pack(side="top", pady=3)
            view_button = ctk.CTkButton(card, text="View", command=lambda b=book, b_id=book_id: self.open_description(b, b_id))
            view_button.pack(side="top", pady=5)

            self.cards.append(card)

        if self.cursor + self.max_cards >= len(self.books["items"]):
            self.next_button.configure(state="disabled")
        if self.cursor == 0:
            self.previous_button.configure(state="disabled")

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
        pass

    def run(self):
        self.root.mainloop()

class Description(ctk.CTkToplevel):
    def __init__(self, master, book, target_id, *args, **kwargs):
        super().__init__(master)
        self.book = book
        self.target_id = target_id

        self.title("Book Description")
        self.geometry("400x300")

        # Display book details
        title = self.book["volumeInfo"].get("title", "Unknown Title")
        description = self.book["volumeInfo"].get("description", "No description available.")

        title_label = ctk.CTkLabel(self, text=title, font=("Arial", 16, "bold"), wraplength=380)
        title_label.pack(pady=10)

        description_text = ctk.CTkTextbox(self, wrap="word", height=200)
        description_text.insert("1.0", description)
        description_text.configure(state="disabled")
        description_text.pack(pady=10, padx=10, fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.run()
