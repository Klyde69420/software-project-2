from StorageDbEntry import StorageDbEntry
import csv  # For CSV export
from tkinter import Tk, Label, filedialog


class StorageDb:
    def __init__(self, init=False, dbName='EmpDb.csv'):
        """
        Initialize the database with an optional file name.
        """
        self.dbName = dbName
        self.items = []  

    def fetch_employees(self):
        """
        Return a list of tuples containing employee data.
        """
        return [(unique.id, unique.item, unique.price, unique.quantity, unique.status) for unique in self.items]

    def insert_employee(self, id, item, price, quantity, status):
        """
        Add a new employee entry.
        """
        if self.id_exists(id):
            print(f"Error: Item with ID {id} already exists.")
            return

        new_entry = StorageDbEntry(id=id, item=item, price=price, quantity=quantity, status=status)
        self.items.append(new_entry)
        print(f"Item {item} added successfully.")

    def delete_employee(self, id):
        """
        Delete an employee by ID.
        """
        for emp in self.items:
            if emp.id == id:
                self.items.remove(emp)
                print(f"Item with ID {id} deleted successfully.")
                return
        print(f"Error: Item with ID {id} not found.")

    def update_employee(self, new_item, new_price, new_quantity, new_status, id):
        """
        Update an employee's details.
        """
        for emp in self.items:
            if emp.id == id:
                emp.item = new_item
                emp.price = new_price
                emp.quantity = new_quantity
                emp.status = new_status
                print(f"Item with ID {id} updated successfully.")
                return
        print(f"Error: Item with ID {id} not found.")

    def export_csv(self):
        """
        Export employee data to a CSV file.
        """
        with open(self.dbName, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Item', 'Price', 'Quantity', 'Status'])
            for emp in self.items:
                writer.writerow([emp.id, emp.item, emp.price, emp.quantity, emp.status])
        print(f"Employee data exported to {self.dbName}.")

    def id_exists(self, id):
        """
        Check if an employee with the given ID exists.
        """
        return any(emp.id == id for emp in self.items)
    
    def import_csv(self):
        filename = filedialog.askopenfilename(initialdir="/desktop/EEE 111 Folder/software project 2", title="Select a File", filetypes=(("csv", "*.csv"), ("All files", "*.*")))    
        if filename:
            self.dbName = filename
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
            next(reader) 
            for row in reader:
                self.items.append(StorageDbEntry(id=row[0], item=row[1], price=float(row[2]), quantity=int(row[3]), status=row[4]))

        

    