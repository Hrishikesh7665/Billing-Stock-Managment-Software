
def start_StockSummery():
    import StockSummery
    StockSummery.main_driver()
    start_stockmanagment ()

def start_stockmanagment ():
    import stockmanagment
    nxt = (stockmanagment.main_driver())
    if nxt == "Open_Stock_Summery":
        start_StockSummery()
    if nxt == "Main_WIN":
        show_Main()

def show_Main ():
    import Main_Screen
    next = Main_Screen.main_driver()
    if next == "Open Inventory":
        start_stockmanagment ()
    if next == "Open Summery":
        start_StockSummery ()
    if next == "":
        import sys
        sys.exit()


import loginscreen
login_status =  loginscreen.main_driver()
if login_status == True:
    show_Main ()
