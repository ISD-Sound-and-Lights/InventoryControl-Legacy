#!/usr/bin/env python
from tkinter import *
from tkinter.ttk import *


# Define classes
class globalvars:
    itemCount = 1
    next_free_id = 0
    selected_id = 0


var = globalvars()


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

# Load Settings
settings = open("settings.conf", "r")
paramaters = settings.read().split("\n")
settings.close()

HOST = paramaters[0]
PORT = paramaters[1]

# Setup tkinter
root = Tk()
root.title("Sound and Lights Inventory System")
root.minsize(width=700, height=420)

frame = Frame(root)


# Define functions
def save():
    print("Saving")
    itemfile = open("items.csv", "w")
    for item in items:
        itemfile.write(item.name + ",")
        itemfile.write(str(item.id) + ",")
        itemfile.write(str(item.locationid) + "\n")
    itemfile.close()


def savebind(event):
    save()


def load():
    itemfile = open("items.csv", "r")
    rows = itemfile.read().split("\n")
    itemfile.close()
    for row in rows:
        values = row.split(",")
        if not values == ['']:
            items.append(Item(values[0], int(values[1])))
            items[var.itemCount - 1].locationid = values[2]
    for item in items:
        valid = False
        trycount = 0
        addtext = ""
        while not valid:
            try:
                globalvars.next_free_id += 1
                itemlist.insert("", var.itemCount, text=item.name + addtext, values=(item.id))
            except TclError:
                trycount += 1
                addtext = str(trycount)
            else:
                var.itemCount += 1
                valid = True

    locationfile = open("locations.csv", "r")
    rows = locationfile.read().split("\n")
    locationfile.close()
    for row in rows:
        values = row.split(",")
        if not values == ['']:
            locations.append(Location(values[0],int(values[1])))


def updateItemList():
    itemlist.delete(*itemlist.get_children())
    for item in items:
        itemlist.insert("", var.itemCount, text=item.name, values=(item.id))


def newItem(event):
    items.append(Item("New Item", globalvars.next_free_id))
    itemlist.insert("", var.itemCount, text=items[var.itemCount - 1].name, values=(items[var.itemCount - 1].id))
    var.itemCount += 1
    globalvars.next_free_id += 1


def getItemIndexById(identification):
    ga = 0
    for item in items:
        if item.id == identification:
            return ga
        else:
            ga += 1


def getItemIndexByName(name):
    ga = 0
    for item in items:
        if (item.name == name):
            return ga
        else:
            ga += 1


def select(event):
    print("Selected Menu Item")
    selected = itemlist.item(itemlist.selection()[0])["text"]
    theItem = items[getItemIndexByName(selected)]
    itemNameEntry.delete(0, "end")
    itemNameEntry.insert(0, theItem.name)
    var.selected_id = theItem.id


def submit(event):
    print(itemlist.item(itemlist.selection()))
    items[getItemIndexById(var.selected_id)].name = itemNameEntry.get()
    updateItemList()


def locationWindow(event):
    locationwindow = Toplevel(root)
    locationwindow.title("Locations")
    locationwindow.minsize(width=500, height=300)
    # Location treeview
    locationList = Treeview(locationwindow)
    locationList["columns"] = ("1")
    itemlist.heading("#0", text="Location Name")
    locationList.column("1",width=50)
    locationList.heading("1", text="id")  # Initialise GUI
    locationList.pack()

# Item list
itemlist = Treeview(root)
itemlist.heading("#0", text="Item Name")
itemlist["columns"] = ("1", "2")
itemlist.column("1", width=50)
itemlist.heading("1", text="Item ID")
itemlist.column("2", width=200)
itemlist.heading("2", text="Location")
itemlist.bind("<Double-1>", select)
itemlist.grid(row=2, column=1, padx=10, pady=10)

# Nametag
Label(root, text="Name:").grid(row=3, column=0)

# 'Save' Button
saveButton = Button(text="Save")
saveButton.bind("<Button-1>", savebind)
saveButton.grid(row=1, column=0)

# 'Add New' button
newItemButton = Button(text="New Item")
newItemButton.bind("<Button-1>", newItem)
newItemButton.grid(row=0, column=1)

# Name entry text field
itemNameEntry = Entry(root, width=25)
itemNameEntry.grid(row=3, column=1)

# Submit Button
submitButton = Button(root, width=25, text="Submit")
submitButton.grid(row=4, column=1)
submitButton.bind("<Button-1>", submit)

# Begin loading
load()

# Configure options
# 'Locations' Button
locationButton = Button(root, text="Locations")
locationButton.grid(column=5, row=1)
locationButton.bind("<Button-1>", locationWindow)

# Start GUI
root.mainloop()
