import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import csv
# acquires access to code in another module through the act of importing it.




class BookManager:
    def __init__(self, csv_path=None):        # Initialize the BookManager. If a CSV file location is specified, load the books from it; otherwise, start with an empty dictionary.
        self.books = self.load_books_from_csv(csv_path) if csv_path else {}

    def load_books_from_csv(self, filepath):   # Create an empty dictionary for storing books. Each key is a book title, while the value is a collection of book-related facts.
        books = {}
        # Open the CSV file in read mode using the specified filepath, assuring correct handling of newline characters and UTF-8 encoding.
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            # Create a CSV reader that process from the opened file.
            reader = csv.reader(csvfile)
            # Iterate over each row of the CSV file. Every row represents a book.
            for row in reader:
                title = row[0]  # The first column of each row is presumed to represent the book's title.
                content = row[1:] # The remaining columns are thought to include information on the book.
                books[title] = content  # Save the details in the dictionary with the title as the key.
        return books  # Return the dictionary with all of the books and their information.

    def get_book_titles(self):
        # Return the list of all book titles. The titles serve as the keys in the 'books' dictionary.
        return list(self.books.keys())

    def get_page(self, book_title, page_num):
        # The method fetches a specific page from a book by verifying if the book title is in the dictionary 'books'
        # And returning the page at the provided index (page_num), or None if it is not found.
        return self.books[book_title][page_num] if book_title in self.books else None

    def get_book_length(self, book_title):
        # This function determines the number of pages in a book by verifying if the book title appears in the dictionary 'books'. If it does, it returns the length of the list connected with the book title,
        # Which represents the number of pages. If no matches are discovered, 0 is returned as the default value.
        return len(self.books[book_title]) if book_title in self.books else 0
class UIManager:
    def __init__(self, master, book_manager):
        # Constructor for the UIManager class. It takes a master widget (often the main application window) and a book management object.
        self.master = master # This is usually the primary window of the application.
        self.book_manager = book_manager# The book manager object, which manages book data operations.
        self.setup_ui()  # Use the setup_ui function to create and organize UI components in the window.

    def setup_ui(self):
        # Configure the user interface components in the master widget.

        # Create a label widget in the title area that instructs the user to select a book.
        self.title_label = tk.Label(self.master, text="Choose a book", font=("Arial", 16))
        self.title_label.pack(padx=10, pady=10)  # Insert the label into the master widget with appropriate padding.

        # Create a combobox widget that lets users choose a book from a dropdown list.
        # This list is filled using titles retrieved from the book manager.
        self.book_selector = ttk.Combobox(self.master, values=self.book_manager.get_book_titles(), state="readonly")
        self.book_selector.pack(padx=8, pady=8)  # Fill the combobox with padding to make it visible and well-spaced.

        # Make a label to indicate which book is selected.
        self.selected_book_label = tk.Label(self.master, text="Selected Book: ", font=("Arial", 12))
        self.selected_book_label.pack(padx=10, pady=(0, 5), anchor=tk.W) # Position this label near the combobox, aligned to the west.

        # Create a scrollable text section to display the content of the chosen book.
        # The text section is set up to wrap words and use a certain font.
        self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, font=("Times New Roman", 12))
        self.text_area.pack(padx=8, pady=8, fill=tk.BOTH, expand=True)  # As the window is enlarged, the text area extends to fill the available space.
        self.text_area.config(state=tk.DISABLED) # Initially, the text field is disabled to prevent user editing.

        # Build a frame for navigation controls (such as page navigation), which may be added later.
        self.navigation_frame = tk.Frame(self.master)
        self.navigation_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=8) # Place it at the bottom of the window, covering its full width.

    def update_book_display(self, title, content, page_num):
        # Update the display with the contents of the selected book.
        # This method modifies the book title label, text area, and page number to match the currently chosen book.

        self.selected_book_label.config(text=f"Selected eBook: {title}")  # Change the text on the selected book label to include the title of the book.

        page_number = f"Page {page_num + 1}"    # Format the page number for display, correcting for zero-based indexing by adding one.

        self.text_area.config(state=tk.NORMAL)  # Turn on the text area widget to allow modifications to the displayed content.

        self.text_area.delete('1.0', tk.END)  # Remove the current content from the text field.

        self.text_area.insert(tk.END, page_number + '\n', 'center')   # Center the formatted page number in the top of the text area.

        self.text_area.insert(tk.END, content)  # Place the content of the selected page behind the page number.

        self.text_area.config(state=tk.DISABLED)  # Turn off the text box to prevent users from altering the visible information.


class KindleApp:
    def __init__(self, master, title="eBook Reader", size="485x630", csv_path=None):
        # Creates the main program window with the requested title and size, then loads books from a CSV file if one is available.

        self.master = master  # This is the application's primary window, usually a Tk root or another Tk frame.
        self.master.title(title) # Set the window title. The default is "eBook Reader".
        self.master.geometry(size) # Set the starting size of the window.
        self.master.resizable(False, False)  #This makes the gui app or window non-raisable.

        # Configure the book manager with an optional CSV path for loading books.
        self.book_manager = BookManager(csv_path)

        # Set up the user interface manager with the master widget and book manager.
        self.ui_manager = UIManager(master, self.book_manager)

        # Variables for tracking the currently chosen book and page.
        self.current_book = None # Initially, no book is chosen.
        self.current_page = 0 # Begin viewing on the first page of the book.

        # This event is triggered when the user picks a book from the menu.
        self.ui_manager.book_selector.bind("<<ComboboxSelected>>", self.update_book)

        # Include navigation buttons in the user interface, such as the next and previous page buttons.
        self.add_navigation_buttons()

        # A flag to indicate whether the dark mode is activated or not.
        self.is_dark_mode = False  # Dark mode is disabled by default.

    def add_navigation_buttons(self):
        # This method adds navigation and control buttons to the user interface, including a 'Previous' button that navigates to the book's previous page and is linked to the 'go_previous' function.
        self.prev_button = tk.Button(self.ui_manager.navigation_frame, text="Previous", command=self.go_previous)
        # Fill in the 'Previous' button on the left side of the navigation frame with the desired padding.
        self.prev_button.pack(side=tk.LEFT, padx=(20, 10))

        # Add a 'Next Page' button to browse to the next page of the book.
        # It is attached to the 'go_next' function, which controls what happens when this button is pressed.
        self.next_button = tk.Button(self.ui_manager.navigation_frame, text="Next Page", command=self.go_next)
        # Place the 'Next Page' button next to the 'Previous' button on the left side, with the supplied padding.
        self.next_button.pack(side=tk.LEFT, padx=(10, 20))

        # This adds a 'Exit' button to exit the application.
        # And it's tied to the master widget's 'destroy' method, which causes the program to finish.
        self.mode_button = tk.Button(self.ui_manager.navigation_frame, text="Dark Mode", command=self.toggle_mode)
        self.mode_button.pack(side=tk.RIGHT, padx=(10, 20)) # Position the 'Dark Mode' button on the right side of the navigation frame, with the required padding.

        # This Creates a 'Exit' button to exit the application. It is bound to the master widget's 'destroy' method, which terminates the application.
        self.exit_button = tk.Button(self.ui_manager.navigation_frame, text="Exit", command=self.master.destroy)

        self.exit_button.pack(side=tk.RIGHT, padx=(20, 10))# Use the provided padding to pack the 'Exit' button next to the 'Dark Mode' button on the right.

    def toggle_mode(self):
        # Change the dark mode status. This boolean flag is switched every time the method is invoked.
        self.is_dark_mode = not self.is_dark_mode

        # Verify that dark mode is now enabled.
        if self.is_dark_mode:
            self.master.configure(background="gray20") # Set the main application window's backdrop to a darker tint ('gray20').

            # Update UI components to dark mode themes with 'gray20' backgrounds and 'white' text for greater contrast in dark mode.
            self.ui_manager.title_label.configure(background="gray20", foreground="white")
            self.ui_manager.selected_book_label.configure(background="gray20", foreground="white")
            self.ui_manager.text_area.configure(background="black", foreground="white")
            self.ui_manager.navigation_frame.configure(background="gray20")

            # Set buttons to a little lighter shade of gray ('gray30') than the background, with white text for all.
            self.prev_button.configure(background="gray30", foreground="white")
            self.next_button.configure(background="gray30", foreground="white")
            self.mode_button.configure(background="gray30", foreground="white")
            self.exit_button.configure(background="gray30", foreground="white")
            self.ui_manager.book_selector.configure(background="gray30", foreground="white")
        else:
            # If dark mode is deactivated, return the UI components to the default system colors. and backgrounds are set to 'SystemButtonFace', a default light mode color, with text set to 'black' for all.
            self.master.configure(background="SystemButtonFace")
            self.ui_manager.title_label.configure(background="SystemButtonFace", foreground="black")
            self.ui_manager.selected_book_label.configure(background="SystemButtonFace", foreground="black")
            self.ui_manager.text_area.configure(background="white", foreground="black")
            self.ui_manager.navigation_frame.configure(background="SystemButtonFace")

            # Set the button look to match the system's default, with black text. for all
            self.prev_button.configure(background="SystemButtonFace", foreground="black")
            self.next_button.configure(background="SystemButtonFace", foreground="black")
            self.mode_button.configure(background="SystemButtonFace", foreground="black")
            self.exit_button.configure(background="SystemButtonFace", foreground="black")
            self.ui_manager.book_selector.configure(background="white", foreground="black")

    def update_book(self, event):
        # This function is invoked when the combobox selection changes. Additionally, it refreshes the current book and resets the page counter.
        self.current_book = self.ui_manager.book_selector.get() # Take the currently chosen book from the combobox.
        self.current_page = 0  # Reset the page number to start at the beginning of the book.
        self.load_page()  # Load the first page of the specified book.

    def load_page(self):
        # Retrieve and show the current page of the specified book.
        content = self.book_manager.get_page(self.current_book,self.current_page) # Retrieve the page contents from the book management.

        if content:
            # If content exists, update the UI to show the book's current page.
            self.ui_manager.update_book_display(self.current_book, content, self.current_page)
        else:
            # If no material is discovered (e.g., book not found or empty), show an error message.
            messagebox.showerror("Error", "Book not found or no content available.")

    def go_next(self):
        # If you are not on the last page of the book, move on to the next one. Check to see if the current page is less than the book's total number of pages minus one.
        if self.current_page < self.book_manager.get_book_length(self.current_book) - 1:
            self.current_page += 1  # Increase the page number.
            self.load_page()  # Load the content for the new page.

    def go_previous(self):
        # If you are not on the opening page of the book, navigate to the previous page.
        if self.current_page > 0:
            self.current_page -= 1  # Decrease the page number.
            self.load_page()  # Load the content for the new page.


