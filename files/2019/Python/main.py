import os
import time

from FileManager import File

dict_command = {"addSV":"Add a new Sales Voucher",
                "addAP","add Accounts Payable",
                "addGJ","Add General Journal",
                "COA":"View Chart of Accounts",
                "addCOA":"Add a new Account Title",
                "Clear":"Clear screens leaving only command prompt",
                "Help":"Shows available commands",
                "Quit":"Terminate the program"}

_file_accounts = r'registers\accounts.txt'
dict_accounts = File(_file_accounts).Retrieve()

def main():
    program_loop = True
    _msg = "Welcome to TOSHCO Inc system"
    print(_msg)    

    while program_loop:    
        _command = input("Command : ")
        if _command in dict_command:
            print("")
            eval(_command)()
        else:
            print("'{0:<12}'.format(_command)")
            print("Invalid command. Type <Help> to view list of available commands")
            time.sleep(1)
                
def Clear():
    os.system('cls')

def Help():
    print("Command Lists")
    for _command in dict_command:
        print(f"    {'{0:<12}'.format(_command)} - {dict_command[_command]}")
    print("")
    
def Quit():
    quit()

def COA():
    print("Chart of Accounts")
    for _acctnum in dict_accounts:
        print(f"{'{0:<6}'.format(_acctnum)} - {dict_accounts[_acctnum]}")
    print("")

def addCOA():
    program_loop = True
    while program_loop:
        print("<Add Account Title>")
        _acctnum = input (f"{'{0:<8}'.format('Number')} : ")
        _accttitle = input (f"{'{0:<8}'.format('Title')} : ")

        edit_loop = True
        while edit_loop:
            _msg = f"""
    1. Account Number : {_acctnum}
    2. Account Title  : {_accttitle}
    """
            print(_msg)
            print("Type 'Yes' to confirm, type [number] to edit entry, type 'Cancel' to exit")
            _response = input("COA Command : ")
            if _response == 'Yes':
                if _acctnum in dict_accounts:
                    print("Account Number already in use.")
                elif _accttitle in dict_accounts.values():
                    print("Account Title already in use")
                else:
                    dict_accounts[_acctnum] = _accttitle
                    File(_file_accounts).Save(dict_accounts)
                    print("Account added")
                    edit_loop = False
                    _response = input("Type <Y> to add another account.")
                    if _response in ("Y","y"):
                        program_loop = True
                    else:
                        program_loop = False

            elif _response in ('1','2'):
                if _response == '1':
                    _acctnum = input (f"{'{0:<8}'.format('Number')} : ")
                else:
                    _accttitle = input (f"{'{0:<8}'.format('Title')} : ")

            elif _response == 'Cancel':
                print("No new account added.")
                edit_loop = False
                program_loop = False

            else:
                print("Invalid command.")

            print("")

def addSV():
    program_loop = True
    while program_loop:
        print("<Add Sales Voucher>")
        _cashinbank = input (f"{'{0:<20}'.format('Cash deposited')} : ")
        _cashshort = input (f"{'{0:<20}'.format('Cash Shortage')} : ")
        _cashoverage = input (f"{'{0:<20}'.format('Cash Overage')} : ")
        _GC = input (f"{'{0:<20}'.format('Gift Check')} : ")
        _check = _ = input (f"{'{0:<20}'.format('Check')} : ")
        _Cc_commission = input (f"{'{0:<20}'.format('CC Commission')} : ")
        _Cc_wtax = input (f"{'{0:<20}'.format(r'CC W/tax')} : ")
        _Cc_receivable = input (f"{'{0:<20}'.format('CC Receivable')} : ")
        _regulardiscount = input (f"{'{0:<20}'.format('Regular Discount')} : ")
        _stockholderdiscount = input (f"{'{0:<20}'.format('Stockholder Discount')} : ")
        _employeediscount = input (f"{'{0:<20}'.format('Employee Discount')} : ")
        _seniordiscount = input (f"{'{0:<20}'.format('Senior Discount')} : ")
        _otherARparticulard = input (f"{'{0:<20}'.format('Other AR Particulars')} : ")
        _otherARAmount = input (f"{'{0:<20}'.format('Other AR Amount')} : ")
        _SCemployee = input (f"{'{0:<20}'.format('Employee SC')} : ")
        _provisionlosses = input (f"{'{0:<20}'.format('Provision for Losses')} : ")
        _localtax = input (f"{'{0:<20}'.format('Local Tax')} : ")
        _nonvatSales = input (f"{'{0:<20}'.format('Non VAT Sales')} : ")
        
        

        edit_loop = True
        while edit_loop:
            _msg = f"""
    1. Account Number : {_acctnum}
    2. Account Title  : {_accttitle}
    """
            print(_msg)
            print("Type 'Yes' to confirm, type [number] to edit entry, type 'Cancel' to exit")
            _response = input("COA Command : ")
            if _response == 'Yes':
                if _acctnum in dict_accounts:
                    print("Account Number already in use.")
                elif _accttitle in dict_accounts.values():
                    print("Account Title already in use")
                else:
                    dict_accounts[_acctnum] = _accttitle
                    File(_file_accounts).Save(dict_accounts)
                    print("Account added")
                    edit_loop = False
                    _response = input("Type <Y> to add another account.")
                    if _response in ("Y","y"):
                        program_loop = True
                    else:
                        program_loop = False

            elif _response in ('1','2'):
                if _response == '1':
                    _acctnum = input (f"{'{0:<8}'.format('Number')} : ")
                else:
                    _accttitle = input (f"{'{0:<8}'.format('Title')} : ")

            elif _response == 'Cancel':
                print("No new account added.")
                edit_loop = False
                program_loop = False

            else:
                print("Invalid command.")

            print("")

        
#==========================================
main()
