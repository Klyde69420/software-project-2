from StorageDb import StorageDb
from StorageGuiTk import StorageGuiTk

def main():
    db = StorageDb(init=False, dbName='EmpDb.csv')
    db.import_csv
    app = StorageGuiTk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()