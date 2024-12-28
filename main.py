import io
import customtkinter as ctk
import tkinter as tk
from google_books_api import *
from PIL import Image, ImageTk
import urllib.request

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
        top_frame.pack(padx = 3, pady = 3, fill="x", expand = False)

        self.middle_frame = ctk.CTkScrollableFrame(self.root)
        self.middle_frame.pack(padx = 3, pady = 3, fill="both", expand = True)
        self.middle_frame.columnconfigure((0, 1), weight=1, uniform="column")

        bottom_frame = ctk.CTkFrame(self.root, height = 50)
        bottom_frame.pack(padx = 3, pady = 3, fill="x", expand = False)

        # Top Frame Content
        self.search_entry = ctk.CTkEntry(top_frame, placeholder_text="Search for a book", width=250)
        self.search_entry.pack(pady=5)

        self.search_button = ctk.CTkButton(top_frame, text="Search", command=self.search_books, width=250)
        self.search_button.pack(pady=5)

        # Middle Frame Content
        if self.books is not None:
            self.generate_card()

        # Bottom Frame Content
        self.previous_button = ctk.CTkButton(bottom_frame, text="Previous", command=self.previous, state="disabled")
        self.previous_button.pack(side="left", padx=5)

        self.next_button = ctk.CTkButton(bottom_frame, text="Next", command=self.next, state="disabled")
        self.next_button.pack(side="left", padx=5)

        self.profile_button = ctk.CTkButton(bottom_frame, text="Profile", command=self.profile)
        self.profile_button.pack(side="right", padx=5)


    def search_books(self):
        self.books = get_book(self.search_entry.get())
        self.cursor = 0
        self.next_button.configure(state="normal")
        self.generate_card()

    def generate_card(self):
        for widget in self.middle_frame.winfo_children():
            widget.destroy()

        print(len(self.books["items"]))
        self.cards = []
        
        for row in range(0, int(self.max_cards / 2)):
            for col in range(2):
                book = self.books["items"][self.cursor]

                # thumbnail
                image_url = book["volumeInfo"]["imageLinks"]["smallThumbnail"]
                try:
                    with urllib.request.urlopen(image_url) as u:
                        raw_data = u.read()
                except Exception as e:
                    print(f"Error fetching image: {e}")
                    continue

                try:
                    image = Image.open(io.BytesIO(raw_data))
                    photo = ImageTk.PhotoImage(image)
                except Exception as e:
                    print(f"Error opening image: {e}")
                    continue

                title = book["volumeInfo"]["title"]
                page = book["volumeInfo"]["pageCount"]

                card = ctk.CTkFrame(self.middle_frame, height=500, border_color="black", border_width=1, corner_radius=16)
                card.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

                # Image side top
                image_label = ctk.CTkLabel(card, image=photo, text = "")
                image_label.pack(side="top", pady = 10)

                # Details side bottom
                page_label = ctk.CTkLabel(card, text=page)
                page_label.pack(side = "bottom", pady = 5)
                title_label = ctk.CTkLabel(card, text=title)
                title_label.pack(side = "bottom", pady = 3)

                self.cursor += 1
                print(self.cursor)
                self.cards.append(card)

            # print(row)

    def next(self):
        self.generate_card()

        if self.cursor == len(self.books["items"]):
            self.next_button.configure(state="disabled")
            self.previous_button.configure(state="normal")
        else:
            self.next_button.configure(state="normal")
            self.previous_button.configure(state="normal")

    def previous(self):
        self.cursor -= 20
        self.generate_card()

        if self.cursor == 0:
            self.next_button.configure(state="normal")
            self.previous_button.configure(state="disabled")
        else:
            self.next_button.configure(state="normal")
            self.previous_button.configure(state="normal")
    
    def profile(self):
        pass

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()