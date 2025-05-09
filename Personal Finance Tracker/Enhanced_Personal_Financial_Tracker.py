import tkinter as tk
from tkinter import ttk
import json
import tkinter.messagebox as mbox


class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.create_widgets()
        self.transactions = self.load_transactions()
        self.click_button = 0
    def create_widgets(self):
        # Frame for table and scrollbar
        table_box = ttk.Frame(self.root)
        table_box.pack(padx =20, pady =20, fill =tk.BOTH, expand =True)

        # Table for displaying transactions
        self.table = ttk.Treeview(table_box, columns =("Count", "Date", "Transaction_type", "Category", "Description", "Amount"), show ="headings")  # table heading
        self.table.heading("Count", text ="No.")
        self.table.column("Count", width =10)
        self.table.heading("Date", text ="Date")
        self.table.column("Date", width =50)
        self.table.heading("Category", text ="Category")
        self.table.heading("Transaction_type", text ="Transaction type")
        self.table.column("Transaction_type", width =70)
        self.table.heading("Description", text ="Description")
        self.table.heading("Amount", text="Amount")
        self.table.column("Amount", width =60)
        self.table.pack(side =tk.LEFT,fill =tk.BOTH, expand =True)

        # Table heading font decoration
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Jersey", 10, "bold"))

        # Scrollbar for the Table
        self.scroll_table = ttk.Scrollbar(table_box, orient ="vertical", command =self.table.yview)
        self.scroll_table.pack(side =tk.RIGHT, fill =tk.BOTH)
        self.table.configure(yscrollcommand=self.scroll_table.set)

        # Search bar
        search_bar_frame = ttk.Frame(self.root, borderwidth =1)
        search_bar_frame.pack(padx =5, pady =(0,5))

        # Get typed in search bar
        self.search_bar = tk.StringVar()
        search_entry = ttk.Entry(search_bar_frame, textvariable =self.search_bar, font =("Helvetica",12), width =100)
        search_entry.pack(side =tk.LEFT, padx =20, pady =5)

        # Sort button
        sort_button = ttk.Button(search_bar_frame, text="Sort", command=self.click_buuton_count, width=10)
        sort_button.pack(side =tk.RIGHT, padx =5, pady =5)

        #Search button
        search_button = ttk.Button(search_bar_frame, text ="Search", command =self.search_transactions,  width =10)
        search_button.pack(side =tk.RIGHT)


    def load_transactions(self):
        try:
            with open("financial_data_new.json", "r") as file:
                transactions = json.load(file)
                if transactions == {}: # If transaction data file is empty, display error box
                    return mbox.showerror("No transactions","No transactions in file")
                else:
                    return transactions # If transaction file has transactions data, return data
        except FileNotFoundError:
            return mbox.showerror("Error","File is not found") # If transaction file not found. Display Error box
        except json.decoder.JSONDecodeError:
            return mbox.showerror("No transactions","No transactions in file")


    def display_transactions(self):
        try:
            for category, items in self.transactions.items(): # Get category from transactions
                for item in items: # Get data in category
                    line_count = len(self.table.get_children()) + 1 # Set line count add
                    # insert data to table
                    self.table.insert("", "end", values =(line_count, item["Date"], item["Transaction_type"], category, item["Description"], item["Amount"]))
        except AttributeError:
            pass

    # Search transactions
    def search_transactions(self):
        search_text = self.search_bar.get().upper().strip() # Get string from search bar
        self.table.delete(*self.table.get_children()) # Remove transactions from table
        for category, items in self.transactions.items(): # Get category from transactions
            for item in items: # Get data in category
                # Check anything related to we are typed in search bar
                if search_text in category or search_text in item["Date"] or search_text in item["Description"] or search_text in item["Transaction_type"]:
                    line_count = len(self.table.get_children()) + 1  # Set line count add
                    # insert data to table
                    self.table.insert("","end", values =(line_count, item["Date"], item["Transaction_type"], category, item["Description"], item["Amount"]))


    def click_buuton_count(self):
        self.click_button +=1 # Add 1 to click button count
        if self.click_button == 1: # Check button count = 1
            self.sort_by_column() # Call sort function
        else:
            # Second time click sort button, Display original view
            self.table.delete(*self.table.get_children())
            self.display_transactions()
            self.click_button = 0 #set line count to 0

    def sort_by_column( self):
        date =["Date"]
        items = [(self.table.set(item, date), item) for item in self.table.get_children('')]
        items.sort()
        for index, (val, item) in enumerate(items):
            self.table.move(item, '', index)

def main():
    root = tk.Tk()
    app = FinanceTrackerGUI(root)
    app.display_transactions()
    root.mainloop()


