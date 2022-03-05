
import sqlite3
import os

from mod_purchases import RecordPurchases
from models import Accounts, Purchases, Supplier


if __name__ == "__main__":
    db = sqlite3.connect(os.path.join('instance', 'data.db'))
    for table in (Purchases, Supplier):
        obj = table(db=db)
        try:
            obj.delete_table
        except sqlite3.OperationalError:
            pass

    for table in (Accounts, Purchases, Supplier):
        obj = table(db=db)
        try:
            obj.create_table
        except sqlite3.OperationalError:
            pass

    filename = os.path.join('instance', 'uploads', 'purchases.xlsx')
    data = RecordPurchases(db, filename)

    db.close()
