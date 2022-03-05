from openpyxl import load_workbook
from dataclasses import dataclass
import os

from models import Accounts, Purchases, Supplier


@dataclass
class RecordPurchases:
    db: any
    filename: str
    header_row: int = 4

    def __post_init__(self):
        wb = load_workbook(self.filename, data_only=True)

        for sheet_name in wb.sheetnames:
            self.process_sheet(wb[sheet_name])

    def process_sheet(self, ws):
        self.ws = ws

        self.column_headers = [self.ws.cell(row=self.header_row, column=column).value
                                for column in range(1, len(list(self.ws.columns)) + 1)
                           ]

        # Get saved account headers
        self.account_headers = [i[0] for i in self.db.execute("SELECT account_tag FROM tbl_accounts;").fetchall()]

        # Get saved purchases headers
        self.purchases_header_path = os.path.join('instance', 'purchases_headers')
        if os.path.isfile(self.purchases_header_path):
            with open(self.purchases_header_path) as file:
                self.purchases_headers = [x.replace('\n', '') for x in file.readlines()][:-1]
        else:
            self.purchases_headers = []

        # Get saved supplier headers
        self.supplier_header_path = os.path.join('instance', 'supplier_headers')
        if os.path.isfile(self.supplier_header_path):
            with open(self.supplier_header_path) as file:
                self.supplier_headers = [x.replace('\n', '') for x in file.readlines()][:-1]
        else:
            self.supplier_headers = []

        self.process_column_headers()
        self.record_entries()


    def process_column_headers(self):
        choices = {str(header[0]+1): header[1] for header in enumerate(
            ('account_headers',
             'supplier_headers',
             'purchases_headers')
        )}

        for column_head in self.column_headers:
            if column_head not in self.account_headers + self.purchases_headers + self.supplier_headers \
                    and column_head is not None:
                header_type = ""
                print(choices)
                while header_type not in choices:
                    print(f"Header not in record: {column_head}")
                    header_type = input("Header type: \n")

                if choices[header_type] == 'account_headers':
                    # Saved account headers
                    self.account_headers.append(column_head)
                    account = Accounts(
                        db=self.db,
                        account_tag=column_head,
                        account_number=input("Account Number: \n"),
                        account_title=input("Account Title: \n"),
                        vat_class=input("VAT Class: \n"),
                        wt_class=input("WT Class: \n"),
                    )
                    account.save
                elif choices[header_type] == 'purchases_headers':
                    # Saved purchases headers
                    self.purchases_headers.append(column_head)
                    if os.path.isfile(self.purchases_header_path):
                        with open(self.purchases_header_path, 'a') as file:
                            file.write(f'{column_head}\n')
                    else:
                        with open(self.purchases_header_path, 'w') as file:
                            file.write(f'{column_head}\n')
                elif choices[header_type] == 'supplier_headers':
                    # Saved supplier headers
                    self.supplier_headers.append(column_head)
                    if os.path.isfile(self.supplier_header_path):
                        with open(self.supplier_header_path, 'a') as file:
                            file.write(f'{column_head}\n')
                    else:
                        with open(self.supplier_header_path, 'w') as file:
                            file.write(f'{column_head}\n')

                print()
                print()

    def record_entries(self):
        row_nums = range(self.header_row + 1, len(list(self.ws.rows))+1)
        columns = range(1, len(list(self.ws.columns)))

        receiving_date = str(self.ws.cell(row=self.header_row + 1, column=1).value)[:10]
        for row in row_nums:
            supplier = {}
            purchases = {}
            accounts = {}
            for column in columns:
                cell_value = self.ws.cell(row=row, column=column).value
                tag = self.ws.cell(row=self.header_row, column=column).value

                if tag in self.supplier_headers:
                    supplier[tag] = cell_value
                elif tag in self.purchases_headers:
                    if tag == 'Receiving Date':
                        if cell_value is None:
                            purchases[tag] = receiving_date
                        else:
                            purchases[tag] = receiving_date = str(cell_value)[:10]
                    else:
                        purchases[tag] = cell_value
                else:
                    if cell_value:
                        accounts[tag] = cell_value

            supplier_id = self.record_supplier(supplier)
            self.record_purchases(purchases, accounts, supplier_id)

    def record_supplier(self, supplier):
        supplier_name = supplier['Supplier Name']
        supplier_tin = supplier['TIN']

        supplier = Supplier(db=self.db)
        if not self.db.execute('SELECT COUNT(*) FROM tbl_supplier WHERE supplier_name=?',
                               (supplier_name,)).fetchone()[0]:
            supplier.supplier_name = supplier_name
            supplier.supplier_tin = supplier_tin
            supplier.save
            print("Added ", supplier)

        else:
            supplier.get(supplier_name=supplier_name)

        return supplier.id

    def record_purchases(self, purchases, accounts, supplier_id):
        received_date = purchases['Receiving Date']
        rr_number = str(purchases['RR Number'])
        po = str(purchases['PO'])
        invoice = str(purchases['Invoice Number'])
        particulars = purchases['Particulars']
        invalid = purchases['Invalid'] if purchases['Invalid'] is not None else 0.0
        vat_zero_rated = purchases['VAT Zero-Rated'] if purchases['VAT Zero-Rated'] is not None else 0.0
        vat_exempt = purchases['VAT Exempt'] if purchases['VAT Exempt'] is not None else 0.0
        vat_12 = purchases['VAT 12%'] if purchases['VAT 12%'] is not None else 0.0
        ewt_rate = purchases['EWT Rate'] if purchases['EWT Rate'] is not None else 0.0

        tag = [account_tag for account_tag, value in accounts.items()
               if account_tag not in ('Input VAT', 'EWT', 'Accounts Payable')][0]

        account_id = self.db.execute('SELECT id FROM tbl_accounts WHERE account_tag=?',
                                                  (tag, )).fetchone()[0]

        purchase = Purchases(
            db=self.db,
            received_date=received_date,
            rr_number=rr_number,
            po=po,
            invoice=invoice,
            particulars=particulars,
            invalid=invalid,
            vat_zero_rated=vat_zero_rated,
            vat_exempt=vat_exempt,
            vat_12=vat_12,
            ewt_rate=ewt_rate,
            supplier_id=supplier_id,
            account_id=account_id,
        )

        if not self.db.execute('SELECT COUNT(*) FROM tbl_purchases WHERE rr_number=?', (rr_number, )).fetchone()[0]:
            purchase.save
            print(f"Added {purchase}")
        else:
            suffix = input(f'Duplicate RR Number detected {rr_number}. Press enter to pass.')
            if suffix:
                purchase.rr_number += suffix
                purchase.save
                print(f"Added {purchase}")
