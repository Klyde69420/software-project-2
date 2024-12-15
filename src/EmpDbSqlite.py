'''
This is the interface to an SQLite Database
'''

import sqlite3

class EmpDbSqlite:
    def __init__(self, dbName='Employees.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS item (
                id TEXT PRIMARY KEY,
                item TEXT,
                price TEXT,
                quantity TEXT,
                status TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute()
        self.commit_close()

    def fetch_item(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM items')
        items =self.cursor.fetchall()
        self.conn.close()
        return items

    def insert_item(self, id, item, price, quantity, status):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO items (id, id, price, quantity, status) VALUES (?, ?, ?, ?, ?)',
                    (id, item, price, quantity, status))
        self.commit_close()

    def delete_item(self, id):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM items WHERE id = ?', (id,))
        self.commit_close()

    def update_item(self, new_item, new_price, new_quantity, new_status, id):
        self.connect_cursor()
        self.cursor.execute('UPDATE items SET name = ?, role = ?, gender = ?, status = ? WHERE id = ?',
                    (new_item, new_price, new_quantity, new_status, id))
        self.commit_close()

    def id_exists(self, id):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM items WHERE id = ?', (id,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            dbEntries = self.fetch_item()
            for entry in dbEntries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]}\n")

def test_EmpDb():
    iEmpDb = EmpDbSqlite(dbName='EmpDbSql.db')

    for entry in range(30):
        iEmpDb.insert_item(entry, f'Item{entry} Item name{entry}', f'Price {entry}', '0 PHP', 'NOT FOR SALE')
        assert iEmpDb.id_exists(entry)

    all_entries = iEmpDb.fetch_item()
    assert len(all_entries) == 30

    for entry in range(10, 20):
        iEmpDb.update_item(f'Item{entry} Price{entry}', f'Price {entry}', 'Quantity', 'NOT FOR SALE', entry)
        assert iEmpDb.id_exists(entry)

    all_entries = iEmpDb.fetch_item()
    assert len(all_entries) == 30

    for entry in range(10):
        iEmpDb.delete_item(entry)
        assert not iEmpDb.id_exists(entry) 

    all_entries = iEmpDb.fetch_item()
    assert len(all_entries) == 20