
from tkinter import *
from tkinter import messagebox, ttk, font
import os, sys, re, subprocess
from datetime import datetime
import webbrowser
import time
import pdfgen
from reportlab.pdfgen import canvas
import sqlite3

menu_category = []
#["Tea & Coffee","Beverages","Fast Food","South Indian","Starters","Main Course","Dessert"]

what_NXT = ""

order_dict = {}

old_Discount = 0.0
#os.chdir(os.path.dirname(os.path.abspath(__file__)))

today = datetime.now()
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')+"\Bill Records"
F_Name = (today.strftime('%d.%m.%Y'))
PATH_Bill = desktop+"\\"+F_Name

if not os.path.exists(desktop):
    os.makedirs(desktop)

if not os.path.exists(PATH_Bill):
    os.makedirs(PATH_Bill)

#folder = f"{t.tm_mday},{t.tm_mon},{t.tm_year}"
#        if not os.path.exists(f"Bill Records\\{folder}"):
#            os.makedirs(f"Bill Records\\{folder}")
#Path



def resource_path():
    CurrentPath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    # Look for the 'sprites' folder on the path I just gave you:
    spriteFolderPath = os.path.join(CurrentPath, 'Assets/')
    path = os.path.join(spriteFolderPath)
    newPath = path.replace(os.sep, '/')
    return newPath

_path = resource_path()

app_Data = (os.getenv('APPDATA'))+"\BillingSoftwareByHrishikesh\\"
Database_Path_With_Name = app_Data+"Stock.db"


#====================Backend Functions===========================

class header:
    def __init__(self,CustomerName,CustomerContact):
        self.InvoiceNumber=time.time()
        self.CustomerName=CustomerName
        self.CustomerContact=CustomerContact
        timedate=time.asctime()
        self.date=timedate[4:8]+timedate[8:10]+", "+timedate[20:24]+"."
        self.time=" "+timedate[11:20]
class product:
    def __init__(self,name,quantity,rate,tax,discount):
        self.name=name
        self.quantity=quantity
        self.rate=rate
        self.tax=tax
        self.total=(quantity*rate)-discount
        self.discount=discount

def main_fun():
    Products=[]

    def printinvoice():
        head=header(customerName.get(),customerContact.get())
        pdf= canvas.Canvas(PATH_Bill+"\\"+str(int(head.InvoiceNumber))+".pdf")
        pdfgen.header(head,pdf)
        pdfgen.middle(pdf)
        ycooridinate=650
        x=1

        for item in Products:
            currproduct=product(item[0],item[1],item[2],item[5],item[3])
            pdf.drawString(35,ycooridinate,str(x))
            x=x+1
            pdf.setFont("Courier-Bold",9)
            ycooridinate=pdfgen.additem(currproduct,pdf,ycooridinate)
        pdf.setFont("Courier-Bold",11)
        try:
            dis = float(itemdis.get())
        except ValueError:
            dis = 0.0
        if Due_Amount_Var.get() == "-NIL-":
            pdfgen.footer(pdf,Products,roundoff_Check.get(),dis)
        else:
            Due = float(Due_Amount_Var.get())
            pdfgen.footer_for_Due(pdf,Products,roundoff_Check.get(),dis,Due)
        pdf.save()
        webbrowser.open(PATH_Bill+"\\"+str(int(head.InvoiceNumber))+".pdf")




    def SubmitData():
        product=PRODUCTNAME.get()
        quantity=QUANTITY.get()
        rate=RATE.get()
        try:
            dis=0.0#float(itemdis.get())
        except ValueError:
            dis=0.0
        #tax=TAX.get()
        #float((quantity*rate)*(DISCOUNT.get()/100))
        total=float(QUANTITY.get()*RATE.get())
        #float(QUANTITY.get()*RATE.get()-dis)

        #tax = float(TAX.get()*0.01*total)
        tax = float(TAX.get())
        grand_total = total#-dis
        Products.append((product,quantity,rate,dis,grand_total,tax))
        PRODUCTNAME.set("")
        QUANTITY.set(1)
        RATE.set(0)
        printinvoice()


    def load_menu():
        global menu_category, order_dict
        menuCategory.set("")
        menu_category = []
        order_dict = {}
        if os.path.exists(Database_Path_With_Name) == True:
            conn = sqlite3.connect(Database_Path_With_Name)
            c = conn.cursor()
            c.execute("SELECT * FROM Stock ORDER BY Product_Name ASC")
            menu_tabel.delete(*menu_tabel.get_children())
            items = c.fetchall()
            menu_category.append("All Items")
            for items in items:
                name = (items[0])
                price = (items[2]) #Sell Price
                category = (items[1])
                gst = (items[4])
                stockQt = (items[5])
                stockUnit = (items[6])
                stock = str(stockQt)+" "+str(stockUnit)
                if category not in menu_category:
                    menu_category.append(category)
                    menu_category.sort()
                menu_tabel.insert('',END,values=[name,price,category,gst,stock])
                menuCategory.set("All Items")
                try:
                    combo_menu.config(values=menu_category)
                except:
                    pass
            conn.close()
            for i in menu_category:
                order_dict[i] = {}

    '''for i in menu_category:
        order_dict[i] = {}'''

    def load_order():
        order_tabel.delete(*order_tabel.get_children())
        for category in order_dict.keys():
            if order_dict[category]:
                for lis in order_dict[category].values():
                    order_tabel.insert('',END,values=lis)
        update_total_price()

    def add_button_operation():
        name = itemName.get()
        rate = itemRate.get()
        category = itemCategory.get()
        quantity = itemQuantity.get()
        gst = itemgst.get()
        stock=itemStock_Var.get()
        stock = (re.findall('\d+', stock ))
        stock = float(str(float(stock[0]))+str((stock[1])))
        if float(quantity) > stock:
            messagebox.showinfo("Error! Low Stock", "Item Quantity More Than Present Stock")
            return
        if name in order_dict[category].keys():
            messagebox.showinfo("Error", "Item already exist in your order")
            return
        if not quantity.isdigit():
            messagebox.showinfo("Error", "Please Enter Valid Quantity")
            return
        price = float(rate)*int(quantity)
        gstcal = (price*float(gst))/100
        total = str(gstcal+price)
        lis = [name,rate,quantity,total,category,float(gst),stock]
        order_dict[category][name] = lis
        load_order()



    def load_item_from_menu(event):
        cursor_row = menu_tabel.focus()
        contents = menu_tabel.item(cursor_row)
        row = contents["values"]
        if row!="":
            #item_quantity.focus()
            itemName.set(row[0])
            itemRate.set(row[1])
            itemCategory.set(row[2])
            itemQuantity.set("1")
            itemgst.set(row[3])
            itemStock_Var.set(row[4])
            stock = itemStock_Var.get()
            stock = (re.findall('\d+', stock ))
            stock = float(str(float(stock[0]))+str((stock[1])))
            if lowStock_amount>=stock:
                gif_label.place(x=1315,y=138)
            else:
                gif_label.place(x=10000,y=10000)


    def load_item_from_order(event):
        cursor_row = order_tabel.focus()
        contents = order_tabel.item(cursor_row)
        row = contents["values"]
        if row!="":
            itemName.set(row[0])
            itemRate.set(row[1])
            itemQuantity.set(row[2])
            itemgst.set(row[5])
            itemCategory.set(row[4])
            itemStock_Var.set(row[6])
            stock = itemStock_Var.get()
            stock = (re.findall('\d+', stock ))
            stock = float(str(float(stock[0]))+str((stock[1])))
            if lowStock_amount>=stock:
                gif_label.place(x=1315,y=138)
            else:
                gif_label.place(x=10000,y=10000)

    def show_button_operation(event):
        search_entry_Main.set("")
        category = menuCategory.get()
        if os.path.exists(Database_Path_With_Name) == True:
            if category == "All Items":
                load_menu()
            else:
                conn = sqlite3.connect(Database_Path_With_Name)
                c = conn.cursor()
                #c.execute("SELECT * FROM Stock ORDER BY Product_Name ASC")
                c.execute("SELECT * FROM Stock WHERE Product_Category IS :Searchfor ORDER BY Product_Name ASC",{'Searchfor': category})
                menu_tabel.delete(*menu_tabel.get_children())
                items = c.fetchall()
                for items in items:
                    name = (items[0])
                    price = (items[2]) #Sell Price
                    category = (items[1])
                    gst = (items[4])
                    stockQt = (items[5])
                    stockUnit = (items[6])
                    stock = str(stockQt)+" "+str(stockUnit)
                    menu_tabel.insert('',END,values=[name,price,category,gst,stock])
                conn.close()


    def SearchBar_Fun_Main(e):
        category = menuCategory.get()
        if search_entry_Main.get()!="":
            search = str(search_entry_Main.get())+"%"
            if os.path.exists(Database_Path_With_Name) == True:
                if category == "All Items":
                    conn = sqlite3.connect(Database_Path_With_Name)
                    c = conn.cursor()
                    c.execute("SELECT * FROM Stock WHERE P_Code LIKE :Searchfor ORDER BY Product_Name ASC",{'Searchfor': search})
                    menu_tabel.delete(*menu_tabel.get_children())
                    items = c.fetchall()
                    for items in items:
                        name = (items[0])
                        price = (items[2]) #Sell Price
                        category = (items[1])
                        gst = (items[4])
                        stockQt = (items[5])
                        stockUnit = (items[6])
                        stock = str(stockQt)+" "+str(stockUnit)
                        menu_tabel.insert('',END,values=[name,price,category,gst,stock])
                    conn.close()
                else:
                    conn = sqlite3.connect(Database_Path_With_Name)
                    c = conn.cursor()
                    c.execute("SELECT * FROM Stock WHERE P_Code LIKE :Searchfor AND Product_Category IS :Search_Cat ORDER BY Product_Name ASC",{'Searchfor': search,'Search_Cat':category})
                    menu_tabel.delete(*menu_tabel.get_children())
                    items = c.fetchall()
                    for items in items:
                        name = (items[0])
                        price = (items[2]) #Sell Price
                        category = (items[1])
                        gst = (items[4])
                        stockQt = (items[5])
                        stockUnit = (items[6])
                        stock = str(stockQt)+" "+str(stockUnit)
                        menu_tabel.insert('',END,values=[name,price,category,gst,stock])
                    conn.close()
        elif search_entry_Main.get()=="":
            load_menu()

    def clear_button_operation():
        global old_Discount
        itemName.set("")
        itemRate.set("")
        itemQuantity.set("")
        itemCategory.set("")
        itemgst.set("")
        itemdis.set("")
        itemStock_Var.set("")
        roundoff_Check.set(0)
        old_Discount = 0.0
        gif_label.place(x=130015,y=13008)

    def cancel_button_operation():
        names = []
        for i in menu_category:
            names.extend(list(order_dict[i].keys()))
        if len(names)==0:
            messagebox.showinfo("Error", "Your order list is Empty")
            return
        ans = messagebox.askquestion("Cancel Order", "Are You Sure to Cancel Order?")
        if ans=="no":
            return
        order_tabel.delete(*order_tabel.get_children())
        for i in menu_category:
            order_dict[i] = {}
        clear_button_operation()
        update_total_price()

    def update_button_operation():
        global old_Discount
        name = itemName.get()
        rate = itemRate.get()
        category = itemCategory.get()
        quantity = itemQuantity.get()
        gst =itemgst.get()
        dis = 0.0
        stock = itemStock_Var.get()
        stock = (re.findall('\d+', stock ))
        stock = float(str(float(stock[0]))+str((stock[1])))
        if float(quantity) > stock:
            messagebox.showinfo("Error! Low Stock", "Item Quantity More Than Present Stock")
            return
        if itemdis.get() != "":
            dis = float(itemdis.get())
        if category=="":
            return
        if name not in order_dict[category].keys():
            messagebox.showinfo("Error", "Item is not in your order list")
            return
        if order_dict[category][name][2]==quantity and dis==old_Discount:
            messagebox.showinfo("Error", "No changes in Quantity Or Discount")
            return
        order_dict[category][name][2] = quantity
        cal =float(rate)*int(quantity)
        gs = cal*float(gst)/100.0
        to = cal+gs
        order_dict[category][name][3] = str(to)
        dis=old_Discount
        load_order()

    def remove_button_operation():
        name = itemName.get()
        category = itemCategory.get()

        if category=="":
            return
        if name not in order_dict[category].keys():
            messagebox.showinfo("Error", "Item is not in your order list")
            return
        del order_dict[category][name]
        load_order()

    total_price_For_Pay = 0

    def PayAmount_Fun(e):
        global total_price_For_Pay
        if Pay_Amount_Var.get() != "":
            pay = float(Pay_Amount_Var.get())
            due = float(total_price_For_Pay - pay)
            if due == 0.0:
                Due_Amount_Var.set("-NIL-")
            elif due < 0:
                messagebox.showwarning("Error","Amount Is Bigger Than Total Price")
                Pay_Amount_Var.set("0")
                return
            elif due != 0.0:
                due = "{:.2f}".format(due)
                Due_Amount_Var.set(due)
            #total_price_For_Pay = 0



    def update_total_price():
        global old_Discount,total_price_For_Pay
        price = 0
        for i in menu_category:
            for j in order_dict[i].keys():
                price += float(order_dict[i][j][3])
        if price == 0:
            totalPrice.set("")
        else:
            dis = 0.0
            if itemdis.get() != "":
                dis = float(itemdis.get())
                old_Discount=dis
            discounted = price-dis
            if  discounted > 0:
                #discounted = "{:.2f}".format(discounted)
                discounted = float("{:.2f}".format(discounted))
                if roundoff_Check.get() == 1:
                    discounted =round(float(discounted))
                total_price_For_Pay = discounted
                totalPrice.set("₹ "+str(discounted)+" /-")
            else:
                messagebox.showerror("Error","Please Enter A Valid Discount Amount")
                if roundoff_Check.get() == 1:
                    price = round(float(price))
                total_price_For_Pay = price
                totalPrice.set("₹ "+str(price)+" /-")
                itemdis.set("")
        PayAmount_Fun(0)

    def Round_Off_fun ():
        update_total_price()


    def bill_button_operation(e):
        if Due_Amount_Var.get() == "-NIL-" or Due_Amount_Var.get() != "":
            global Products
            customer_name = customerName.get()
            customer_contact = customerContact.get()
            customer_add = customerAddress.get()
            names = []
            for i in menu_category:
                names.extend(list(order_dict[i].keys()))
            if len(names)==0:
                messagebox.showinfo("Error", "Your order list is Empty")
                return
            if customer_name=="" or customer_contact=="" or customer_add=="":
                messagebox.showinfo("Error", "Customer Details Required")
                return
            if not customerContact.get().isdigit():
                messagebox.showinfo("Error", "Invalid Customer Contact")
                return

            def countDigit(n):
                count = 0
                while n != 0:
                    n //= 10
                    count += 1
                return count
            n = int(customer_contact)
            c = countDigit(n)
            if c != 10:
                messagebox.showinfo("Error", "Invalid Customer Number")
                return
            ans = messagebox.askquestion("Generate Bill", "Are You Sure to Generate Bill?")
            if ans=="yes":
                Bill_Con_Win = Toplevel()
                Bill_Con_Win.title("Bill")
                w = 500
                h = 500
                ws = Bill_Con_Win.winfo_screenwidth()
                hs = Bill_Con_Win.winfo_screenheight()
                x = (ws/2) - (w/2)
                y = (hs/2) - (h/2)
                Bill_Con_Win.geometry('%dx%d+%d+%d' % (w, h, x, y))
                Bill_Con_Win.resizable(False,False)
                Bill_Con_Header_Top = Frame(Bill_Con_Win)
                Bill_Con_Header_Top.pack(fill=BOTH)

                Bill_Con_Header = Frame(Bill_Con_Win)
                Bill_Con_Header.pack(fill=BOTH)

                Label(Bill_Con_Header_Top,text="   Bill No. : "+"123456",font=("Franklin Gothic Demi",10)).pack(side=LEFT)
                Label(Bill_Con_Header_Top,text="Date : "+str(today.strftime("%d/%m/%Y")+"   "),font=("Franklin Gothic Demi",10)).pack(side=RIGHT)
                Label(Bill_Con_Header_Top,text="      Time : "+str(datetime.now().strftime("%H:%M:%S")),font=("Franklin Gothic Demi",10)).pack()

                #Label(Bill_Con_Header,text=" ",font=("arial",1),height=1).pack()
                Label(Bill_Con_Header,text="Name : "+customerName.get(),font=("Franklin Gothic Book",12)).pack()
                Label(Bill_Con_Header,text="Mobile No. : "+customerContact.get(),font=("Franklin Gothic Book",12)).pack()
                Label(Bill_Con_Header,text="Address : "+customerAddress.get(),font=("Franklin Gothic Book",12)).pack()

                Bill_Con_Body = Frame(Bill_Con_Win)
                Bill_Con_Body.pack(fill=BOTH)


                scrollbar_billCon_x = Scrollbar(Bill_Con_Body,orient=HORIZONTAL)
                scrollbar_billCon_y = Scrollbar(Bill_Con_Body,orient=VERTICAL)

                style = ttk.Style()
                style.configure("Treeview.Heading",font=("arial",13, "bold"))
                style.configure("Treeview",font=("arial",12),rowheight=25)

                billCon_table_Stock = ttk.Treeview(Bill_Con_Body,style = "Treeview",
                            columns =("name","quantity","rate","gst","total"),height=7,xscrollcommand=scrollbar_billCon_x.set,
                            yscrollcommand=scrollbar_billCon_y.set)

                billCon_table_Stock.heading("name",text="Product Name")
                billCon_table_Stock.heading("quantity",text="Quantity")
                billCon_table_Stock.heading("rate",text="Rate")
                billCon_table_Stock.heading("gst",text="GST (%)")
                billCon_table_Stock.heading("total",text="Total")

                billCon_table_Stock["displaycolumns"]=("name", "quantity","rate", "gst", "total")
                billCon_table_Stock["show"] = "headings"

                billCon_table_Stock.column("name")
                billCon_table_Stock.column("quantity",width=72,anchor='center')
                billCon_table_Stock.column("rate",width=50,anchor='center')
                billCon_table_Stock.column("gst",width=34,anchor='center')
                billCon_table_Stock.column("total",width=72,anchor='center')



                scrollbar_billCon_x.pack(side=BOTTOM,fill=X)
                scrollbar_billCon_y.pack(side=RIGHT,fill=Y)

                scrollbar_billCon_x.configure(command=billCon_table_Stock.xview)
                scrollbar_billCon_y.configure(command=billCon_table_Stock.yview)

                billCon_table_Stock.pack(fill=BOTH,expand=1)

                t = 0

                for i in menu_category:
                    for j in order_dict[i].keys():
                        lis = order_dict[i][j]
                        #name = lis[0]
                        billCon_table_Stock.insert('',END,values=[lis[0],lis[2],lis[1],lis[5],lis[3]])
                        t = t+float(lis[3])

                if itemdis.get() != "":
                    di = float(itemdis.get())
                else:
                    di = 0
                gt = t - di

                Bill_Con_Footer = Frame(Bill_Con_Win)
                Bill_Con_Footer.pack(fill=BOTH)

                Label(Bill_Con_Footer,text="   Total",font=("Arial Rounded MT",12)).pack(side=LEFT)
                Label(Bill_Con_Footer,text=str(t)+"   ",font=("Arial Rounded MT Bold",12)).pack(side=RIGHT)

                Bill_Con_Footer2 = Frame(Bill_Con_Win)
                Bill_Con_Footer2.pack(fill=BOTH)

                Label(Bill_Con_Footer2,text="   Discount",font=("Arial Rounded MT",12)).pack(side=LEFT)
                Label(Bill_Con_Footer2,text="(-)"+str(di)+"   ",font=("Arial Rounded MT Bold",12)).pack(side=RIGHT)

                LineCan2 = Canvas(Bill_Con_Win,height=5)
                LineCan2.pack(fill=BOTH)
                LineCan2.create_line(12, 4, 486,4)

                Bill_Con_Footer3 = Frame(Bill_Con_Win)
                Bill_Con_Footer3.pack(fill=BOTH)

                if roundoff_Check.get() == 0:
                    Label(Bill_Con_Footer3,text="   Grand Total",font=("Arial Rounded MT",12)).pack(side=LEFT)
                    Label(Bill_Con_Footer3,text=str(gt)+"   ",font=("Arial Rounded MT Bold",12)).pack(side=RIGHT)

                elif roundoff_Check.get() == 1:
                    Label(Bill_Con_Footer3,text="   Grand Total *",font=("Arial Rounded MT",12)).pack(side=LEFT)
                    Label(Bill_Con_Footer3,text=str(round(gt))+"   ",font=("Arial Rounded MT Bold",12)).pack(side=RIGHT)

                Bill_Con_Footer4 = Frame(Bill_Con_Win)
                Bill_Con_Footer4.pack(fill=BOTH)

                Label(Bill_Con_Footer4,text="   Paid",font=("Arial Rounded MT",12)).pack(side=LEFT)
                Label(Bill_Con_Footer4,text=str(Pay_Amount_Var.get())+"   ",font=("Arial Rounded MT Bold",13)).pack(side=RIGHT)


                Bill_Con_Footer5 = Frame(Bill_Con_Win)
                Bill_Con_Footer5.pack(fill=BOTH)

                Label(Bill_Con_Footer5,text="   Due",font=("Arial Rounded MT",12)).pack(side=LEFT)
                Label(Bill_Con_Footer5,text=str(Due_Amount_Var.get())+"   ",font=("Arial Rounded MT Bold",13)).pack(side=RIGHT)

                Bill_Con_Footer_Btn = Frame(Bill_Con_Win)
                Bill_Con_Footer_Btn.pack(side=RIGHT,anchor=S)

                def update_ST_after_B():
                    p_name = []
                    P_stock = []
                    for i in menu_category:
                        for j in order_dict[i].keys():
                            lis = order_dict[i][j]
                            name = lis[0]
                            quantity = float(lis[2])
                            stock = lis[6]
                            p_name.append(name)
                            #print(p_name)
                            #print(stock)
                            #stock = (re.findall('\d+', stock ))
                            #stock = float(str(float(stock[0]))+str((stock[1])))
                            P_stock.append(float(stock)-float(quantity))
                    conn = sqlite3.connect(Database_Path_With_Name)
                    c = conn.cursor()
                    for i in range (len(p_name)):
                        name = p_name[i]
                        qty = P_stock[i]
                        c.execute("""UPDATE Stock SET
                                    Stock_Qty          = :Qty
                                    WHERE Product_Name = :_Name""",{'_Name'  : name,
                                                                    'Qty'    : qty})
                    conn.commit()
                    conn.close()
                def save_pdf ():
                    for i in menu_category:
                        for j in order_dict[i].keys():
                            lis = order_dict[i][j]
                            name = lis[0]
                            PRODUCTNAME.set(name)
                            rate = lis[1]
                            RATE.set(float(rate))
                            quantity = lis[2]
                            QUANTITY.set(int(quantity))
                            price = float(rate)*int(quantity)#lis[3]
                            discount=0#itemdis.get()
                            tax=price*lis[5]/100#itemgst.get()
                            TAX.set(tax)
                            x = (name,int(quantity),float(rate),float(discount),float(price),float(tax))
                            Products.append(x)

                    Products.pop()
                    SubmitData()
                    update_ST_after_B()
                    order_tabel.delete(*order_tabel.get_children())
                    for i in menu_category:
                        order_dict[i] = {}
                    clear_button_operation()
                    update_total_price()
                    customerName.set("")
                    customerContact.set("")
                    customerAddress.set("")
                    Products.clear()
                    Pay_Amount_Var.set("")
                    Due_Amount_Var.set("")
                    Bill_Con_Win.destroy()
                    root.focus()
                    root.focus_force()
                    load_menu()

                printer = PhotoImage(file=_path+"print.png",master=Bill_Con_Win)
                pdf = PhotoImage(file=_path+"pdf.png",master=Bill_Con_Win)

                Label(Bill_Con_Footer_Btn,text=" ",font=("Arial Rounded MT",4)).pack(side=RIGHT)
                Button(Bill_Con_Footer_Btn,image = printer,text="Save & Print Bill",compound=RIGHT).pack(side=RIGHT)
                Label(Bill_Con_Footer_Btn,text=" ",font=("Arial Rounded MT",14)).pack(side=RIGHT)
                Button(Bill_Con_Footer_Btn,image = pdf,text="Save Bill As PDF",compound=RIGHT,command=save_pdf).pack(side=RIGHT)

                Bill_ic = _path+"B_Icon.png"

                Bill_Con_Win.tk.call('wm', 'iconphoto', Bill_Con_Win._w, PhotoImage(file=Bill_ic,master=Bill_Con_Win))
                #Bill_Con_Winiconphoto(False, p1)

                Bill_Con_Win.mainloop()
        else:
            messagebox.showinfo("Error", "Enter Pay Amount")


    #[name,rate,quantity,str(int(rate)*int(quantity)),category]
    #==================Backend Code Ends===============

    #================Frontend Code Start==============
    root = Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    root.title("Welcome to (Your Company Name Here)")
    root.wm_iconbitmap(_path+"Burger.ico")
    #root.attributes('-fullscreen', True)
    #root.resizable(0, 0)

    #---------------------
    PRODUCTNAME = StringVar(root)
    QUANTITY = IntVar(root)
    RATE = DoubleVar(root)
    TAX = DoubleVar(root)
    DISCOUNT=DoubleVar(root)

    #---------------------------





    #================Title==============
    style_button = ttk.Style()
    style_button.configure("TButton",font = ("arial",10,"bold"),background="lightgreen")

    title_frame = Frame(root, bd=8, bg="yellow", relief=GROOVE)
    title_frame.pack(side=TOP, fill="x")

    title_label = Label(title_frame, text="Your Company Name Here",
                        font=("times new roman", 20, "bold"),bg = "yellow", fg="red", pady=5)
    title_label.pack(side = LEFT)


    Label(title_frame, text="   ",bg = "yellow", fg="yellow").pack(side = RIGHT)

    Label(title_frame, text="   ",bg = "yellow", fg="yellow").pack(side = RIGHT)



    #add_button = ttk.Button(item_frame3, text="Add Item"
    #                        ,command=add_button_operation)
    #add_button.grid(row=0,column=0,padx=40,pady=30)

    #==============Customer=============
    customer_frame = LabelFrame(root,text="Customer Details",font=("times new roman", 15, "bold"),
                                bd=8, bg="lightblue", relief=GROOVE)
    customer_frame.pack(side=TOP, fill="x")

    customer_name_label = Label(customer_frame, text="Name",
                        font=("arial", 15, "bold"),bg = "lightblue", fg="blue")
    customer_name_label.grid(row = 0, column = 0)

    customerName = StringVar()
    customerName.set("")
    customer_name_entry = Entry(customer_frame,width=20,font="arial 15",bd=5,
                                    textvariable=customerName)
    customer_name_entry.grid(row = 0, column=1,padx=50)

    customer_contact_label = Label(customer_frame, text="Contact",
                        font=("arial", 15, "bold"),bg = "lightblue", fg="blue")
    customer_contact_label.grid(row = 0, column = 2)

    customerContact = StringVar()
    customerContact.set("")
    customer_contact_entry = Entry(customer_frame,width=20,font="arial 15",bd=5,
                                    textvariable=customerContact)
    customer_contact_entry.grid(row = 0, column=3,padx=50)


    #
    customer_address_label = Label(customer_frame, text="Address",
                        font=("arial", 15, "bold"),bg = "lightblue", fg="blue")
    customer_address_label.grid(row = 0, column = 4)

    customerAddress = StringVar()
    customerAddress.set("")

    customer_address_Entry = Entry(customer_frame,width=20,font="arial 15",bd=5,
                                    textvariable=customerAddress)
    customer_address_Entry.grid(row = 0, column=5,padx=50)




    #===============Menu===============
    menu_frame = Frame(root,bd=8, bg="lightgreen", relief=GROOVE)
    menu_frame.place(x=0,y=125,height=585,width=680)

    menu_label = Label(menu_frame, text="Menu",
                        font=("times new roman", 20, "bold"),bg = "lightgreen", fg="red", pady=0)
    menu_label.pack(side=TOP,fill="x")

    menu_category_frame = Frame(menu_frame,bg="lightgreen",pady=10)
    menu_category_frame.pack(fill="x")

    combo_label = Label(menu_category_frame,text="Category",
                        font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
    combo_label.grid(row=0,column=0)

    menuCategory = StringVar(root)
    search_entry_Main=StringVar(root)

    Label(menu_category_frame,text="  Search  ",
                        font=("arial", 12, "bold"),bg = "lightgreen", fg="blue").grid(row=0,column=2)

    def Clear_SearchBar_Fun_Main ():
        search_entry_Main.set("")
        SearchBar_Fun_Main(0)

    Search_icon = PhotoImage(file=_path+"Se.png",master=root)
    del_icon_Root = PhotoImage(file=_path+"del.png",master=root)



    search_Bar_Main = Entry(menu_category_frame,textvariable=search_entry_Main,font=("Lucida Fax",13),width=26,bd=1)
    search_Bar_Main.grid(row=0,column=3)
    Label(menu_category_frame,text=" ",font=("arial", 1),bg="lightgreen").grid(row=0,column=4)
    search_Bar_Main.bind('<Return>', SearchBar_Fun_Main)
    search_Bar_Main.bind('<KeyRelease>', SearchBar_Fun_Main)

    Button(menu_category_frame,image= Search_icon,bg="lightgreen",activebackground="lightblue",bd=0,command=lambda:SearchBar_Fun_Main(0)).grid(row=0,column=5)

    Button(menu_category_frame,image= del_icon_Root,bd=0,activebackground="white",bg="white",font=("DubaiMedium",10),compound=LEFT,command=Clear_SearchBar_Fun_Main).place(x=604,y=4)

    ############################# Menu Tabel ##########################################
    menu_tabel_frame = Frame(menu_frame)
    menu_tabel_frame.pack(fill=BOTH,expand=1)

    scrollbar_menu_x = Scrollbar(menu_tabel_frame,orient=HORIZONTAL)
    scrollbar_menu_y = Scrollbar(menu_tabel_frame,orient=VERTICAL)

    style = ttk.Style()
    style.configure("Treeview.Heading",font=("arial",13, "bold"))
    style.configure("Treeview",font=("arial",12),rowheight=25)

    menu_tabel = ttk.Treeview(menu_tabel_frame,style = "Treeview",
                columns =("name","price","category","gst","stock"),xscrollcommand=scrollbar_menu_x.set,
                yscrollcommand=scrollbar_menu_y.set)

    menu_tabel.heading("name",text="Name")
    menu_tabel.heading("price",text="Price (Rs)")
    menu_tabel.heading("gst",text="Gst (%)")
    menu_tabel["displaycolumns"]=("name", "price", "gst")
    menu_tabel["show"] = "headings"
    menu_tabel.column("price",width=50,anchor='center')
    menu_tabel.column("gst",width=30,anchor='center')

    scrollbar_menu_x.pack(side=BOTTOM,fill=X)
    scrollbar_menu_y.pack(side=RIGHT,fill=Y)

    scrollbar_menu_x.configure(command=menu_tabel.xview)
    scrollbar_menu_y.configure(command=menu_tabel.yview)

    menu_tabel.pack(fill=BOTH,expand=1)


    load_menu()


    combo_menu = ttk.Combobox(menu_category_frame,font=("Arial",10,"bold"),state="readonly",values=menu_category,textvariable=menuCategory)
    combo_menu.grid(row=0,column=1,padx=10)
    combo_menu.bind("<<ComboboxSelected>>", show_button_operation)


    menu_tabel.bind("<ButtonRelease-1>",load_item_from_menu)
    menu_tabel.bind('<Return>', load_item_from_menu)

    ###########################################################################################

    #===============Item Frame=============
    item_frame = Frame(root,bd=8, bg="lightgreen", relief=GROOVE)
    item_frame.place(x=680,y=125,height=230,width=680)

    item_title_label = Label(item_frame, text="Item",
                        font=("times new roman", 20, "bold"),bg = "lightgreen", fg="red")
    item_title_label.pack(side=TOP,fill="x")

    item_frame2 = Frame(item_frame, bg="lightgreen")
    item_frame2.pack(fill=X)

    item_name_label = Label(item_frame2, text=" Name  ",
                        font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
    item_name_label.grid(row=0,column=0)

    itemCategory = StringVar()
    itemCategory.set("")

    itemName = StringVar()
    itemName.set("")
    item_name = Entry(item_frame2, font="arial 12",textvariable=itemName,state=DISABLED, width=25)
    item_name.grid(row=0,column=1,padx=15)

    item_rate_label = Label(item_frame2, text="                   Rate ",
                        font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
    item_rate_label.grid(row=0,column=2,padx=14)

    itemRate = StringVar()
    itemRate.set("")
    item_rate = Entry(item_frame2, font="arial 12",textvariable=itemRate,state=DISABLED, width=10)
    item_rate.grid(row=0,column=3,padx=10)

    item_quantity_label = Label(item_frame2, text="    Quantity",
                        font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
    item_quantity_label.grid(row=1,column=0,pady =25)
    #.place(x=0,y=52)

    def Qty_Dis_Enter_Press (e):
        name = itemName.get()
        category = itemCategory.get()
        if category=="":
            return

        if name not in order_dict[category].keys():
            add_button_operation()
        else:
            update_button_operation()


    itemQuantity = StringVar()
    itemQuantity.set("")
    item_quantity = Entry(item_frame2, font="arial 12",textvariable=itemQuantity, width=10)
    item_quantity.place(x=101,y=51)
    item_quantity.bind("<Return>", Qty_Dis_Enter_Press)


    #93

    item_Stock_label = Label(item_frame2, text="                    Stock",font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
    item_Stock_label.grid(row=1,column=2)
    #place(x=215,y=45)

    itemgst = StringVar()
    itemgst.set("")

    itemStock_Var = StringVar()
    itemStock_Var.set("")

    item_Stock = Entry(item_frame2, font="arial 12",state=DISABLED,textvariable=itemStock_Var, width=10)
    item_Stock.grid(row=1,column=3,pady =25)
    #place(x=266,y=45)

    Label(item_frame2, text="      ",font=("arial", 12, "bold"),bg = "lightgreen", fg="lightgreen").grid(row=1,column=5,pady =25)


    item_Dis_label = Label(item_frame2, text="  Discount",font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
    item_Dis_label.place(x=211,y=50)
    #place(x=388,y=45)

    itemdis = StringVar()
    itemdis.set("")

    item_Dis = Entry(item_frame2, font="arial 12",textvariable=itemdis, width=10)
    item_Dis.place(x=310,y=51)
    item_Dis.bind("<Return>", Qty_Dis_Enter_Press)


    item_frame3 = Frame(item_frame, bg="lightgreen")
    item_frame3.pack(fill=X)

    add_button = ttk.Button(item_frame3, text="Add Item"
                            ,command=add_button_operation)
    add_button.grid(row=0,column=0,padx=23,pady=16)

    remove_button = ttk.Button(item_frame3, text=" Remove Item "
                            ,command=remove_button_operation)
    remove_button.grid(row=0,column=1,padx=23,pady=16)

    update_button = ttk.Button(item_frame3, text="Update"
                            ,command=update_button_operation)
    update_button.grid(row=0,column=2,padx=23,pady=16)

    clear_button = ttk.Button(item_frame3, text="Clear",
                            width=8,command=clear_button_operation)
    clear_button.grid(row=0,column=3,padx=23,pady=16)

    cancel_button = ttk.Button(item_frame3, text="Clear All",command=cancel_button_operation)
    cancel_button.grid(row=0,column=4,padx=23,pady=16)

    frameCnt_gif = 2

    path = _path+"Red.gif"
    frames = [PhotoImage(file=path,format = 'gif -index %i' %(i)) for i in range(frameCnt_gif)]


    def update(ind):

        frame = frames[ind]
        ind += 1
        if ind == frameCnt_gif:
            ind = 0
        gif_label.configure(image=frame)
        root.after(500, update, ind)


    gif_label = Label(root,bg="lightgreen")
    #gif_label.place(x=1315,y=138)
    gif_label.after(0, update, 0)






    #==============Order Frame=====================
    order_frame = Frame(root,bd=8, bg="lightgreen", relief=GROOVE)
    order_frame.place(x=680,y=335,height=370,width=680)

    order_title_label = Label(order_frame, text="Your Order",
                        font=("times new roman", 20, "bold"),bg = "lightgreen", fg="red")
    order_title_label.pack(side=TOP,fill="x")

    ############################## Order Tabel ###################################
    order_tabel_frame = Frame(order_frame)
    order_tabel_frame.place(x=0,y=40,height=260,width=663)

    scrollbar_order_x = Scrollbar(order_tabel_frame,orient=HORIZONTAL)
    scrollbar_order_y = Scrollbar(order_tabel_frame,orient=VERTICAL)

    order_tabel = ttk.Treeview(order_tabel_frame,
                columns =("name","rate","quantity","price","category","gst","stock"),xscrollcommand=scrollbar_order_x.set,
                yscrollcommand=scrollbar_order_y.set)

    order_tabel.heading("name",text="Name")
    order_tabel.heading("rate",text="Rate")
    order_tabel.heading("quantity",text="Quantity")
    order_tabel.heading("price",text="Price")
    order_tabel.heading("gst",text="GST (%)")
    order_tabel["displaycolumns"]=("name", "rate","quantity","gst","price")
    order_tabel["show"] = "headings"
    order_tabel.column("rate",width=88,anchor='center', stretch=NO)
    order_tabel.column("quantity",width=88,anchor='center', stretch=NO)
    order_tabel.column("gst",width=88,anchor='center', stretch=NO)
    order_tabel.column("price",width=100,anchor='center', stretch=NO)

    def remove_Item_Shortcut(e):
        remove_button_operation()


    order_tabel.bind("<ButtonRelease-1>",load_item_from_order)
    order_tabel.bind("<Delete>",remove_Item_Shortcut)

    scrollbar_order_x.pack(side=BOTTOM,fill=X)
    scrollbar_order_y.pack(side=RIGHT,fill=Y)

    scrollbar_order_x.configure(command=order_tabel.xview)
    scrollbar_order_y.configure(command=order_tabel.yview)

    order_tabel.pack(fill=BOTH,expand=1)

    ###########################################################################################

    total_price_label = Label(order_frame, text="Total",
                        font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
    total_price_label.pack(side=LEFT,anchor=SW,padx=2,pady=10)

    totalPrice = StringVar()
    totalPrice.set("")
    total_price_entry = Entry(order_frame, font="arial 12",textvariable=totalPrice,state=DISABLED,
                                width=10)
    total_price_entry.pack(side=LEFT,anchor=SW,padx=8,pady=11)

    roundoff_Check = IntVar()

    Checkbutton(order_frame, text ='Round\nOff',takefocus = 0,activebackground="lightgreen",bg="lightgreen",variable=roundoff_Check,offvalue = 0,command=Round_Off_fun).pack(side=LEFT,anchor=SW,padx=2,pady=2)

    Label(order_frame, text="Pay",
                        font=("arial", 12, "bold"),bg = "lightgreen", fg="blue").pack(side=LEFT,anchor=SW,padx=8,pady=10)

    Pay_Amount_Var = StringVar()
    Due_Amount_Var = StringVar()




    Pay_Entry =  Entry(order_frame, font="arial 12",textvariable=Pay_Amount_Var,width=10)
    Pay_Entry.pack(side=LEFT,anchor=SW,padx=2,pady=11)
    Pay_Entry.bind("<KeyRelease>", PayAmount_Fun)
    Pay_Entry.bind("<Return>", PayAmount_Fun)

    Label(order_frame, text="Due",
                        font=("arial", 12, "bold"),bg = "lightgreen", fg="blue").pack(side=LEFT,anchor=SW,padx=8,pady=10)


    Entry(order_frame, font="arial 12",textvariable=Due_Amount_Var,state=DISABLED,width=10).pack(side=LEFT,anchor=SW,padx=2,pady=11)



    bill_button = ttk.Button(order_frame, text="Bill",width=8,
                            command=lambda:bill_button_operation(0))
    bill_button.pack(side=LEFT,anchor=SW,padx=40,pady=10)

    #cancel_button = ttk.Button(order_frame, text="Cancel",command=cancel_button_operation)
    #cancel_button.pack(side=LEFT,anchor=SW,padx=20,pady=10)


    def onhover_company_Web_Btn(e):
        company_Web_Btn['fg'] = "red"
    def onleave_company_Web_Btn(e):
        company_Web_Btn['fg'] = "blue"

    company_Web_Btn = Button(root,text="©HrishikeshPatra",fg="blue",bd=0,command= lambda: webbrowser.open_new_tab("https://github.com/Hrishikesh7665"))
    company_Web_Btn.place(x=1250,y=702)#.pack(side=BOTTOM,anchor=NE)
    company_Web_Btn.bind('<Enter>', onhover_company_Web_Btn)
    company_Web_Btn.bind('<Leave>', onleave_company_Web_Btn)

    lowStock_amount = 50

    def showAbout():
        messagebox.showinfo("About","Developed By\nHrishikesh Patra")
        #about_Frame.place(x=-60,y=0)

    def showShortcut():
        messagebox.showinfo("Shortcut Keys List","Ctrl + S = Search For Product\nCtrl + N = Customer Name\nCtrl + C = Customer Contact\nCtrl + A Customer Address\nCtrl + I = Open Inventory Management\nCtrl + R = On\Off Round Off\nCtrl + Q = Enter Item Quantity\nCtrl + D = Item Discount\nDel = Delete A Single Item From Your Order\nCtrl + Del = Clear All\nCtrl + P = Pay Amount\nCtrl + B = Generate Bill\n1st Time Press Enter On Quantity\Discount To Add Item Press Enter 2nd Time To Update")



    def open_Inventory ():
        global what_NXT
        what_NXT = "Open Inventory"
        root.destroy()

    def open_summery ():
        global what_NXT
        what_NXT = "Open Summery"
        root.destroy()


    menubar = Menu(root)


    def open_All_Bill_R():
        desktop2 = desktop+"\\"
        subprocess.Popen(f'explorer "{desktop2}"')

    def open_Today_Bill_R():
        desktop2 = PATH_Bill+"\\"
        subprocess.Popen(f'explorer "{desktop2}"')


    m1=Menu(menubar,tearoff=0)
    m1.add_command(label="Open Today Bills Record's",command=open_Today_Bill_R)
    m1.add_command(label="Open All Bills Record's",command=open_All_Bill_R)

    m2=Menu(menubar,tearoff=0)
    m2.add_command(label="Inventory",command=open_Inventory)
    m2.add_command(label="Stock Summery",command=open_summery)

    menubar.add_cascade(label="Bill Records",menu=m1)
    menubar.add_cascade(label="Stock Management",menu=m2)

    menubar.add_command(label="Shortcut Keys", command=showShortcut)
    menubar.add_command(label="About", command=showAbout)

        # display the menu
    root.config(menu=menubar)

    def root_close_window():
        global what_NXT
        a = messagebox.askyesno("Exit Conformation", "Are You Want To Exit?")
        if a == True:
            what_NXT = ""
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", root_close_window)
    root.state('zoomed')
    root.mainloop()

def main_driver():
    main_fun()
    return what_NXT


#main_driver()