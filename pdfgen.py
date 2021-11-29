import qrcode
import webbrowser
from reportlab.pdfgen import canvas
import PIL.Image
def getTotal(list):
  total=0
  for data in list:
    total=total+data[4]
  return total

def getTotalTax(list):
  totalTax=0
  for data in list:
    totalTax=totalTax+data[5]
  return totalTax

def getTotalDis(list):
  totalDis=0
  for data in list:
    totalDis=totalDis+data[3]
  return totalDis

def rightalingn(pdf,string,left,right,ycoordinate):
  length=len(string)
  totalLength=(right-left)/7
  spaces=int(totalLength-length)
  pdf.drawString(right,ycoordinate," "*spaces)
  left=left+(7*spaces)
  pdf.drawString(left,ycoordinate,string)

def header(header,pdf):
  pdf.setTitle(header.date+"Invoice")
  # logo="logo.jpeg"
  # pdf.drawInlineImage(logo,190,253)

  pdf.line(30,815,350,815)
  pdf.setFont("Courier-Bold",20)
  pdf.drawString(30,800,"Your Company Name")
  pdf.setFont("Courier-Bold",11)
  pdf.drawString(30,785,"yourcompanywebsite.com")
  pdf.drawString(30,770,"Facebook@yourcompanypage")
  pdf.drawString(30,755,"West Bengal. Phone: +91 XXXXX XXXXX")

  pdf.line(30,753,350,753)

  pdf.drawString(30,735,"Invoice Number: "+ str(int(header.InvoiceNumber)))
  pdf.drawString(30,720,"Customer Name: "+ str(header.CustomerName))
  pdf.drawString(30,705,"Contact Number: "+ str(header.CustomerContact))
  pdf.drawString(30,690,"Date: "+ str(header.date))

  qr = qrcode.QRCode(
    version=1,
    box_size=5,
    border=2
  )

  #data = 'InvoiceNumber:'+str(int(header.InvoiceNumber))+'\nTime:'+(header.date+"--"+header.time)+"\nGoogle Map: https://goo.gl/maps/DV59uHs2eoYpuvsC9\nTerms & Conditions:\n1:Sold items will not be returned or changed.\n2:Every dispute will settled in Mau Court.\n3:Battery, Charger, Mobile warranty is provided by service center.\nTHANK YOU"
  data = "https://github.com/Hrishikesh7665"
  qr.add_data(data)
  qr.make(fit=True)
  img = qr.make_image(fill='black', back_color='white')
  #logo = (image_string)
  #img = PIL.Image.open("C:/Users/Hrishikesh/OneDrive/Documents/Programing Work/Python Projects/New Project (A)/InvoiceGenerator-master/LOGO.png")
  pdf.drawInlineImage(img,400,685)


def middle(pdf):
  pdf.line(30,677,550,677)

  pdf.drawString(30,668,"Sr.No.")
  pdf.drawString(75,668,"Product Name")
  #pdf.drawString(200,668,"Product Name")
  pdf.drawString(260,668,"Quantity")
  pdf.drawString(320,668,"Rate")
  pdf.drawString(400,668,"Total")
  pdf.drawString(490,668,"GST")

  pdf.line(30,662,550,662)
  pdf.line(73,677,73,150)
  #pdf.line(198,677,198,150)
  pdf.line(258,677,258,150)
  pdf.line(318,677,318,150)
  pdf.line(398,677,398,150)
  pdf.line(488,677,488,150)
  pdf.line(30,150,550,150)

def additem(product,pdf,ycoordinate):
  while(len(product.name)>18):
    pdf.drawString(75,ycoordinate,product.name[:18]+"-")
    product.name=product.name[18:]
    ycoordinate=ycoordinate-15
  qt = str(product.quantity)
  pdf.drawString(75,ycoordinate,product.name)
  #pdf.drawString(260,ycoordinate,str(product.quantity))
  rightalingn(pdf,qt,260,295,ycoordinate)

  rightalingn(pdf,"%.2f" %product.rate,320,398,ycoordinate)
  #rightalingn(pdf,"%.2f" %product.discount,320,398,ycoordinate)
  rightalingn(pdf,"%.2f" %product.total,400,488,ycoordinate)
  rightalingn(pdf,"%.2f" %product.tax,490,552,ycoordinate)
  return (ycoordinate-15)

def footer(pdf,list,roundoff_Check,dis):
  pdf.drawString(30,135,"Total Discount:")
  rightalingn(pdf,"-"+"%.2f" %dis+" INR",393,488,135)
  pdf.drawString(30,120,"Gross Total(Discount Included):")
  grossTotal = getTotal(list)-dis
  rightalingn(pdf,"%.2f" %grossTotal+" INR",400,488,120)
  pdf.drawString(30,105,"GST:")
  rightalingn(pdf,"+"+"%.2f" %getTotalTax(list)+" INR",393,488,105)
  pdf.line(30,100,550,100)
  pdf.drawString(30,90,"Grand Total: ")
  grand_Total= getTotal(list)+getTotalTax(list)-dis
  if roundoff_Check == 1:
        grand_Total = round(float(grand_Total))
        grand_Total = float(grand_Total)
  rightalingn(pdf,"%.2f" %grand_Total+" INR",400,488,90)
  pdf.drawString(400,50,"Authorized Signatory")
  pdf.setFont("Courier-Bold",7)
  #pdf.drawString(15,15,"Scan QR code for Applied Terms & Conditions.")


def footer_for_Due(pdf,list,roundoff_Check,dis,due):
  pdf.drawString(30,135,"Total Discount:")
  rightalingn(pdf,"-"+"%.2f" %dis+" INR",393,488,135)
  pdf.drawString(30,120,"Gross Total(Discount Included):")
  grossTotal = getTotal(list)-dis
  rightalingn(pdf,"%.2f" %grossTotal+" INR",400,488,120)
  pdf.drawString(30,105,"GST:")
  rightalingn(pdf,"+"+"%.2f" %getTotalTax(list)+" INR",393,488,105)
  pdf.line(30,100,550,100)
  pdf.drawString(30,90,"Grand Total: ")
  pdf.drawString(30,75,"Amount Pay: ")
  pdf.drawString(30,60,"Amount Due: ")
  grand_Total= getTotal(list)+getTotalTax(list)-dis
  if roundoff_Check == 1:
        grand_Total = round(float(grand_Total))
        grand_Total = float(grand_Total)
  rightalingn(pdf,"%.2f" %grand_Total+" INR",400,488,90)
  rec = grand_Total-due
  rightalingn(pdf,"%.2f" %rec+" INR",400,488,75)
  rightalingn(pdf,"%.2f" %due+" INR",400,488,60)
  pdf.drawString(400,25,"Authorized Signatory")
  pdf.setFont("Courier-Bold",7)
  #pdf.drawString(15,15,"Scan QR code for Applied Terms & Conditions.")