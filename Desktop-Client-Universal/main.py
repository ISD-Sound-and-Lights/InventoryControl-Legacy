from tkinter import *
from tkinter.ttk import *

next_free_id = 0
class globalvars:
    itemCount=1
var=globalvars()

class Location:
    def __init__(self, name, id):
        self.name = name
        self.id = id
class Item:
    locationid = -1
    def __init__(self, name, id):
        self.name = name
        self.id = id

items = []
locations = []
#Load Settings
settings = open("settings", "r")
paramaters=settings.read().split("\n")
settings.close()

HOST=paramaters[0]
PORT=paramaters[1]

root=Tk()
root.title("Sound and Lights Inventory Sy stem")
root.minsize(width=700, height=420)

frame = Frame(root)
def save():
    print("Saving")
    itemfile=open("items.csv", "w")
    for item in items:
        itemfile.write(item.name+",")
        itemfile.write(item.id+",")
        itemfile.write(item.locationid+"\n")
    itemfile.close()
def saveButtonEvent(event):
    save()
def load():
    for item in items:
        var.itemCount+=1
        valid=False
        trycount=0
        addtext=""
        while not valid:
            try:
                itemlist.insert("", var.itemCount, text=item.name + addtext,values=(item.id))
            except TclError:
                trycount+=1
                addtext=str(trycount)
            else:
                var.itemCount+=1
                valid=True
def newItem(event):
    items.append(Item("New Item", next_free_id))
    itemlist.insert("", var.itemCount, text=items[var.itemCount-1].name,values=(items[var.itemCount-1].id))
    var.itemCount+=1
items.append(Item("Ubar12", 0))
items.append(Item("Ubar12", 1))
items.append(Item("Ubar12", 2))
#Begin UI Initialisation
#Itemlist
itemlist=Treeview(root)
itemlist.heading("#0", text="Name")
itemlist["columns"]=("1")
itemlist.column("1",width=50)
itemlist.heading("1",text="id")
itemlist.grid(row=2,column=1,padx=10,pady=10)
#Name tag
Label(root,text="Name:").grid(row=3,column=0)
#Add New button
newItemButton=Button(root,text="New Event")
newItemButton.bind("<Button-1>",newItem)
newItemButton.grid(row=0,column=1)
#Save Button
saveButton=Button(root,text="Save")
saveButton.bind(("<Button-1>", saveButtonEvent))
saveButton.grid(row=1,column=0)
#Name Entry
itemNameEntry=Entry(root,width=25)
itemNameEntry.grid(row=3,column=1)

#Begin loading
load()
#Starting UI
root.mainloop()