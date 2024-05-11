from kindle import KindleApp # Import the KindleApp class from the Kindle module to manage the eBook reading functionality.
# Import the tkinter library, which is used to create graphical user interfaces using Python.
import tkinter as tk

def main():
    # This method initializes the main program window and launches the GUI event loop.
    # Create the application's root window with Tkinter's Tk class.
    root = tk.Tk()
    # Create a KindleApp instance, using the root window as the master.
    # Set particular settings, such as the window title and size, as well as the CSV file location for loading books.
    app = KindleApp(master=root, title="eBook", size="485x630", csv_path="books.csv")

    # Start the tkinter event loop, which listens for user input such as button clicks or key presses.
    root.mainloop()

if __name__ == '__main__':  #checks if the script is being run as the main program.
    main()
