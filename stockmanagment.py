from tkinter import *
from tkinter import messagebox, ttk, font
import sqlite3
import os, sys
import webbrowser
from datetime import date

what_next = "Main_WIN"


def resource_path():
    CurrentPath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    # Look for the 'sprites' folder on the path I just gave you:
    spriteFolderPath = os.path.join(CurrentPath, 'Assets/')
    path = os.path.join(spriteFolderPath)
    newPath = path.replace(os.sep, '/')
    return newPath


app_Data = (os.getenv('APPDATA'))+"\BillingSoftwareByHrishikesh\\"

Database_Path_With_Name = app_Data+"Stock.db"

_path = resource_path()

background_ST_Win = "pink"




def inventory_Management():
    global what_next
    Stock_Management_Window = Tk()
    Stock_Management_Window.state('zoomed')
    #Stock_Management_Window.overrideredirect(True)
    search_entry_Stock = StringVar(Stock_Management_Window)
    Stock_Management_Window.config(bg=background_ST_Win)
    Stock_Management_Window.title("Stock Management")
    ButtonFrame = Frame(Stock_Management_Window,bg=background_ST_Win)
    menu_tabs_framel_Stock = Frame(Stock_Management_Window)
    ButtonFrame.pack(fill=BOTH)
    menu_tabs_framel_Stock.pack(fill=BOTH,expand=1)
    Company_Logo_Web_Frame = Frame(Stock_Management_Window,bg=background_ST_Win)
    Company_Logo_Web_Frame.pack(fill=BOTH)
    Stock_Management_Window.minsize(800,400)

    Pname_Order = True
    Pcat_Order = False
    PurPrice_Order = False
    SellPrice_Order = False
    Gst_Order = False
    Stock_Order = False


    w, h = Stock_Management_Window.winfo_screenwidth()-10, Stock_Management_Window.winfo_screenheight()-36
    Stock_Management_Window.geometry("%dx%d+0+0" % (w, h))


    Up = PhotoImage(file=_path+"UpArrow.png",master=Stock_Management_Window)
    Down = PhotoImage(file=_path+"DownArrow.png",master=Stock_Management_Window)
    StockIcon = _path+"Stock.png"
    AddIcon = _path+"AddIcon.png"
    SumIcon = _path+"summery.png"
    LowIcon = _path+"lowST.png"
    Edit_Icon = _path+"EditIcon.png"
    Delete_Icon = _path+"DeleteIcon.png"
    AddIcon_Ico = _path+"AddIcon.ico"
    LowIcon_Ico = _path+"lowST.ico"
    Edit_Icon_Ico = _path+"EditIcon.ico"
    Search_icon = PhotoImage(file=_path+"Se.png",master=Stock_Management_Window)
    del_icon = PhotoImage(file=_path+"del.png",master=Stock_Management_Window)


    def load_menu_Stock():
        global Pname_Order, Pcat_Order, PurPrice_Order, SellPrice_Order, Gst_Order, Stock_Order
        if os.path.exists(Database_Path_With_Name) == True:
            conn = sqlite3.connect(Database_Path_With_Name)
            c = conn.cursor()
            c.execute("SELECT * FROM Stock ORDER BY Product_Name ASC")
            #c.execute("SELECT * FROM Stock")
            #menuCategory.set("")
            menu_table_Stock.delete(*menu_table_Stock.get_children())
            items = c.fetchall()
            for items in items:
                name = (items[0])
                P_price = (items[3])
                S_price = (items[2])
                category = (items[1])
                gst = (items[4])
                stock = (items[5])
                stock_U = (items[6])
                st = str(stock)+" "+str(stock_U)
                menu_table_Stock.insert('',END,values=[name,category,P_price,S_price,gst,st])
            conn.close()
        Pname_Order = True
        Pcat_Order = False
        PurPrice_Order = False
        SellPrice_Order = False
        Gst_Order = False
        Stock_Order = False
        menu_table_Stock.heading("name",image="")
        menu_table_Stock.heading("category",image="")
        menu_table_Stock.heading("p_price",image="")
        menu_table_Stock.heading("s_price",image="")
        menu_table_Stock.heading("gst",image="")
        menu_table_Stock.heading("stock",image="")
        Edit_btn.config(state=DISABLED)
        delete_btn.config(state=DISABLED)
        menu_table_Stock.selection_clear()
        menu_table_Stock.selection_remove(menu_table_Stock.focus())

    #c.execute("SELECT * FROM Stock ORDER BY Product_Name DESC")


    def Product_Name_Fun ():
        global Pname_Order, Pcat_Order, PurPrice_Order, SellPrice_Order, Gst_Order, Stock_Order
        if Pname_Order == False:
            if os.path.exists(Database_Path_With_Name) == True:
                conn = sqlite3.connect(Database_Path_With_Name)
                c = conn.cursor()
                search = str(search_entry_Stock.get())+"%"
                c.execute("SELECT * FROM Stock WHERE P_Code LIKE :Searchfor ORDER BY Product_Name ASC",{'Searchfor': search})
                menu_table_Stock.delete(*menu_table_Stock.get_children())
                items = c.fetchall()
                for items in items:
                    name = (items[0])
                    P_price = (items[3])
                    S_price = (items[2])
                    category = (items[1])
                    gst = (items[4])
                    stock = (items[5])
                    stock_U = (items[6])
                    st = str(stock)+" "+str(stock_U)
                    menu_table_Stock.insert('',END,values=[name,category,P_price,S_price,gst,st])
                conn.close()
            menu_table_Stock.heading("name",image=Up)
            Pname_Order = True
            Pcat_Order = False
            PurPrice_Order = False
            SellPrice_Order = False
            Gst_Order = False
            Stock_Order = False
        elif Pname_Order == True:
            if os.path.exists(Database_Path_With_Name) == True:
                conn = sqlite3.connect(Database_Path_With_Name)
                c = conn.cursor()
                search = str(search_entry_Stock.get())+"%"
                c.execute("SELECT * FROM Stock WHERE P_Code LIKE :Searchfor ORDER BY Product_Name DESC",{'Searchfor': search})
                #c.execute("SELECT * FROM Stock ORDER BY Product_Name DESC")
                #c.execute("SELECT * FROM Stock")
                #menuCategory.set("")
                menu_table_Stock.delete(*menu_table_Stock.get_children())
                items = c.fetchall()
                for items in items:
                    name = (items[0])
                    P_price = (items[3])
                    S_price = (items[2])
                    category = (items[1])
                    gst = (items[4])
                    stock = (items[5])
                    stock_U = (items[6])
                    st = str(stock)+" "+str(stock_U)
                    menu_table_Stock.insert('',END,values=[name,category,P_price,S_price,gst,st])
                conn.close()
            menu_table_Stock.heading("name",image=Down)
            Pcat_Order = False
            Pname_Order = False
            PurPrice_Order = False
            SellPrice_Order = False
            Gst_Order = False
            Stock_Order = False
        menu_table_Stock.heading("category",image="")
        menu_table_Stock.heading("p_price",image="")
        menu_table_Stock.heading("s_price",image="")
        menu_table_Stock.heading("gst",image="")
        menu_table_Stock.heading("stock",image="")
        Edit_btn.config(state=DISABLED)
        delete_btn.config(state=DISABLED)
        menu_table_Stock.selection_clear()
        menu_table_Stock.selection_remove(menu_table_Stock.focus())





    def Product_Cat_Fun ():
        global Pname_Order, Pcat_Order, PurPrice_Order, SellPrice_Order, Gst_Order, Stock_Order
        if Pcat_Order == False:
            if os.path.exists(Database_Path_With_Name) == True:
                conn = sqlite3.connect(Database_Path_With_Name)
                c = conn.cursor()
                search = str(search_entry_Stock.get())+"%"
                c.execute("SELECT * FROM Stock WHERE P_Code LIKE :Searchfor ORDER BY Product_Category ASC",{'Searchfor': search})
                #c.execute("SELECT * FROM Stock ORDER BY Product_Category ASC")
                #c.execute("SELECT * FROM Stock")
                #menuCategory.set("")
                menu_table_Stock.delete(*menu_table_Stock.get_children())
                items = c.fetchall()
                for items in items:
                    name = (items[0])
                    P_price = (items[3])
                    S_price = (items[2])
                    category = (items[1])
                    gst = (items[4])
                    stock = (items[5])
                    stock_U = (items[6])
                    st = str(stock)+" "+str(stock_U)
                    menu_table_Stock.insert('',END,values=[name,category,P_price,S_price,gst,st])
                conn.close()
            menu_table_Stock.heading("category",image=Up)
            Pcat_Order = True
            Pname_Order = False
            PurPrice_Order = False
            SellPrice_Order = False
            Gst_Order = False
            Stock_Order = False
        elif Pcat_Order == True:
            if os.path.exists(Database_Path_With_Name) == True:
                conn = sqlite3.connect(Database_Path_With_Name)
                c = conn.cursor()
                search = str(search_entry_Stock.get())+"%"
                c.execute("SELECT * FROM Stock WHERE P_Code LIKE :Searchfor ORDER BY Product_Category DESC",{'Searchfor': search})
                #c.execute("SELECT * FROM Stock ORDER BY Product_Category DESC")
                #c.execute("SELECT * FROM Stock")
                #menuCategory.set("")
                menu_table_Stock.delete(*menu_table_Stock.get_children())
                items = c.fetchall()
                for items in items:
                    name = (items[0])
                    P_price = (items[3])
                    S_price = (items[2])
                    category = (items[1])
                    gst = (items[4])
                    stock = (items[5])
                    stock_U = (items[6])
                    st = str(stock)+" "+str(stock_U)
                    menu_table_Stock.insert('',END,values=[name,category,P_price,S_price,gst,st])
                conn.close()
            menu_table_Stock.heading("category",image=Down)
            Pcat_Order = False
            Pname_Order = False
            PurPrice_Order = False
            SellPrice_Order = False
            Gst_Order = False
            Stock_Order = False
        menu_table_Stock.heading("name",image="")
        menu_table_Stock.heading("p_price",image="")
        menu_table_Stock.heading("s_price",image="")
        menu_table_Stock.heading("gst",image="")
        menu_table_Stock.heading("stock",image="")
        Edit_btn.config(state=DISABLED)
        delete_btn.config(state=DISABLED)
        menu_table_Stock.selection_clear()
        menu_table_Stock.selection_remove(menu_table_Stock.focus())




    def Purchase_Price_Fun ():
        global Pname_Order, Pcat_Order, PurPrice_Order, SellPrice_Order, Gst_Order, Stock_Order
        if PurPrice_Order == False:
            if os.path.exists(Database_Path_With_Name) == True:
                conn = sqlite3.connect(Database_Path_With_Name)
                c = conn.cursor()
                search = str(search_entry_Stock.get())+"%"
                c.execute("SELECT * FROM Stock WHERE P_Code LIKE :Searchfor ORDER BY Purchase_Price ASC",{'Searchfor': search})
                #c.execute("SELECT * FROM Stock ORDER BY Purchase_Price ASC")
                #c.execute("SELECT * FROM Stock")
                #menuCategory.set("")
                menu_table_Stock.delete(*menu_table_Stock.get_children())
                items = c.fetchall()
                for items in items:
                    name = (items[0])
                    P_price = (items[3])
                    S_price = (items[2])
                    category = (items[1])
                    gst = (items[4])
                    stock = (items[5])
                    stock_U = (items[6])
                    st = str(stock)+" "+str(stock_U)
                    menu_table_Stock.insert('',END,values=[name,category,P_price,S_price,gst,st])
                conn.close()
            menu_table_Stock.heading("p_price",image=Up)
            PurPrice_Order = True
            Pname_Order = False
            Pcat_Order = False
            SellPrice_Order = False
            Gst_Order = False
            Stock_Order = False
        elif PurPrice_Order == True:
            if os.path.exists(Database_Path_With_Name) == True:
                conn = sqlite3.connect(Database_Path_With_Name)
                c = conn.cursor()
                search = str(search_entry_Stock.get())+"%"
                c.execute("SELECT * FROM Stock WHERE P_Code LIKE :Searchfor ORDER BY Purchase_Price DESC",{'Searchfor': search})
                #c.execute("SELECT * FROM Stock ORDER BY Purchase_Price DESC")
                #c.execute("SELECT * FROM Stock")
                #menuCategory.set("")
                menu_table_Stock.delete(*menu_table_Stock.get_children())
                items = c.fetchall()
                for items in items:
                    name = (items[0])
                    P_price = (items[3])
                    S_price = (items[2])
                    category = (items[1])
                    gst = (items[4])
                    stock = (items[5])
                    stock_U = (items[6])
                    st = str(stock)+" "+str(stock_U)
                    menu_table_Stock.insert('',END,values=[name,category,P_price,S_price,gst,st])
                conn.close()
            menu_table_Stock.heading("p_price",image=Down)
            Pcat_Order = False
            Pname_Order = False
            PurPrice_Order = False
            SellPrice_Order = False
            Gst_Order = False
            Stock_Order = False
        menu_table_Stock.heading("category",image="") #p_price
        menu_table_Stock.heading("name",image="")
        menu_table_Stock.heading("s_price",image="")
        menu_table_Stock.heading("gst",image="")
        menu_table_Stock.heading("stock",image="")
        Edit_btn.config(state=DISABLED)
        delete_btn.config(state=DISABLED)
        menu_table_Stock.selection_clear()
        menu_table_Stock.selection_remove(menu_table_Stock.focus())




    def Sell_Price_Fun ():
        global Pname_Order, Pcat_Order, PurPrice_Order, SellPrice_Order, Gst_Order, Stock_Order
        if SellPrice_Order == False:
            if os.path.exists(Database_Path_With_Name) == True:
                conn = sqlite3.connect(Database_Path_With_Name)
                c = conn.cursor()
                search = str(search_entry_Stock.get())+"%"
                c.execute("SELECT * FROM Stock WHERE P_Code LIKE :Searchfor ORDER BY Sale_Price ASC",{'Searchfor': search})
                #c.execute("SELECT * FROM Stock ORDER BY Sale_Price ASC")
                menu_table_Stock.delete(*menu_table_Stock.get_children())
                items = c.fetchall()
                for items in items:
                    name = (items[0])
                    P_price = (items[3])
                    S_price = (items[2])
                    category = (items[1])
                    gst = (items[4])
                    stock = (items[5])
                    stock_U = (items[6])
                    st = str(stock)+" "+str(stock_U)
                    menu_table_Stock.insert('',END,values=[name,category,P_price,S_price,gst,st])
                conn.close()
            menu_table_Stock.heading("s_price",image=Up)
            SellPrice_Order = True
            Pname_Order = False
            Pcat_Order = False
            PurPrice_Order = False
            Gst_Order = False
            Stock_Order = False
        elif SellPrice_Order == True:
            if os.path.exists(Database_Path_With_Name) == True:
                conn = sqlite3.connect(Database_Path_With_Name)
                c = conn.cursor()
                search = str(search_entry_Stock.get())+"%"
                c.execute("SELECT * FROM Stock WHERE P_Code LIKE :Searchfor ORDER BY Sale_Price DESC",{'Searchfor': search})
                #c.execute("SELECT * FROM Stock ORDER BY Sale_Price DESC")
                menu_table_Stock.delete(*menu_table_Stock.get_children())
                items = c.fetchall()
                for items in items:
                    name = (items[0])
                    P_price = (items[3])
                    S_price = (items[2])
                    category = (items[1])
                    gst = (items[4])
                    stock = (items[5])
                    stock_U = (items[6])
                    st = str(stock)+" "+str(stock_U)
                    menu_table_Stock.insert('',END,values=[name,category,P_price,S_price,gst,st])
                conn.close()
            menu_table_Stock.heading("s_price",image=Down)
            Pcat_Order = False
            Pname_Order = False
            PurPrice_Order = False
            SellPrice_Order = False
            Gst_Order = False
            Stock_Order = False
        menu_table_Stock.heading("category",image="") #p_price
        menu_table_Stock.heading("name",image="")
        menu_table_Stock.heading("p_price",image="")
        menu_table_Stock.heading("gst",image="")
        menu_table_Stock.heading("stock",image="")
        Edit_btn.config(state=DISABLED)
        delete_btn.config(state=DISABLED)
        menu_table_Stock.selection_clear()
        menu_table_Stock.selection_remove(menu_table_Stock.focus())




    def Gst_Per_Fun ():
        global Pname_Order, Pcat_Order, PurPrice_Order, SellPrice_Order, Gst_Order, Stock_Order
        if Gst_Order == False:
            if os.path.exists(Database_Path_With_Name) == True:
                conn = sqlite3.connect(Database_Path_With_Name)
                c = conn.cursor()
                search = str(search_entry_Stock.get())+"%"
                c.execute("SELECT * FROM Stock WHERE P_Code LIKE :Searchfor ORDER BY GST ASC",{'Searchfor': search})
                #c.execute("SELECT * FROM Stock ORDER BY GST ASC")
                menu_table_Stock.delete(*menu_table_Stock.get_children())
                items = c.fetchall()
                for items in items:
                    name = (items[0])
                    P_price = (items[3])
                    S_price = (items[2])
                    category = (items[1])
                    gst = (items[4])
                    stock = (items[5])
                    stock_U = (items[6])
                    st = str(stock)+" "+str(stock_U)
                    menu_table_Stock.insert('',END,values=[name,category,P_price,S_price,gst,st])
                conn.close()
            menu_table_Stock.heading("gst",image=Up)
            Gst_Order = True
            Pname_Order = False
            Pcat_Order = False
            PurPrice_Order = False
            SellPrice_Order = False
            Stock_Order = False
        elif Gst_Order == True:
            if os.path.exists(Database_Path_With_Name) == True:
                conn = sqlite3.connect(Database_Path_With_Name)
                c = conn.cursor()
                search = str(search_entry_Stock.get())+"%"
                c.execute("SELECT * FROM Stock WHERE P_Code LIKE :Searchfor ORDER BY GST DESC",{'Searchfor': search})
                #c.execute("SELECT * FROM Stock ORDER BY GST DESC")
                menu_table_Stock.delete(*menu_table_Stock.get_children())
                items = c.fetchall()
                for items in items:
                    name = (items[0])
                    P_price = (items[3])
                    S_price = (items[2])
                    category = (items[1])
                    gst = (items[4])
                    stock = (items[5])
                    stock_U = (items[6])
                    st = str(stock)+" "+str(stock_U)
                    menu_table_Stock.insert('',END,values=[name,category,P_price,S_price,gst,st])
                conn.close()
            menu_table_Stock.heading("gst",image=Down)
            Pcat_Order = False
            Pname_Order = False
            PurPrice_Order = False
            SellPrice_Order = False
            Gst_Order = False
            Stock_Order = False
        menu_table_Stock.heading("category",image="") #p_price
        menu_table_Stock.heading("name",image="")
        menu_table_Stock.heading("p_price",image="")
        menu_table_Stock.heading("s_price",image="")
        menu_table_Stock.heading("stock",image="")
        Edit_btn.config(state=DISABLED)
        delete_btn.config(state=DISABLED)
        menu_table_Stock.selection_clear()
        menu_table_Stock.selection_remove(menu_table_Stock.focus())



    def Stock_order_Fun ():
        global Pname_Order, Pcat_Order, PurPrice_Order, SellPrice_Order, Gst_Order, Stock_Order
        if Stock_Order == False:
            if os.path.exists(Database_Path_With_Name) == True:
                conn = sqlite3.connect(Database_Path_With_Name)
                c = conn.cursor()
                search = str(search_entry_Stock.get())+"%"
                c.execute("SELECT * FROM Stock WHERE P_Code LIKE :Searchfor ORDER BY Stock_Qty ASC",{'Searchfor': search})
                #c.execute("SELECT * FROM Stock ORDER BY Stock_Qty ASC")
                menu_table_Stock.delete(*menu_table_Stock.get_children())
                items = c.fetchall()
                for items in items:
                    name = (items[0])
                    P_price = (items[3])
                    S_price = (items[2])
                    category = (items[1])
                    gst = (items[4])
                    stock = (items[5])
                    stock_U = (items[6])
                    st = str(stock)+" "+str(stock_U)
                    menu_table_Stock.insert('',END,values=[name,category,P_price,S_price,gst,st])
                conn.close()
            menu_table_Stock.heading("stock",image=Up)
            Stock_Order = True
            Pname_Order = False
            Pcat_Order = False
            PurPrice_Order = False
            SellPrice_Order = False
            Gst_Order = False
        elif Stock_Order == True:
            if os.path.exists(Database_Path_With_Name) == True:
                conn = sqlite3.connect(Database_Path_With_Name)
                c = conn.cursor()
                search = str(search_entry_Stock.get())+"%"
                c.execute("SELECT * FROM Stock WHERE P_Code LIKE :Searchfor ORDER BY Stock_Qty DESC",{'Searchfor': search})
                #c.execute("SELECT * FROM Stock ORDER BY Stock_Qty DESC")
                menu_table_Stock.delete(*menu_table_Stock.get_children())
                items = c.fetchall()
                for items in items:
                    name = (items[0])
                    P_price = (items[3])
                    S_price = (items[2])
                    category = (items[1])
                    gst = (items[4])
                    stock = (items[5])
                    stock_U = (items[6])
                    st = str(stock)+" "+str(stock_U)
                    menu_table_Stock.insert('',END,values=[name,category,P_price,S_price,gst,st])
                conn.close()
            menu_table_Stock.heading("stock",image=Down) #stock
            Pcat_Order = False
            Pname_Order = False
            PurPrice_Order = False
            SellPrice_Order = False
            Gst_Order = False
            Stock_Order = False
        menu_table_Stock.heading("category",image="") #p_price
        menu_table_Stock.heading("name",image="")
        menu_table_Stock.heading("p_price",image="")
        menu_table_Stock.heading("s_price",image="")
        menu_table_Stock.heading("gst",image="")
        Edit_btn.config(state=DISABLED)
        delete_btn.config(state=DISABLED)
        menu_table_Stock.selection_clear()
        menu_table_Stock.selection_remove(menu_table_Stock.focus())


    ############################# Menu Table ##########################################


    scrollbar_menu_x = Scrollbar(menu_tabs_framel_Stock,orient=HORIZONTAL)
    scrollbar_menu_y = Scrollbar(menu_tabs_framel_Stock,orient=VERTICAL)

    s = ttk.Style(Stock_Management_Window)
    s.configure("Treeview.Heading",font=("arial",13, "bold"))
    s.configure("Treeview",font=("arial",12),rowheight=25)

    menu_table_Stock = ttk.Treeview(menu_tabs_framel_Stock,style = "Treeview",
                columns =("name", "category", "p_price", "s_price","gst","stock"),xscrollcommand=scrollbar_menu_x.set,
                yscrollcommand=scrollbar_menu_y.set)

    menu_table_Stock.heading("name",text="Product Name",command = Product_Name_Fun)
    menu_table_Stock.heading("category",text="Product Category",command = Product_Cat_Fun)
    menu_table_Stock.heading("p_price",text="Purchase Price (Rs)",command=Purchase_Price_Fun)
    menu_table_Stock.heading("s_price",text="Sell Price (Rs)",command=Sell_Price_Fun )
    menu_table_Stock.heading("gst",text="GST (%)",command = Gst_Per_Fun)
    menu_table_Stock.heading("stock",text="Stock",command = Stock_order_Fun)

    menu_table_Stock["displaycolumns"]=("name", "category","stock", "p_price", "s_price","gst")
    menu_table_Stock["show"] = "headings"

    menu_table_Stock.column("p_price",width=72,anchor='center')
    menu_table_Stock.column("gst",width=25,anchor='center')
    menu_table_Stock.column("s_price",width=72,anchor='center')
    menu_table_Stock.column("stock",width=30,anchor='center')
    menu_table_Stock.column("name",anchor='center')
    menu_table_Stock.column("category",anchor='center')

    scrollbar_menu_x.pack(side=BOTTOM,fill=X)
    scrollbar_menu_y.pack(side=RIGHT,fill=Y)

    scrollbar_menu_x.configure(command=menu_table_Stock.xview)
    scrollbar_menu_y.configure(command=menu_table_Stock.yview)

    menu_table_Stock.pack(fill=BOTH,expand=1)



    #menu_table_Stock.bind("<ButtonRelease-1>",load_item_from_menu_Stock_Management)

    ###########################################################################################

    def delete_fun():
        cursor_row = menu_table_Stock.focus()
        contents = menu_table_Stock.item(cursor_row)
        row = contents["values"]
        p = row[0]
        Stock_Management_Window.withdraw()
        a = messagebox.askquestion("Delete Conformation","Are You Sure You Want To Delete\n"+'"'+str(p)+'"'+"\nThis Product ?",default ="no",icon='warning')
        if a == "yes":
            conn = sqlite3.connect(Database_Path_With_Name)
            c = conn.cursor()
            c.execute("DELETE FROM Stock WHERE Product_Name = :Product_Name",{'Product_Name': p})
            conn.commit()
            conn.close()
            Edit_btn.config(state=DISABLED)
            delete_btn.config(state=DISABLED)
            menu_table_Stock.selection_clear()
            menu_table_Stock.selection_remove(menu_table_Stock.focus())
            load_menu_Stock()
        Edit_btn.config(state=DISABLED)
        delete_btn.config(state=DISABLED)
        menu_table_Stock.selection_clear()
        menu_table_Stock.selection_remove(menu_table_Stock.focus())
        Stock_Management_Window.deiconify()
        load_menu_Stock()

    def addProduct_Fun(e):
        addProductWin =Tk()
        addProductWin.config(bg=background_ST_Win)
        addProductWin.title("Add Product")
        w = 500
        h = 396
        ws = addProductWin.winfo_screenwidth()
        hs = addProductWin.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)  #change hs/2 to hs/4 to left window up
        addProductWin.geometry('%dx%d+%d+%d' % (w, h, x, y))
        addProductWin.resizable(False,False)
        Stock_Management_Window.withdraw()
        PnameVar = StringVar(addProductWin)
        PcataVar = StringVar(addProductWin)
        SalePVar = DoubleVar(addProductWin)
        PurPVar =  DoubleVar(addProductWin)
        GSTVar =   DoubleVar(addProductWin)
        StockVar = DoubleVar(addProductWin)
        StockUnitVar = StringVar(addProductWin)
        P_code_Var = StringVar(addProductWin)
        StockUnitVar.set("Not Selected")

        Label(addProductWin,text="  Product Name         :      ",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).grid(row=0,column=0)
        Label(addProductWin,text=" ",bg=background_ST_Win,justify=LEFT).grid()
        Label(addProductWin,text="  Product Code         :      ",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).grid(row=2,column=0)
        Label(addProductWin,text=" ",bg=background_ST_Win,justify=LEFT).grid()
        Label(addProductWin,text="  Product Category  :      ",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).grid(row=4,column=0)
        Label(addProductWin,text=" ",bg=background_ST_Win,justify=LEFT).grid()
        Label(addProductWin,text="  Sale Price                 :      ",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).grid(row=6,column=0)
        Label(addProductWin,text=" ",bg=background_ST_Win,justify=LEFT).grid()
        Label(addProductWin,text="  Purchase Price       :      ",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).grid(row=8,column=0)
        Label(addProductWin,text=" ",bg=background_ST_Win,justify=LEFT).grid()
        Label(addProductWin,text="  GST                            :      ",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).grid(row=10,column=0)
        Label(addProductWin,text=" ",justify=LEFT,bg=background_ST_Win).grid()
        Label(addProductWin,text="  Stock & Unit             :      ",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).grid(row=12,column=0)


        Entry(addProductWin,textvariable=PnameVar,font=("Arial",13),width=27,bd=3).grid(row=0,column=2)
        Entry(addProductWin,textvariable=P_code_Var,font=("Arial",13),width=27,bd=3).grid(row=2,column=2)
        Entry(addProductWin,textvariable=PcataVar,font=("Arial",13),width=27,bd=3).grid(row=4,column=2)
        Entry(addProductWin,textvariable=SalePVar,font=("Arial",13),width=27,bd=3).grid(row=6,column=2)
        Entry(addProductWin,textvariable=PurPVar,font=("Arial",13),width=27,bd=3).grid(row=8,column=2)
        Entry(addProductWin,textvariable=GSTVar,font=("Arial",13),width=27,bd=3).grid(row=10,column=2)
        Entry(addProductWin,textvariable=StockVar,font=("Arial",13),width=15,bd=3).grid(row=12,sticky=NW,column=2)
        OPM = ttk.OptionMenu(addProductWin, StockUnitVar, "Not Selected", "Packet", "Kg")
        OPM.config(width=10)
        OPM.grid(row=12,sticky=NE,column=2)


        Label(addProductWin,text=" ",justify=LEFT,bg=background_ST_Win).grid()

        def addBtn_Fun():
            if PnameVar.get()== "":
                LabelFWarning.config(text="Please Enter Product Name")
            elif P_code_Var.get()== "":
                LabelFWarning.config(text="Please Enter Product Code")
            elif PcataVar.get()== "":
                LabelFWarning.config(text="Please Enter Product Category")
            elif SalePVar.get()== 0.0:
                LabelFWarning.config(text="Please Enter Sale Price")
            elif PurPVar.get()== 0.0:
                LabelFWarning.config(text="Please Enter Purchase Price")
            elif GSTVar.get()== 0.0:
                LabelFWarning.config(text="Please Enter GST Percentage")
            elif StockVar.get()== 0.0:
                LabelFWarning.config(text="Please Enter Stock Value")
            elif StockUnitVar.get()== "Not Selected":
                LabelFWarning.config(text="Please Select Stock Unit")
            else:
                a = messagebox.askquestion("New Product Add Conformation","Are You Sure You Want To Add\n"+'"'+str(PnameVar.get().title())+'"'+"\nThis Product ?",default ="no",icon='warning')
                if a == "yes":
                    ProductName = PnameVar.get().title()
                    ProductCategory = PcataVar.get().title()
                    SalePrice = SalePVar.get()
                    PurchasePrice = PurPVar.get()
                    GST = GSTVar.get()
                    StockQty = StockVar.get()
                    StockUnit = StockUnitVar.get()
                    P_short_name = P_code_Var.get()
                    L_UP = date.today()
                    if os.path.exists(Database_Path_With_Name) != True:
                        database = sqlite3.connect(Database_Path_With_Name)
                        database.execute('''CREATE TABLE Stock
                            (Product_Name       TEXT    PRIMARY KEY,
                            Product_Category    TEXT,
                            Sale_Price          REAL,
                            Purchase_Price      REAL,
                            GST                 REAL,
                            Stock_Qty           REAL,
                            Stock_Unit          TEXT,
                            P_Code              TEXT,
                            L_UP                TEXT)''')
                        c = database.cursor()
                        try:
                            c.execute("INSERT INTO Stock (Product_Name, Product_Category, Sale_Price, Purchase_Price, GST, Stock_Qty, Stock_Unit, P_Code, L_UP) values(?,?,?,?,?,?,?,?,?)",(ProductName, ProductCategory, SalePrice, PurchasePrice, GST, StockQty, StockUnit, P_short_name, L_UP))
                            database.commit()
                            database.close()
                            addProductWin.destroy()
                            Stock_Management_Window.deiconify()
                            Edit_btn.config(state=DISABLED)
                            delete_btn.config(state=DISABLED)
                            menu_table_Stock.selection_clear()
                            menu_table_Stock.selection_remove(menu_table_Stock.focus())
                            load_menu_Stock()
                        except sqlite3.IntegrityError:
                            a = messagebox.askretrycancel("Product Exits",str(ProductName)+" or "+str(P_short_name)+" Is Already Available In Stock",icon='error' )
                            if a == False:
                                database.close()
                                addProductWin.destroy()
                                Stock_Management_Window.deiconify()
                                Edit_btn.config(state=DISABLED)
                                delete_btn.config(state=DISABLED)
                                menu_table_Stock.selection_clear()
                                menu_table_Stock.selection_remove(menu_table_Stock.focus())
                                load_menu_Stock()
                    else:
                        database = sqlite3.connect(Database_Path_With_Name)
                        c = database.cursor()
                        try:
                            c.execute("INSERT INTO Stock (Product_Name, Product_Category, Sale_Price, Purchase_Price, GST, Stock_Qty, Stock_Unit, P_Code, L_UP) values(?,?,?,?,?,?,?,?,?)",(ProductName, ProductCategory, SalePrice, PurchasePrice, GST, StockQty, StockUnit, P_short_name, L_UP))
                            database.commit()
                            database.close()
                            addProductWin.destroy()
                            Stock_Management_Window.deiconify()
                            Edit_btn.config(state=DISABLED)
                            delete_btn.config(state=DISABLED)
                            menu_table_Stock.selection_clear()
                            menu_table_Stock.selection_remove(menu_table_Stock.focus())
                            load_menu_Stock()
                        except sqlite3.IntegrityError:
                            a = messagebox.askretrycancel("Product Exits",str(ProductName)+" Is Already Available In Stock",icon='error' )
                            if a == False:
                                database.close()
                                addProductWin.destroy()
                                Stock_Management_Window.deiconify()
                                Edit_btn.config(state=DISABLED)
                                delete_btn.config(state=DISABLED)
                                menu_table_Stock.selection_clear()
                                menu_table_Stock.selection_remove(menu_table_Stock.focus())
                                load_menu_Stock()

        Button(addProductWin,command=addBtn_Fun,text="                          Add Item                          ").grid(row=14,columnspan=3)

        LabelFWarning = Label(addProductWin,text=" ",font=("Arial Bold",10),bg=background_ST_Win,fg="Indianred1")
        LabelFWarning.grid(row=16,columnspan=3)

        def close_window_addProductWin():
            a = messagebox.askquestion("Exit Conformation","Are You Sure You Want To Exit ?",default ="no",icon='warning')
            if a == "yes":
                Edit_btn.config(state=DISABLED)
                delete_btn.config(state=DISABLED)
                menu_table_Stock.selection_remove(menu_table_Stock.focus())
                addProductWin.destroy()
                Stock_Management_Window.deiconify()
                load_menu_Stock()

        addProductWin.wm_iconbitmap(AddIcon_Ico)
        addProductWin.protocol("WM_DELETE_WINDOW", close_window_addProductWin)
        addProductWin.mainloop()

    #AddIcon_Ico

    def Edit_btn_fun():
        EditWin = Tk()
        EditWin.config(bg=background_ST_Win)
        EditWin.title("Edit Product")
        w = 500
        h = 396
        ws = EditWin.winfo_screenwidth()
        hs = EditWin.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)  #change hs/2 to hs/4 to left window up
        EditWin.geometry('%dx%d+%d+%d' % (w, h, x, y))

        EditWin.resizable(False,False)

        PnameVar_EditWin = StringVar(EditWin)
        PcataVar_EditWin = StringVar(EditWin)
        SalePVar_EditWin = DoubleVar(EditWin)
        PurPVar_EditWin = DoubleVar(EditWin)
        GSTVar_EditWin = DoubleVar(EditWin)
        StockVar_EditWin = DoubleVar(EditWin)
        StockUnitVar_EditWin = StringVar(EditWin)
        P_code_Var_EditWin = StringVar(EditWin)
        #StockUnitVar_EditWin.set("Not Selected")



        Stock_Management_Window.withdraw()
        cursor_row = menu_table_Stock.focus()
        contents = menu_table_Stock.item(cursor_row)
        row = contents["values"]
        p = row[0]
        conn = sqlite3.connect(Database_Path_With_Name)
        c = conn.cursor()
        #c.execute("DELETE FROM Stock WHERE Product_Name = :Product_Name",{'Product_Name': p})
        c.execute('SELECT * FROM Stock WHERE Product_Name = :Product_Name',{'Product_Name': p})
        item = c.fetchall()
        PnameVar_EditWin_Old = item[0][0]
        PcataVar_EditWin_Old = item[0][1]
        SalePVar_EditWin_Old = item[0][2]
        PurPVar_EditWin_Old =  item[0][3]
        GSTVar_EditWin_Old = item[0][4]
        StockVar_EditWin_Old = item[0][5]
        StockUnitVar_EditWin_Old = item[0][6]
        P_code_Var_EditWin_Old = item[0][7]


        PnameVar_EditWin.set(PnameVar_EditWin_Old)
        PcataVar_EditWin.set(PcataVar_EditWin_Old)
        SalePVar_EditWin.set(SalePVar_EditWin_Old)
        PurPVar_EditWin.set(PurPVar_EditWin_Old)
        GSTVar_EditWin.set(GSTVar_EditWin_Old)
        StockVar_EditWin.set(StockVar_EditWin_Old)
        P_code_Var_EditWin.set(P_code_Var_EditWin_Old)


        Label(EditWin,text="  Product Name         :      ",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).grid(row=0,column=0)
        Label(EditWin,text=" ",justify=LEFT,bg=background_ST_Win).grid()
        Label(EditWin,text="  Product Code         :      ",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).grid(row=2,column=0)
        Label(EditWin,text=" ",justify=LEFT,bg=background_ST_Win).grid()
        Label(EditWin,text="  Product Category  :      ",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).grid(row=4,column=0)
        Label(EditWin,text=" ",justify=LEFT,bg=background_ST_Win).grid()
        Label(EditWin,text="  Sale Price                 :      ",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).grid(row=6,column=0)
        Label(EditWin,text=" ",justify=LEFT,bg=background_ST_Win).grid()
        Label(EditWin,text="  Purchase Price       :      ",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).grid(row=8,column=0)
        Label(EditWin,text=" ",justify=LEFT,bg=background_ST_Win).grid()
        Label(EditWin,text="  GST                            :      ",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).grid(row=10,column=0)
        Label(EditWin,text=" ",justify=LEFT,bg=background_ST_Win).grid()
        Label(EditWin,text="  Stock & Unit             :      ",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).grid(row=12,column=0)

        Entry(EditWin,textvariable=PnameVar_EditWin,font=("Arial",13),width=27,bd=3).grid(row=0,column=2)
        Entry(EditWin,textvariable=P_code_Var_EditWin,font=("Arial",13),width=27,bd=3).grid(row=2,column=2)
        Entry(EditWin,textvariable=PcataVar_EditWin,font=("Arial",13),width=27,bd=3).grid(row=4,column=2)
        Entry(EditWin,textvariable=SalePVar_EditWin,font=("Arial",13),width=27,bd=3).grid(row=6,column=2)
        Entry(EditWin,textvariable=PurPVar_EditWin,font=("Arial",13),width=27,bd=3).grid(row=8,column=2)
        Entry(EditWin,textvariable=GSTVar_EditWin,font=("Arial",13),width=27,bd=3).grid(row=10,column=2)
        Entry(EditWin,textvariable=StockVar_EditWin,font=("Arial",13),width=15,bd=3).grid(row=12,sticky=NW,column=2)
        OPM = ttk.OptionMenu(EditWin, StockUnitVar_EditWin, "Not Selected", "Packet", "Kg")
        OPM.config(width=10)
        OPM.grid(row=12,sticky=NE,column=2)
        StockUnitVar_EditWin.set(StockUnitVar_EditWin_Old)
        Label(EditWin,text=" ",justify=LEFT,bg=background_ST_Win).grid()

        def editBtn_Fun ():
            if PnameVar_EditWin.get() == PnameVar_EditWin_Old and P_code_Var_EditWin.get() == P_code_Var_EditWin_Old and PcataVar_EditWin.get() == PcataVar_EditWin_Old and SalePVar_EditWin.get() == SalePVar_EditWin_Old and PurPVar_EditWin.get() == PurPVar_EditWin_Old and GSTVar_EditWin.get() == GSTVar_EditWin_Old and StockVar_EditWin.get() == StockVar_EditWin_Old and StockUnitVar_EditWin.get() == StockUnitVar_EditWin_Old:
                messagebox.showerror("Update Error","No Changes Made")
            elif PnameVar_EditWin.get()== "":
                LabelFWarning.config(text="Please Enter Product Name")
            elif P_code_Var_EditWin.get()== "":
                LabelFWarning.config(text="Please Enter Product Code")
            elif PcataVar_EditWin.get()== "":
                LabelFWarning.config(text="Please Enter Product Category")
            elif SalePVar_EditWin.get()== 0.0:
                LabelFWarning.config(text="Please Enter Sale Price")
            elif PurPVar_EditWin.get()== 0.0:
                LabelFWarning.config(text="Please Enter Purchase Price")
            elif GSTVar_EditWin.get()== 0.0:
                LabelFWarning.config(text="Please Enter GST Percentage")
            elif StockVar_EditWin.get()== 0.0:
                LabelFWarning.config(text="Please Enter Stock Value")
            elif StockUnitVar_EditWin.get()== "Not Selected":
                LabelFWarning.config(text="Please Select Stock Unit")
            else:
                a = messagebox.askquestion("Update Conformation","Are You Sure You Want\nTo Update This ?",default ="no",icon='warning')
                if a =="yes":
                    conn = sqlite3.connect(Database_Path_With_Name)
                    c = conn.cursor()
                    c = c.execute("SELECT rowid, * FROM Stock WHERE Product_Name = :Product_Name",{'Product_Name': PnameVar_EditWin_Old})
                    t = c.fetchall()
                    rowID = t[0][0]
                    L_N = date.today()
                    try:
                        c.execute("""UPDATE Stock SET
                                    Product_Name     = :Product_Name,
                                    Product_Category = :Product_Category,
                                    Sale_Price       = :Sale_Price,
                                    Purchase_Price   = :Purchase_Price,
                                    GST              = :GST,
                                    Stock_Qty        = :Stock_Qty,
                                    Stock_Unit       = :Stock_Unit,
                                    P_Code           = :P_Code,
                                    L_UP             = :L_UP
                                    WHERE rowid = :rowid""",{'rowid'          : rowID,
                                                            'Product_Name'    : PnameVar_EditWin.get().title(),
                                                            'Product_Category': PcataVar_EditWin.get().title(),
                                                            'Sale_Price'      : SalePVar_EditWin.get(),
                                                            'GST'             : GSTVar_EditWin.get(),
                                                            'Stock_Qty'       : StockVar_EditWin.get(),
                                                            'Stock_Unit'      : StockUnitVar_EditWin.get(),
                                                            'P_Code'          : P_code_Var_EditWin.get(),
                                                            'Purchase_Price'  : PurPVar_EditWin.get(),
                                                            'L_UP'            : L_N})
                        conn.commit()
                        conn.close()
                        EditWin.destroy()
                        Stock_Management_Window.deiconify()
                        Edit_btn.config(state=DISABLED)
                        delete_btn.config(state=DISABLED)
                        menu_table_Stock.selection_clear()
                        menu_table_Stock.selection_remove(menu_table_Stock.focus())
                        load_menu_Stock()
                    except sqlite3.IntegrityError:
                        a = messagebox.askretrycancel("Product Exits",str(PnameVar_EditWin.get().title())+" Is Already Available In Stock",icon='error' )
                        if a == False:
                            conn.close()
                            EditWin.destroy()
                            Stock_Management_Window.deiconify()
                            Edit_btn.config(state=DISABLED)
                            delete_btn.config(state=DISABLED)
                            menu_table_Stock.selection_clear()
                            menu_table_Stock.selection_remove(menu_table_Stock.focus())
                            load_menu_Stock()

        Button(EditWin,command=editBtn_Fun,text="                          Edit Item                          ").grid(row=14,columnspan=3)
        LabelFWarning = Label(EditWin,text=" ",font=("Arial Bold",10),bg=background_ST_Win,fg="Indianred1")
        LabelFWarning.grid(row=16,columnspan=3)

        def close_window_EditWin():
            a = messagebox.askquestion("Exit Conformation","Are You Sure You Want To Exit ?",default ="no",icon='warning')
            if a == "yes":
                Edit_btn.config(state=DISABLED)
                delete_btn.config(state=DISABLED)
                #menu_table_Stock.selection_remove(menu_table_Stock.focus())
                menu_table_Stock.selection_clear()
                menu_table_Stock.selection_remove(menu_table_Stock.focus())
                EditWin.destroy()
                Stock_Management_Window.deiconify()
                load_menu_Stock()
        EditWin.wm_iconbitmap(Edit_Icon_Ico)
        EditWin.protocol("WM_DELETE_WINDOW", close_window_EditWin)
        EditWin.mainloop()

    def stock_Sum_btn_Fun(e):
        global what_next
        e = "Open_Stock_Summery"
        what_next = e
        Stock_Management_Window.destroy()

    def low_stock_btn_Fun(e):
        Low_stock_win = Tk()
        Low_stock_win.config(bg=background_ST_Win)
        Low_stock_win.title("Low Stock")
        w = 630
        h = 400
        ws = Low_stock_win.winfo_screenwidth()
        hs = Low_stock_win.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)  #change hs/2 to hs/4 to left window up
        Low_stock_win.geometry('%dx%d+%d+%d' % (w, h, x, y))
        Stock_Management_Window.withdraw()
        Low_stock_win.focus_force()

        top_frame = Frame(Low_stock_win,bg=background_ST_Win)
        top_frame.pack()


        Label(top_frame,text="Enter Low Stock Value (Default 10) :- ",font=("Arial Rounded MT Bold",12),bg=background_ST_Win).pack(side=LEFT)

        e1 = Entry(top_frame,textvariable=search_entry_Stock,font=("Lucida Fax",13),width=10,bd=1)
        e1.pack(side=LEFT)

        Label(top_frame,text=" \n\n ",font=("Arial Rounded MT Bold",6),bg=background_ST_Win).pack(side=LEFT)

        b1 = Button(top_frame,text=" Set ")
        b1.pack(side=LEFT)

        table_frame = Frame(Low_stock_win,bg=background_ST_Win)
        table_frame.pack(fill=BOTH,expand=1)

        scrollbar_x = Scrollbar(table_frame,orient=HORIZONTAL)
        scrollbar_y = Scrollbar(table_frame,orient=VERTICAL)



        def fixed_map(option):
            return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]

        style = ttk.Style(Low_stock_win)
        style.theme_use("clam")
        style.configure("Treeview.Heading",font=("arial",12, "bold"))
        style.configure("Treeview",font=("arial",12),rowheight=25)
        style.map('Treeview', foreground=fixed_map('foreground'),background=fixed_map('background'))

        tabel = ttk.Treeview(table_frame,style = "Treeview",
                    columns =("P_name","P_code","stock"),xscrollcommand=scrollbar_x.set,
                    yscrollcommand=scrollbar_y.set)


        tabel.heading("P_name",text="Product Name")
        tabel.heading("P_code",text="Product Code")
        tabel.heading("stock",text="Stock")
        tabel["displaycolumns"]=("P_name", "P_code", "stock")
        tabel["show"] = "headings"
        tabel.column("P_name",anchor='center')
        tabel.column("P_code",anchor='center')
        tabel.column("stock",anchor='center')

        scrollbar_x.pack(side=BOTTOM,fill=X)
        scrollbar_y.pack(side=RIGHT,fill=Y)

        scrollbar_x.configure(command=tabel.xview)
        scrollbar_y.configure(command=tabel.yview)

        tabel.pack(fill=BOTH,expand=1)


        def show_low(val):
            if os.path.exists(Database_Path_With_Name) == True:
                conn = sqlite3.connect(Database_Path_With_Name)
                c = conn.cursor()
                c.execute("SELECT * FROM Stock WHERE Stock_Qty <= :val ORDER BY Stock_Qty ASC",{'val': val})
                tabel.delete(*tabel.get_children())
                items = c.fetchall()
                for items in items:
                    name = (items[0])
                    code = (items[7])
                    stock = (items[5])
                    stock_U = (items[6])
                    st = str(stock)+" "+str(stock_U)
                    tabel.insert('',END,values=[name,code,st])
                conn.close()

        def close_window_Low_stock_win():
            a = messagebox.askquestion("Exit Conformation","Are You Sure You Want To Exit ?",default ="no",icon='warning')
            if a == "yes":
                Edit_btn.config(state=DISABLED)
                delete_btn.config(state=DISABLED)
                menu_table_Stock.selection_remove(menu_table_Stock.focus())
                Low_stock_win.destroy()
                Stock_Management_Window.deiconify()
                load_menu_Stock()

        def show_low2():
            val = e1.get()
            if val != "":
                try:
                    val = float(val)
                    e1.config(state=DISABLED)
                    b1.config(state=DISABLED)
                    show_low(val)
                except:
                    messagebox.showwarning("Error","Please Input A Numeric Value")
            else:
                messagebox.showwarning("Error","Please Input A Value")

        b1.config(command=show_low2)

        show_low(10)

        Low_stock_win.wm_iconbitmap(LowIcon_Ico)
        Low_stock_win.protocol("WM_DELETE_WINDOW", close_window_Low_stock_win)
        Low_stock_win.resizable(False,False)
        Low_stock_win.mainloop()

    #bisque2
    Label(ButtonFrame,text=" "*4,bg=background_ST_Win).pack(side=RIGHT)
    x = PhotoImage(file = Delete_Icon,master=Stock_Management_Window)
    delete_btn = Button(ButtonFrame,text="   Delete  ",bg="bisque2",font=("DubaiMedium",10),image= x,compound=LEFT,command=delete_fun)
    delete_btn.pack(side=RIGHT)
    delete_btn.config(state=DISABLED)
    Label(ButtonFrame,text=" "*3,bg=background_ST_Win).pack(side=RIGHT)
    Label(ButtonFrame,text="                \n\n",font=("Arial",8),bg=background_ST_Win).pack(side=LEFT)
    y = PhotoImage(file = Edit_Icon,master=Stock_Management_Window)
    Edit_btn = Button(ButtonFrame,text="   Edit  ",bg="bisque2",font=("DubaiMedium",10),image= y,compound=LEFT,command=Edit_btn_fun)
    Edit_btn.pack(side=RIGHT)
    Edit_btn.config(state=DISABLED)
    Label(ButtonFrame,text=" "*3,bg=background_ST_Win).pack(side=RIGHT)
    k = PhotoImage(file = AddIcon,master=Stock_Management_Window)
    Button(ButtonFrame,text="   Add  ",image= k,bg="bisque2",font=("DubaiMedium",10),compound=LEFT,command=lambda:addProduct_Fun(0)).pack(side=RIGHT)
    Label(ButtonFrame,text=" "*3,bg=background_ST_Win).pack(side=RIGHT)
    L = PhotoImage(file = SumIcon,master=Stock_Management_Window)
    Button(ButtonFrame,text=" Summery ",image= L,bg="bisque2",font=("DubaiMedium",10),compound=LEFT,command=lambda:stock_Sum_btn_Fun(0)).pack(side=RIGHT)
    Label(ButtonFrame,text=" "*3,bg=background_ST_Win).pack(side=RIGHT)
    Lt = PhotoImage(file = LowIcon,master=Stock_Management_Window)
    Button(ButtonFrame,text=" Low Stock ",image= Lt,bg="bisque2",font=("DubaiMedium",10),compound=LEFT,command=lambda:low_stock_btn_Fun(0)).pack(side=RIGHT)


    def SearchBar_Fun_Stock_Management(event):
        global Pname_Order, Pcat_Order, PurPrice_Order, SellPrice_Order, Gst_Order, Stock_Order
        if search_entry_Stock.get()!="":
            if os.path.exists(Database_Path_With_Name) == True:
                conn = sqlite3.connect(Database_Path_With_Name)
                c = conn.cursor()
                search = str(search_entry_Stock.get())+"%"
                #c.execute("SELECT * FROM Stock ORDER BY Product_Name ASC") :Product_Name",{'Product_Name': p})
                #Product_Name
                c.execute("SELECT * FROM Stock WHERE Product_Name LIKE :Searchfor ORDER BY Product_Name ASC",{'Searchfor': search})
                #menuCategory.set("")
                menu_table_Stock.delete(*menu_table_Stock.get_children())
                items = c.fetchall()
                for items in items:
                    name = (items[0])
                    P_price = (items[3])
                    S_price = (items[2])
                    category = (items[1])
                    gst = (items[4])
                    stock = (items[5])
                    stock_U = (items[6])
                    st = str(stock)+" "+str(stock_U)
                    menu_table_Stock.insert('',END,values=[name,category,P_price,S_price,gst,st])
                conn.close()
                menu_table_Stock.heading("name",image="")
                Pname_Order = True
                Pcat_Order = False
                PurPrice_Order = False
                SellPrice_Order = False
                Gst_Order = False
                Stock_Order = False
                Edit_btn.config(state=DISABLED)
                delete_btn.config(state=DISABLED)
                menu_table_Stock.selection_clear()
                menu_table_Stock.selection_remove(menu_table_Stock.focus())
        elif search_entry_Stock.get()=="":
            load_menu_Stock()

    def on_search_Bar_Stock_click(e):
        Edit_btn.config(state=DISABLED)
        delete_btn.config(state=DISABLED)
        menu_table_Stock.selection_clear()
        menu_table_Stock.selection_remove(menu_table_Stock.focus())


    def on_search_Bar_Stock_focusout(e):
        Edit_btn.config(state=DISABLED)
        delete_btn.config(state=DISABLED)
        menu_table_Stock.selection_clear()
        menu_table_Stock.selection_remove(menu_table_Stock.focus())

    def Clear_SearchBar_Fun_Stock_Management ():
        search_entry_Stock.set("")
        SearchBar_Fun_Stock_Management(0)

    search_Bar_Stock = Entry(ButtonFrame,textvariable=search_entry_Stock,font=("Lucida Fax",13),width=27,bd=1)
    Label(ButtonFrame,text="Search  ",font=("BerlinSansFBDemi",13),bg=background_ST_Win).pack(side=LEFT)
    search_Bar_Stock.pack(side=LEFT)
    Label(ButtonFrame,text=" ",bg=background_ST_Win).pack(side=LEFT)
    Button(ButtonFrame,image= Search_icon,bd=0,activebackground="bisque2",bg=background_ST_Win,font=("DubaiMedium",10),compound=LEFT,command=lambda:SearchBar_Fun_Stock_Management(0)).pack(side=LEFT)

    Button(ButtonFrame,image= del_icon,bd=0,activebackground="white",bg="white",font=("DubaiMedium",10),compound=LEFT,command=Clear_SearchBar_Fun_Stock_Management).place(x=403,y=14)
    #search_Bar_Stock.bind('<KeyPress>', SearchBar_Fun_Stock_Management)
    search_Bar_Stock.bind('<Return>', SearchBar_Fun_Stock_Management)
    search_Bar_Stock.bind('<KeyRelease>', SearchBar_Fun_Stock_Management)
    search_Bar_Stock.bind('<FocusIn>', on_search_Bar_Stock_click)
    search_Bar_Stock.bind('<FocusOut>', on_search_Bar_Stock_focusout)

    #uname_input.bind('<FocusIn>', on_uname_input_click)
    #uname_input.bind('<FocusOut>', on_uname_input_focusout)

    def onhover_Company_Logo_Web_Button(e):
        Company_Logo_Web_Button['fg'] = "red"
    def onleave_Company_Logo_Web_Button(e):
        Company_Logo_Web_Button['fg'] = "blue"


    Label(Company_Logo_Web_Frame,text=" "*3,bg=background_ST_Win).pack(side=RIGHT)
    #Label(Company_Logo_Web_Frame,text=" "*360,bg="black").pack(side=LEFT,fill=BOTH)
    Company_Logo_Web_Button = Button(Company_Logo_Web_Frame,bd=0,fg="blue",bg=background_ST_Win,activebackground=background_ST_Win,command= lambda: webbrowser.open_new_tab("https://github.com/Hrishikesh7665"),text="                         Developed By ©Hrishikesh Patra")
    Company_Logo_Web_Button.pack(side=RIGHT)
    Company_Logo_Web_Button.bind('<Enter>', onhover_Company_Logo_Web_Button)
    Company_Logo_Web_Button.bind('<Leave>', onleave_Company_Logo_Web_Button)



    def show_Details(event):
        global what_next
        curItem = menu_table_Stock.focus()
        cursor_row = menu_table_Stock.focus()
        contents = menu_table_Stock.item(cursor_row)
        row = contents["values"]
        if row != "":
            show_Product_Details_Win =Tk()
            show_Product_Details_Win.config(bg=background_ST_Win)
            show_Product_Details_Win.title("'"+str(row[0])+"' Product Details")
            w = 500
            h = 446
            ws = show_Product_Details_Win.winfo_screenwidth()
            hs = show_Product_Details_Win.winfo_screenheight()
            # calculate position x, y
            x = (ws/2) - (w/2)
            y = (hs/2) - (h/2)  #change hs/2 to hs/4 to left window up
            show_Product_Details_Win.geometry('%dx%d+%d+%d' % (w, h, x, y))
            show_Product_Details_Win.resizable(False,False)
            Stock_Management_Window.withdraw()
            show_Product_Details_Win.focus_force()

            conn = sqlite3.connect(Database_Path_With_Name)
            c = conn.cursor()
            c = c.execute("SELECT rowid, * FROM Stock WHERE Product_Name = :Product_Name",{'Product_Name': str(row[0])})
            t = c.fetchall()
            Label(show_Product_Details_Win,text=" ",font=("Arial Rounded MT Bold",2),bg=background_ST_Win).pack(side=TOP)

            Label(show_Product_Details_Win,text=("  "+str(row[0])+"  "),font=("Arial Rounded MT Bold",20,"underline"),bg=background_ST_Win).pack(side=TOP)
            Label(show_Product_Details_Win,text=" ",font=("Arial Rounded MT Bold",4),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text="  Product Code                     :          "+str(t[0][8]),font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text=" ",font=("Arial Rounded MT Bold",2),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text="  Product Category             :          "+str(t[0][2]),font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text=" ",font=("Arial Rounded MT Bold",2),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text="  Stock & Unit                        :          "+str(t[0][6])+" "+str(t[0][7]),font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text=" ",font=("Arial Rounded MT Bold",2),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text="  Sale Price                            :          "+str(t[0][3])+" Rs.",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text=" ",font=("Arial Rounded MT Bold",2),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text="  Stock Value                         :          "+(str(float(t[0][6])*float(t[0][3])))+" Rs.",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text=" ",font=("Arial Rounded MT Bold",2),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text="  Purchase Price                  :          "+str(t[0][4])+" Rs.",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text=" ",font=("Arial Rounded MT Bold",2),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text="  GST(%)                                 :          "+str(t[0][5]),font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text=" ",font=("Arial Rounded MT Bold",2),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text="  Sale Price Without GST   :          "+str(t[0][5]),font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text=" ",font=("Arial Rounded MT Bold",2),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            #Label(show_Product_Details_Win,text="  Marchendice                      :          "+str(t[0][9]),font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text="  Marchendice                      :          "+"Not Defined",font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text=" ",font=("Arial Rounded MT Bold",2),bg=background_ST_Win,justify=LEFT).pack(anchor=W)
            Label(show_Product_Details_Win,text="  Last Update                        :          "+str(t[0][9]),font=("Arial Rounded MT Bold",15),bg=background_ST_Win,justify=LEFT).pack(anchor=W)


            def close_window_EditWin():
                a = messagebox.askquestion("Exit Conformation","Are You Sure You Want To Exit ?",default ="no",icon='warning')
                if a == "yes":
                    Edit_btn.config(state=DISABLED)
                    delete_btn.config(state=DISABLED)
                    menu_table_Stock.selection_clear()
                    menu_table_Stock.selection_remove(menu_table_Stock.focus())
                    show_Product_Details_Win.destroy()
                    Stock_Management_Window.deiconify()
                    load_menu_Stock()
            show_Product_Details_Win.wm_iconbitmap(Edit_Icon_Ico)
            show_Product_Details_Win.protocol("WM_DELETE_WINDOW", close_window_EditWin)
            show_Product_Details_Win.mainloop()


    def load_item_from_menu_Stock_Management(event):
        #delete_btn.config(state="normal")
        #Edit_btn.config(state="normal")
        curItem = menu_table_Stock.focus()
        cursor_row = menu_table_Stock.focus()
        contents = menu_table_Stock.item(cursor_row)
        row = contents["values"]
        if row != "":
            delete_btn.config(state="normal")
            Edit_btn.config(state="normal")

    def close_window_Stock_Management_Close():
        global what_next
        a = messagebox.askquestion("Exit Conformation","Are You Sure You Want To Exit ?",default ="no",icon='warning')
        if a == "yes":
            what_next = 'Main_WIN'
            Stock_Management_Window.destroy()
    Stock_Management_Window.protocol("WM_DELETE_WINDOW", close_window_Stock_Management_Close)

    load_menu_Stock()
    menu_table_Stock.bind("<ButtonRelease-1>",load_item_from_menu_Stock_Management)

    Stock_Management_Window.tk.call('wm', 'iconphoto', Stock_Management_Window._w, PhotoImage(file=StockIcon,master=Stock_Management_Window))

    def Search_Focus_st(e):
        search_Bar_Stock.focus()
        search_Bar_Stock.icursor("end")

    def Del_Shortcut(e):
        if (delete_btn["state"]) == "normal":
            delete_fun()

    def Edit_Shortcut(e):
        if (Edit_btn["state"]) == "normal":
            Edit_btn_fun()

    Stock_Management_Window.bind("<Control-S>",Search_Focus_st)
    Stock_Management_Window.bind("<Control-s>",Search_Focus_st)
    Stock_Management_Window.bind("<Control-A>",addProduct_Fun)
    Stock_Management_Window.bind("<Control-a>",addProduct_Fun)
    Stock_Management_Window.bind("<Delete>",Del_Shortcut)
    Stock_Management_Window.bind("<Control-e>",Edit_Shortcut)
    Stock_Management_Window.bind("<Control-E>",Edit_Shortcut)
    menu_table_Stock.bind("<Double-Button-1>",show_Details)
    Stock_Management_Window.mainloop()

def main_driver():
    inventory_Management()
    return  what_next


#print(main_driver())