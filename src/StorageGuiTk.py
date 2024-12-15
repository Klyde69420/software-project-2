from tkinter import *
from tkinter import ttk, filedialog
import tkinter as tk
from tkinter import messagebox
from EmpDbSqlite import EmpDbSqlite
from PIL import Image, ImageTk

class StorageGuiTk(Tk):

    def __init__(self, dataBase=EmpDbSqlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

        self.attributes('-fullscreen', True)
        self.bind('<Escape>', lambda e: self.attributes('-fullscreen', False))


        self.title('Employee Management System')
        self.geometry('1500x1500')
        self.config(bg='#FF7F7F')
        self.resizable(False, False)

        self.font1 = ('Helvetica', 20, 'bold')
        self.font2 = ('Helvetica', 10, 'bold')

        try:
            self.logo_image = PhotoImage(file="itim.png")
            self.logo_label = Label(self, image=self.logo_image, bg='#FF7F7F')
            # Place logo at the top-left corner
            self.logo_label.place(x=-1, y=500)
            # For middle placement, use: self.logo_label.place(relx=0.5, y=10, anchor="n")
        except Exception as e:
            print(f"Error loading logo image: {e}")
        
        # Data Entry Form
        # 'ID' Label and Entry Widgets
        self.id_label = self.newCtkLabel('ID')
        self.id_label.place(x=20, y=40)
        self.id_entryVar = StringVar()
        self.id_entry = self.newCtkEntry(entryVariable=self.id_entryVar)
        self.id_entry.place(x=100, y=40)

        # 'Name' Label and Entry Widgets
        self.item_label = self.newCtkLabel('Item')
        self.item_label.place(x=20, y=100)
        self.item_entryVar = StringVar()
        self.item_entry = self.newCtkEntry(entryVariable=self.item_entryVar)
        self.item_entry.place(x=100, y=100)

        # 'Role' Label and Combo Box Widgets
        self.price_label = self.newCtkLabel('Price')
        self.price_label.place(x=20, y=160)
        self.price_cboxVar = StringVar()
        self.price_cboxOptions = ['10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60', '65', '70', '75', '80', '85', '90', '95', '100']
        self.price_cbox = self.newCtkComboBox(options=self.price_cboxOptions, 
                                    entryVariable=self.price_cboxVar)
        self.price_cbox.place(x=100, y=160)

        # 'Gender' Label and Combo Box Widgets
        self.quantity_label = self.newCtkLabel('Quantity')
        self.quantity_label.place(x=20, y=220)
        self.quantity_cboxVar = StringVar()
        self.quantity_cboxOptions = ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100']
        self.quantity_cbox = self.newCtkComboBox(options=self.quantity_cboxOptions, 
                                    entryVariable=self.quantity_cboxVar)
        self.quantity_cbox.place(x=100, y=220)

        # 'Status' Label and Combo Box Widgets
        self.status_label = self.newCtkLabel('Status')
        self.status_label.place(x=20, y=280)
        self.status_cboxVar = StringVar()
        self.status_cboxOptions = ['ON SALE', 'NOT FOR SALE', 'OUT-OF-STOCK']
        self.status_cbox = self.newCtkComboBox(options=self.status_cboxOptions, 
                                    entryVariable=self.status_cboxVar)
        self.status_cbox.place(x=100, y=280)


        self.add_button = self.newCtkButton(text='Add Item',
                                onClickHandler=self.add_entry,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=50,y=350)

        self.new_button = self.newCtkButton(text='New Item',
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=50,y=400)

        self.update_button = self.newCtkButton(text='Update Item',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=360,y=400)

        self.delete_button = self.newCtkButton(text='Delete Item',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#E40404',
                                    hoverColor='#AE0000',
                                    borderColor='#E40404')
        self.delete_button.place(x=670,y=400)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv)
        self.export_button.place(x=980,y=400)

        self.projected_income_button = self.newCtkButton (text='Projected Income', onClickHandler=self.calculate_projected_income)
        self.projected_income_button.place(x=1200, y=400)
        self.import_button = self.newCtkButton(text='Import from CSV', onClickHandler=self.import_csv)
        self.import_button.place(x=1365, y=150)
        self.import_button = self.newCtkButton(text='Import from CSV', onClickHandler=self.import_csv)
        self.import_button.place(x=1365, y=150)
        
        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#fff',
                        background='#000',
                        fieldlbackground='#313837')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('ID', 'Item', 'Price', 'Quantity', 'Status')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.CENTER, width=10)
        self.tree.column('Item', anchor=tk.CENTER, width=150)
        self.tree.column('Price', anchor=tk.CENTER, width=150)
        self.tree.column('Quantity', anchor=tk.CENTER, width=10)
        self.tree.column('Status', anchor=tk.CENTER, width=150)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Item', text='Item') 
        self.tree.heading('Price', text='Price (PHP)')
        self.tree.heading('Quantity', text='Quantity (PCS)')
        self.tree.heading('Status', text='Status')

        self.tree.place(x=360, y=20, width=1000, height=350)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget
    def newCtkLabel(self, text='CTK Label'):
        widget_Font = self.font1
        widget_TextColor = '#FFF'
        widget_BgColor = '#161C25'

        # Apply the attributes directly
        widget = ttk.Label(self, text=text)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label', entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Font = self.font1
        widget_Width=25

        widget = ttk.Entry(self, textvariable=entryVariable, width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=25
        widget_Options=options

        widget = ttk.Combobox(self, 
                              textvariable=entryVariable,
                              width=widget_Width)
        
        # set default value to 1st option
        widget['values'] = tuple(options)
        widget.current(1)
        return widget

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#161C25', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=25
        widget_Function=onClickHandler

        widget = ttk.Button(self,
                            text=text,
                            command=widget_Function,
                            width=widget_Width)
       
        return widget

    # Handles
    def add_to_treeview(self):
        employees = self.db.fetch_employees()
        self.tree.delete(*self.tree.get_children())
        for employee in employees:
            print(employee)
            self.tree.insert('', END, values=employee)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.id_entryVar.set('')
        self.item_entryVar.set('')
        self.price_cboxVar.set('')
        self.quantity_cboxVar.set('')
        self.status_cboxVar.set('')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.id_entryVar.set(row[0])
            self.item_entryVar.set(row[1])
            self.price_cboxVar.set(row[2])
            self.quantity_cboxVar.set(row[3])
            self.status_cboxVar.set(row[4])
        else:
            pass

    def add_entry(self):
        id=self.id_entryVar.get()
        item=self.item_entryVar.get()
        price=self.price_cboxVar.get()
        quantity=self.quantity_cboxVar.get()
        status=self.status_cboxVar.get()

        if not (id and item and price and quantity and status):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.id_exists(id):
            messagebox.showerror('Error', 'ID already exists')
        else:
            self.db.insert_employee(id, item, price, quantity, status)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an Item to delete')
        else:
            id = self.id_entryVar.get()
            self.db.delete_employee(id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an Item to update')
        else:
            id=self.id_entryVar.get()
            item=self.item_entryVar.get()
            price=self.price_cboxVar.get()
            quantity=self.quantity_cboxVar.get()
            status=self.status_cboxVar.get()
            self.db.update_employee(item, price, quantity, status, id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')

    def calculate_projected_income(self):
        total_income = 0
        for child in self.tree.get_children():
            row = self.tree.item(child)['values']
            price = float(row[2])
            quantity = int(row[3])
            total_income += price * quantity
        messagebox.showinfo('Projected Income', f'Total Projected Income: PHP {total_income:.2f}')

    def import_csv(self):
        filename = filedialog.askopenfilename(initialdir="/desktop/EEE 111 Folder/software project 2", title="Select a File", filetypes=(("csv", "*.csv"), ("All files", "*.*")))    
        if filename:
            self.db.import_csv(filename)  
            self.add_to_treeview()  
            messagebox.showinfo('Success', 'Data has been imported from the CSV.')



