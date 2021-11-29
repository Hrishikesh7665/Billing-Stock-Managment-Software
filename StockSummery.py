from tkinter import *
from tkinter import messagebox, ttk, font
import sqlite3
import os, sys
import webbrowser



def resource_path():
    CurrentPath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    spriteFolderPath = os.path.join(CurrentPath, 'Assets/')
    path = os.path.join(spriteFolderPath)
    newPath = path.replace(os.sep, '/')
    return newPath

app_Data = (os.getenv('APPDATA'))+"\BillingSoftwareByHrishikesh\\"

Database_Path_With_Name = app_Data+"Stock.db"

_path = resource_path()

background_ST_Win = "pink"

Total_VAl = 0


def inventory_Management():
    global Total_VAl
    Stock_Management_Window = Tk()
    Stock_Management_Window.state('zoomed')
    #Stock_Management_Window.overrideredirect(True)
    search_entry_Stock = StringVar(Stock_Management_Window)
    Stock_Management_Window.config(bg=background_ST_Win)
    Stock_Management_Window.title("Stock Summery")
    ButtonFrame = Frame(Stock_Management_Window,bg=background_ST_Win)
    menu_tabs_framel_Stock = Frame(Stock_Management_Window)
    ButtonFrame.pack(fill=BOTH)
    menu_tabs_framel_Stock.pack(fill=BOTH,expand=1)
    Company_Logo_Web_Frame = Frame(Stock_Management_Window,bg=background_ST_Win)
    Company_Logo_Web_Frame.pack(fill=BOTH)
    Stock_Management_Window.minsize(800,400)

    w, h = Stock_Management_Window.winfo_screenwidth()-10, Stock_Management_Window.winfo_screenheight()-36
    Stock_Management_Window.geometry("%dx%d+0+0" % (w, h))

    StockIcon = _path+"summery.png"
    Search_icon = PhotoImage(file=_path+"Se.png",master=Stock_Management_Window)
    del_icon = PhotoImage(file=_path+"del.png",master=Stock_Management_Window)


    def load_menu_Stock():
        global Total_VAl
        if os.path.exists(Database_Path_With_Name) == True:
            conn = sqlite3.connect(Database_Path_With_Name)
            c = conn.cursor()
            c.execute("SELECT * FROM Stock ORDER BY Product_Name ASC")
            menu_table_Stock.delete(*menu_table_Stock.get_children())
            items = c.fetchall()
            for items in items:
                name = (items[0])
                P_price = (items[3])
                stock = (items[5])
                stock_U = (items[6])
                s_total = float(stock)*float(P_price)
                Total_VAl = float(Total_VAl)+float(s_total)
                st = str(stock)+" "+str(stock_U)
                menu_table_Stock.insert('',END,values=[name,P_price,st,s_total,s_total])
            conn.close()
        menu_table_Stock.heading("name",image="")
        menu_table_Stock.heading("p_price",image="")
        menu_table_Stock.heading("stock",image="")
        menu_table_Stock.heading("s_total",image="")
        menu_table_Stock.selection_clear()
        menu_table_Stock.selection_remove(menu_table_Stock.focus())

    ############################# Menu Table ##########################################


    scrollbar_menu_x = Scrollbar(menu_tabs_framel_Stock,orient=HORIZONTAL)
    scrollbar_menu_y = Scrollbar(menu_tabs_framel_Stock,orient=VERTICAL)

    s = ttk.Style(Stock_Management_Window)
    s.configure("Treeview.Heading",font=("arial",13, "bold"))
    s.configure("Treeview",font=("arial",12),rowheight=25)

    menu_table_Stock = ttk.Treeview(menu_tabs_framel_Stock,style = "Treeview",
                columns =("name", "p_price", "stock", "s_total"),xscrollcommand=scrollbar_menu_x.set,
                yscrollcommand=scrollbar_menu_y.set)

    menu_table_Stock.heading("name",text="Product Name")
    menu_table_Stock.heading("p_price",text="Purchase Price (Rs)")
    menu_table_Stock.heading("stock",text="Stock")
    menu_table_Stock.heading("s_total",text="Stock Value (Rs)")



    menu_table_Stock["displaycolumns"]=("name", "stock", "p_price", "s_total")
    menu_table_Stock["show"] = "headings"


    menu_table_Stock.column("s_total",width=62,anchor='center')
    menu_table_Stock.column("p_price",width=62,anchor='center')
    menu_table_Stock.column("stock",width=30,anchor='center')
    menu_table_Stock.column("name",anchor='center')

    scrollbar_menu_x.pack(side=BOTTOM,fill=X)
    scrollbar_menu_y.pack(side=RIGHT,fill=Y)

    scrollbar_menu_x.configure(command=menu_table_Stock.xview)
    scrollbar_menu_y.configure(command=menu_table_Stock.yview)

    menu_table_Stock.pack(fill=BOTH,expand=1)



    #menu_table_Stock.bind("<ButtonRelease-1>",load_item_from_menu_Stock_Management)

    ###########################################################################################

    def SearchBar_Fun_Stock_Management(event):
        global Pname_Order, PurPrice_Order, Stock_Order, S_total_Order
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
                    stock = (items[5])
                    stock_U = (items[6])
                    s_total = float(stock)*float(P_price)
                    st = str(stock)+" "+str(stock_U)
                    menu_table_Stock.insert('',END,values=[name,P_price,st,s_total])
                conn.close()
                menu_table_Stock.heading("name",image="")
                Pname_Order = True
                PurPrice_Order = False
                Stock_Order = False
                menu_table_Stock.selection_clear()
                menu_table_Stock.selection_remove(menu_table_Stock.focus())
        elif search_entry_Stock.get()=="":
            load_menu_Stock()

    def on_search_Bar_Stock_click(e):
        menu_table_Stock.selection_clear()
        menu_table_Stock.selection_remove(menu_table_Stock.focus())


    def on_search_Bar_Stock_focusout(e):
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

    Button(ButtonFrame,image= del_icon,bd=0,activebackground="white",bg="white",font=("DubaiMedium",10),compound=LEFT,command=Clear_SearchBar_Fun_Stock_Management).place(x=348,y=13)




    Label(ButtonFrame,text="        \n",font=("BerlinSansFBDemi",13),bg=background_ST_Win).pack(side=RIGHT)
    lb = Label(ButtonFrame,text=str(Total_VAl),font=("BerlinSansFBDemi",14,"bold"),bg=background_ST_Win)
    lb.pack(side=RIGHT)
    Label(ButtonFrame,text="Total Stock Value :- ",font=("BerlinSansFBDemi",13),bg=background_ST_Win).pack(side=RIGHT)


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



    def load_item_from_menu_Stock_Management(event):
        curItem = menu_table_Stock.focus()
        cursor_row = menu_table_Stock.focus()
        contents = menu_table_Stock.item(cursor_row)
        row = contents["values"]

    def close_window_Stock_Management_Close():
        a = messagebox.askquestion("Exit Conformation","Are You Sure You Want To Exit ?",default ="no",icon='warning')
        if a == "yes":
            Stock_Management_Window.destroy()
    Stock_Management_Window.protocol("WM_DELETE_WINDOW", close_window_Stock_Management_Close)

    load_menu_Stock()
    lb.config(text=str(Total_VAl)+" Rs.")
    menu_table_Stock.bind("<ButtonRelease-1>",load_item_from_menu_Stock_Management)

    Stock_Management_Window.tk.call('wm', 'iconphoto', Stock_Management_Window._w, PhotoImage(file=StockIcon,master=Stock_Management_Window))

    def Search_Focus_st(e):
        search_Bar_Stock.focus()
        search_Bar_Stock.icursor("end")

    Stock_Management_Window.bind("<Control-S>",Search_Focus_st)
    Stock_Management_Window.bind("<Control-s>",Search_Focus_st)
    Stock_Management_Window.mainloop()

def main_driver():
    inventory_Management()


#main_driver()