import threading
import sqlite3
import os

from mod_purchases import RecordPurchases
from mod_petty_cash import RecordPettyCash
from models import Accounts, Purchases, PettyCash, Supplier


if __name__ == "__main__":
    if not os.path.isdir('instance'):
        os.makedirs('instance')

    db = sqlite3.connect(os.path.join('instance', 'data.db'))
    for table in (Accounts, Purchases, PettyCash, Supplier):
        obj = table(db=db)
        try:
            obj.delete_table
            obj.create_table
        except sqlite3.OperationalError:
            pass

    supplier = Supplier(
        db=db,
        supplier_name="CANCELLED"
    )
    supplier.save

    account = Accounts(
        db=db,
        account_tag="CANCELLED",
    )

    filename = os.path.join('instance', 'uploads', 'purchases.xlsx')
    RecordPurchases(db, filename)
    #
    for name in ('pcf 2017.xlsx', 'pcf 2018.xlsx', 'pcf 2019.xlsx', 'pcf 2020.xlsx'):
        filename = os.path.join('instance', 'uploads', name)
        RecordPettyCash(db, filename)

    db.close()
