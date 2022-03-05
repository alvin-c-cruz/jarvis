from dataclasses import dataclass
from sqlite_data_model import sqliteDataModel

@dataclass
class Accounts(sqliteDataModel):
    account_tag: str = ""
    account_number: str = ""
    account_title: str = ""
    vat_class: str = ""
    wt_class: str = ""


@dataclass
class Purchases(sqliteDataModel):
    received_date: str = ""
    rr_number: str = ""
    po: str = ""
    invoice: str = ""
    particulars: str = ""
    invalid: float = 0.0
    vat_zero_rated: float = 0.0
    vat_exempt: float = 0.0
    vat_12: float = 0.0
    ewt_rate: float = 0.0
    supplier_id: int = None
    account_id: int = None


@dataclass
class PettyCash(sqliteDataModel):
    received_date: str = ""
    rr_number: str = ""
    po: str = ""
    invoice: str = ""
    particulars: str = ""
    invalid: float = 0.0
    vat_zero_rated: float = 0.0
    vat_exempt: float = 0.0
    vat_12: float = 0.0
    ewt_rate: float = 0.0
    supplier_id: int = None
    account_id: int = None


@dataclass
class Supplier(sqliteDataModel):
    supplier_name: str = ""
    supplier_tin: str = ""
