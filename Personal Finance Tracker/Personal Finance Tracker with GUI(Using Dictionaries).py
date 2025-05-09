import json

from datetime import datetime

import tkinter as tk
from Enhanced_Personal_Financial_Tracker import main

#create a empty dictionary
transactions = {}

# Function to get valid date from user
def get_valid_date(prompt):
    while True: # This program run while this program true
        try:
            value = str(input(prompt)) # prompt message display to user
            date = datetime.strptime(value,"%Y-%m-%d") # check date is valid or invalid
            check_date =date.strftime("%Y-%m-%d") # get date only. remove time
            return check_date #return valid date
        except ValueError:
            print("ERROR: Invalid date...!!") # if user entered invalid date, display message to user

# Function to get string value from user
def get_str_value(prompt):
    while True: # This program run while this program true
        try:
            value = str(input(prompt)) # prompt message display to user
            return value  # return string value entered by user
        except ValueError:
            print("Error: Value Error..! Invalid Input")  # If user entered other data type ,display message to user

# Function to get integer value from user
def get_int_value(prompt):
    while True: # This program run while this program true
        try:
            value = int(input(prompt))  # prompt message display to user
            return value  # return integer value entered by user
        except ValueError:
            print("Error: Value Error..! Invalid Input")   # If user entered other data type ,display message to user

# Function to get float value from user
def get_float_value(prompt):
    while True:   # This program run while this program true
        try:
            value = float(input(prompt))  # prompt message display to user
            return value  # return float value entered by user
        except ValueError:
            print("Error: Value Error..! Invalid Input")   # If user entered other data type ,display message to user

# Function to get transaction type
def get_transaction_type(prompt):
    while True:
        transaction_type = str(input(prompt)).upper()  # prompt message display to user
        if transaction_type == "EXPENSE" or transaction_type == "INCOME":   # check transaction type is income or expense
            return transaction_type # return transaction type entered by user
        else:
            print("Error: Invalid transaction type..!")  # If user entered invalid transaction type ,display message to user

# Function to load transactions to program
def load_transactions():
    global transactions # transactions use globally
    try:
        with open ("financial_data_new.json","r") as file:      # open and read json file
            transactions =json.load(file)      # load data in json file to transactions dictionary

    except json.JSONDecodeError:  # exception JSONDecodeError
        with open ("financial_data_new.json","w") as file:  # open and write json file
            json.dump(transactions,file)   # save transactions dictionary to json file
    except FileNotFoundError:  # exception File not found
        with open ("financial_data_new.json","w") as file: # create a json file
            print("File is not found..! Create a new file..!")  # display message to user

# Function to save transactions to program
def save_transactions():
    with open ("financial_data_new.json","w") as file: # open and write json file
        json.dump(transactions,file,indent=1)  # save data to json file
        print("!!!!<<<<....TRANSACTIONS SAVE SUCCESSFULLY....>>>>!!!!")  # display message to user

# Function to get transactions from text file to program
def read_bulk_transactions(file_name):
    global transactions
    try:
        with open (file_name,"r") as file:  # open and read json file
            for line in file:  # read json file line by line
                data_line = line.strip().split(',')  # Extracting group parts separated by ',' in the line
                category = data_line[2].strip().upper()  # get above parts's data calling from index numbers
                date = data_line[0].strip()         # get above parts's data calling from index numbers
                try:
                    check_date = datetime.strptime(date,"%Y-%m-%d")   # check date is valid or invalid
                    valid_date = check_date.strftime("%Y-%m-%d")     # get date only. remove time
                    transaction_type = data_line[1].strip().upper()   # get above parts's data calling from index numbers
                    if transaction_type == "INCOME" or transaction_type == "EXPENSE": # check transaction type is income or expense
                        description = data_line[3].strip().upper()   # get above parts's data calling from index numbers
                        amount = float(data_line[4])   # get above parts's data calling from index numbers
                        transaction = {"Date" :valid_date, "Transaction_type":transaction_type, "Description" :description, "Amount" :amount }  # add date, transaction type, description, amount to transaction dictionary
                        if category in transactions: # check category in transactions dictionary
                            transactions[category].append(transaction) # if category in transactions dictionary, add transaction dictionary to it
                        else :
                            transactions[category] = [transaction] # if not category in transactions dictionary, create category and add transaction dictionary to it
                    else:
                        return print("ERROR : Invalid transaction type in text file...!! Check text file..!")  # if have invalid transaction type in text file, display message
                except ValueError:    # if have invalid date in text file,
                    return print("ERROR : date in text file...!! Check text file..!")  # display message
        print("!!..FILE IMPORT SUCCESSFULLY..!!")
        save_transactions()
    except FileNotFoundError:
        print("File is not found...!")   # if text file is not found ,display message

# Function to add transactions
def add_transaction():
    global transactions
    date = get_valid_date("Enter date(YYYY-MM-DD):")   # get valid date
    transaction_type = get_transaction_type("Enter new transaction_type (EXPENSE/INCOME):")   # get valid transaction type
    category = get_str_value("Enter new transaction category (BILLS,SALARIES,....ETC):").upper()       # get transaction category
    description = get_str_value("Enter short description about new transaction:").upper()    # get description about transaaction
    amount = get_float_value("Enter new transaction amount:")   # get transaction amount
    transaction = {"Date" :date, "Transaction_type":transaction_type, "Description" :description, "Amount" : amount}   # add date, transaction type, description, amount to transaction dictionary
    if category in transactions:   # check category in transactions dictionary
        transactions[category].append(transaction)  # if category in transactions dictionary, add transaction dictionary to it
    else:
        transactions[category] = [transaction]   # if not category in transactions dictionary, create category and add transaction dictionary to it

    print("!!!!<<<<....TRANSACTION ADD SUCCESSFULLY....>>>>!!!!")
    save_transactions()

# Function to view transactions
def view_transactions():
    global transactions
    print("                   !!!!<<<<....YOUR TRANSACTIONS HISTORY....>>>>!!!!")
    if transactions == {} or transactions == None:  # check transactions is available in file
        return print("No transactions...!! File is empty...!!") # if transactions is unavailable, display message
    for category, items in transactions.items():  # access items in transactions dictionary
        print(f"{category}:")
        count = 0
        for item in items:
            count +=1
            print(f"({count}) | Date: {item["Date"]} | Transaction type: {item["Transaction_type"]} | Description: {item["Description"]} | Amount: {item["Amount"]}")

# Function to update transactions
def update_transactions():
    print("                   !!!!<<<<....YOUR TRANSACTION UPDATE....>>>>!!!!")
    view_transactions()
    category = get_str_value("Enter category of transaction to be update:").upper()  # get we want to update category
    if category in transactions:  # check this category in transactions dictionary
        update_transaction_index = get_int_value("Enter update transaction line number:") # get we want to update line number
        if update_transaction_index >=1 and update_transaction_index <= len(transactions[category]): # check line number
            actual_transaction_index = update_transaction_index -1
            date = get_valid_date("Enter date(YYYY-MM-DD):")  # get valid date
            transaction_type = get_transaction_type("Enter transaction_type (EXPENSE/INCOME):")   # get valid transaction type
            description = get_str_value("Enter short description about transaction:").upper()    # get description about transaaction
            amount = get_float_value("Enter amount:")   # get transaction amount
            transactions[category][actual_transaction_index] = {"Date" :date, "Transaction_type":transaction_type, "Description" :description, "Amount" : amount}     # update relevant line
            print("!!!!<<<<....TRANSACTION UPDATE SUCCESSFULLY....>>>>!!!!")
            save_transactions()
        else:
            print("Error: Invalid Index..!!")
    else:
        print("Error: category is not found..!!")

# Function to delete transactions
def delete_transactions():
    print("                   !!!!<<<<....YOUR TRANSACTION DELETE....>>>>!!!!")
    view_transactions()
    category = get_str_value("Enter category of transaction to be delete:").upper()   # get we want to delete category
    if category in transactions:  # check this category in transactions dictionary
        delete_transaction_index = get_int_value("Enter delete line's number:")    # get delete line number
        if delete_transaction_index >=1 and delete_transaction_index <= len(transactions[category]):    # check line number
            actual_delete_transaction_index = delete_transaction_index -1
            del transactions[category][actual_delete_transaction_index]     # delete line
            if transactions[category] == []:  # if category is null, delete category
                del transactions[category]
                print("!!!!<<<<....TRANSACTION DELETE SUCCESSFULLY....>>>>!!!!")
                save_transactions()
            else:
                print("!!!!<<<<....TRANSACTION DELETE SUCCESSFULLY....>>>>!!!!")
                save_transactions()
        else:
            print("Error: Invalid Index..!!")
    else:
        print("ERROR: category is not found..!!")

# Function to display summary
def display_summary():
    global transactions
    total_income = 0
    total_expense = 0
    for category,items in transactions.items():
       for item in items:
           if item["Transaction_type"] == "INCOME" :
               total_income += item["Amount"]
           else:
               total_expense += item["Amount"]
    print("!!-----------------TRANSACTION SUMMARY-----------------!!")
    print(f"Total Income  : {total_income}")
    print(f"Total Expense : {total_expense}")
    print(f"NET INCOME    : {total_income-total_expense}")
    print("--------------------------------------------------------")

#Function for main menu
def main_menu():
    load_transactions() # Load transaction to start
    while True:
        print("\n===================== Personal Finance Tracker =====================")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Import Transactions in text file")
        print("7. Exit")
        choice = get_int_value("Enter your choice: ")

        if choice == 1:
            add_transaction()
        elif choice == 2:
            main()
        elif choice == 3:
            update_transactions()
        elif choice == 4:
            delete_transactions()
        elif choice == 5:
            display_summary()
        elif choice == 6:
            print("                   !!!!<<<<....YOUR TRANSACTION IMPORT....>>>>!!!!")
            file_name = get_str_value("Enter text file name:")  # get import text file
            read_bulk_transactions(file_name)
        elif choice == 7:
            save_transactions()
            print("!!!!..........Exiting Program..........!!!!")
            print("========================================================================")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()