#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
import cgi, cgitb
import sys

cgitb.enable()
form = cgi.FieldStorage()

def main():

    print "Content-Type: text/html;charset=utf-8"
    print

    # get the value from the hidden field
    loggedInUser = form.getvalue('username')

#checks if the user is logged in
    if loggedInUser != "":
            logged = False
            f = open('Database/LoggedIn.csv', 'rt')
            lines = f.readlines()
            for line in lines:
                users = line.split(",")
                for user in users:
                    if loggedInUser == user:
                        logged = True
                        break
            if not logged:
                error("You are not currently logged in.")
                sys.exit(0)

#opens the inventory and puts its contents into the array
    f=open("Database/Inventory.csv")
    lines=f.readlines()
    inventory=[]
    for line in lines: 
        row=[]
        items = line.split(",") #splits line up by comma
        for item in items:
            row.append(item.strip()) #takes end and beginning characters out
        inventory.append(row)
    f.close()

#intializes the arrays
    quantity =[]
    product = []
    newinventory=[]
    total = []
    name = []
    price = []
    inven = []

#get values from button and textbox
    for i in range(1,4):
        tval = 'Quantity'+str(i)
        cval = 'item'+str(i)
        textbox=form.getvalue(tval)
        checkbox=form.getvalue(cval)
        if (checkbox == "no"):
            quantity.append(textbox)
        else:
            quantity.append(0)

#puts values into arrays
    for i in range(1,len(inventory),1): #starts at 1 to inventory.length step by 1
        obj = inventory[i][0]
        original = inventory[i][1]
        dollar = inventory[i][2]
        name.append(obj)
        price.append(dollar)
        inven.append(original)

#calculates updated quantity
    for j in range(0, len(quantity),1):
        newnewq = int(inven[j])-int(quantity[j])
        if(newnewq<0):
            error(str("Not enough %s speakers in stock."%name[j]))
            sys.exit(0)
        newinventory.append(newnewq)
        unitprice = int(quantity[j])*float(price[j])
        total.append(unitprice)

    #print total
    final  = sum(total)

#puts updated inventory into this file
    f2=open("Database/Inventory.csv","w") #new inventory file created that has new changed inventory
    f2.write("%s,%s,%s\n"%(inventory[0][0],inventory[0][1],inventory[0][2]))
    for index in range(0,len(newinventory)):
        row = index+1
        item = newinventory[index]
        updatedLine = "%s,%s,%s\n"%(inventory[row][0],item,inventory[row][2])
        f2.write(updatedLine) #convert back to string
    f2.close()

    generateBill(loggedInUser, name, quantity, price, final )       

#prints out bill
def generateBill(u, n, v, p, f):
    f = open('Errors/template.html')
    lines = f.readlines()
    for line in lines:
        print line
        if(line.find("<!--Message-->")!=-1):
            total = 0
            print """<table align=center bgcolor="black">"""
            print """<thead><td align=center width=20%>Stereos ordered</td> <td align=center width=20%>Number ordered</td> <td align=center width=20%>Unit Price</td></thead>"""  
            
            for i in range(0,3):
                name = n[i]
                inven = v[i]
                price = p[i]
                print """<tr><td>""" + str(name) + """</td><td>""" + str(inven) + """</td><td>""" + str(price) + """</td></tr>"""
                total = total + float(inven)*float(price)
            print """<tr><td></td><td>Total</td><td>$""" + str(total) + """</td></tr>"""
            print """<tr><td></td><td></td><td><form action="index.html">
            <input type="submit" value="Confirm">
            </form>
            </td></tr></table>"""

#sends out error message
def error(message):
    temp = open('Errors/template.html')
    lines = temp.readlines()
    for line in lines:
        print line
        if(line.find("<!--Message-->")!=-1):
            print "<h2>Error:</h2>"
            print "<p>%s</p>"%message


main()