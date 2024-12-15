class StorageDbEntry:
    def __init__(self,
                 id=1,
                 item='Ballpen name or Brand',
                 price='20 PHP',
                 quantity='20 PCS',
                 status='FOR SALE'):
        self.id = id
        self.item = item
        self.price = price
        self.quantity = quantity
        self.status = status
