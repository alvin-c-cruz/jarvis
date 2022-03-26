import sqlite3
import os
import pandas as pd

YEAR = "2017"
MONTH = "12"


def sql(table_name):
    return f'''
        SELECT 
             supplier.supplier_tin,
             supplier.supplier_name,
             sum(exp.vat_exempt) as vat_exempt,
             sum(exp.vat_zero_rated) as vat_zero_rated,
             sum(exp.vat_12) as vat_12,
             account.vat_class
        FROM {table_name} exp
        INNER JOIN tbl_supplier as supplier on supplier.id = exp.supplier_id
        INNER JOIN tbl_accounts as account on account.id = exp.account_id
        WHERE 
            exp.received_date LIKE "{YEAR}-{MONTH}%"
            AND (exp.vat_exempt + exp.vat_zero_rated + exp.vat_12) != 0
        GROUP BY 
            supplier.supplier_name,
            supplier.supplier_tin,
            account.vat_class
        ORDER BY account.vat_class, supplier.supplier_name
        ;
    '''


with sqlite3.connect(os.path.join('instance', 'data.db')) as db:
    purchases = pd.read_sql_query(sql('tbl_purchases'), db)
    petty_cash = pd.read_sql_query(sql('tbl_pettycash'), db)
    expenses = pd.read_sql_query(sql('tbl_expenses'), db)

# Prepare a list of the dataframes, needed for the concat method
all_df = [purchases, petty_cash, expenses]

out_df = pd.concat(all_df).reset_index(drop=True)

# Write concatenated dataframes to Excel
out_df.to_excel("Z-Reading.xlsx", MONTH, index=False)