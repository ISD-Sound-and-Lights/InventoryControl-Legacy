#!/usr/bin/env python
from tkinter import *
from tkinter.ttk import *

import random
import socket
import pickle
import os

def breaknow(event):
    print("Breaking")

currentSyncVersion = "100000"

# Define classes
class globalvars: #This class exists because im an idiot, PM me to find out more
    itemCount = 0
    locationCount = 0
    next_free_id = 1
    item_selected_id = 0
    loc_selected_id = 0

var = globalvars()


class Location:
    selectid=0
    def __init__(self, name, id, selectid=0):
        self.name = name
        self.id = id
        self.selectid = selectid
class Item:
    selectid=0
    locationid = -1
    def __init__(self, name, id, selectid=0):
        self.name = name
        self.id = id
        self.selectid = selectid

class Version:
    finalItem = ""
    finalLocation = ""
    finalversion = ""
    def __init__(self, id, itemDiff = "", locationDiff = ""):
        self.id = id
        self.itemDiff = itemDiff
        self.locationDiff = locationDiff

    def newItem(self,id):
        self.itemDiff+=str(id)+";"

    def newLocation(self,id):
        self.locationDiff+=str(id)+";"
    def finalise(self):
        itemId = self.itemDiff.split(";")
        locationid = self.locationDiff.split(";")

        for item in items:
            if item.id in itemId:
                self.finalItem += "+" + item.name + ";" + item.id + ";" + item.locationid+"."
        for location in locations:
            if location.id in locationid:
                self.finalLocation += "+" + location.name+";" + location.id+"."
        self.finalItem = self.finalItem[:-1]
        self.finalLocation = self.finalLocation[:-1]
        self.finalversion = currentSyncVersion+","+self.finalItem +","+ self.finalLocation

items = []
locations = []

currentVersion = Version(random.randint(int(currentSyncVersion),1000000))

# Load Settings
# HOST, PORT
try:
    open("settings.conf", "r").close()
except FileNotFoundError:
    open("settings.conf", "w").close()
settings = open("settings.conf", "r")

values=settings.read().split(",")
try:
    HOST = values[0]
    PORT = int(values[1])
except IndexError:
    print("No HOST found in conf file")
    raise IndexError

settings.close()
# Setup tkinter
root = Tk()
root.title("Sound and Lights Inventory System")
root.minsize(width=900, height=420)

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

    locationfile = open("locations.csv", "w")
    for loc in locations:
        locationfile.write(loc.name+",")
        locationfile.write(str(loc.id) + "\n")
    locationfile.close()
    pickle.dump(currentVersion,open("version.p","wb"))

def savebind(event):
    save()


def load():
    global currentVersion
    try:
        open("items.csv", "r").close()
    except FileNotFoundError:
        open("items.csv", "w").close()

    try:
        open("locations.csv", "r").close()
    except FileNotFoundError:
        open("items.csv","w").close()
    itemfile = open("items.csv", "r")
    rows = itemfile.read().split("\n")
    itemfile.close()
    for row in rows:
        values = row.split(",")
        if not values == ['']:
            var.next_free_id += 1
            var.itemCount += 1
            items.append(Item(values[0], int(values[1])))
            items[var.itemCount - 1].locationid = int(values[2])
            items[var.itemCount - 1].selectid = var.itemCount-1


    for item in items:
        valid = False
        trycount = 0
        addtext = ""
        while not valid:
            try:
                itemlist.insert("", var.itemCount, text=item.name + addtext, values=(item.id))
            except TclError:
                trycount += 1
                addtext = str(trycount)
            else:
                valid = True

    locationfile = open("locations.csv", "r")
    rows = locationfile.read().split("\n")
    locationfile.close()
    for row in rows:
        values = row.split(",")
        if not values == ['']:
            var.next_free_id += 1
            var.locationCount += 1
            locations.append(Location(values[0],int(values[1])))
            locations[var.locationCount - 1].selectid = var.locationCount - 1
    for location in locations:
        valid = False
        trycount = 0
        addtext = ""
        while not valid:
            try:
                locationList.insert("", var.locationCount, text=location.name + addtext, values=(location.id))
            except TclError:
                trycount += 1
                addtext = str(trycount)
            else:
                valid = True
    updateItemList()
    currentVersion = pickle.load(open("version.p","rb"))
def updateItemList():
    itemlist.delete(*itemlist.get_children())
    for item in items:
        itemlist.insert("", var.itemCount, text=item.name, values=(item.id,locations[getLocationIndexByGlobalId(item.locationid)].name))
def updateLocationList():
    locationList.delete(*locationList.get_children())
    locationList.delete(*locationList.get_children())
    for location in locations:
        locationList.insert("", var.locationCount,text=location.name,values=(location.id))

def newItem(event):
    var.itemCount += 1
    items.append(Item("New Item", var.next_free_id,selectid=var.itemCount-1))
    itemlist.insert("", var.itemCount, text=items[var.itemCount - 1].name, values=(items[var.itemCount - 1].id))
    currentVersion.newItem(var.next_free_id)
    var.next_free_id += 1

def newLocation(event):
    var.locationCount += 1
    locations.append(Item("New Location", var.next_free_id,selectid=var.locationCount-1))
    locationList.insert("",var.locationCount,text=locations[var.locationCount-1].name, values=(locations[var.locationCount-1].id))
    currentVersion.newLocation(var.next_free_id)
    var.next_free_id += 1

def getItemIndexById(identification):
    ga = 0
    for item in items:
        if item.selectid == identification:
            return ga
        else:
            ga += 1
    print("Item not found")
def getLocationIndexById(identification):
    ga = 0
    for loc in locations:
        if loc.selectid == identification:
            return ga
        else:
            ga += 1
def getLocationIndexByName(name):
    ga = 0
    for loc in locations:
        if loc.name == name:
            return ga
        else:
            ga+=1

def getItemIndexByName(name):
    ga = 0
    for item in items:
        if (item.name == name):
            return ga
        else:
            ga += 1

def getItemIndexByGlobalId(identification):
    ga = 0
    for item in items:
        if item.id == identification:
            return ga
        else:
            ga += 1


def returnAllLocationNames():
    final = []
    for location in locations:
        final.append(location.name)
    return final

def getLocationIndexByGlobalId(identification):
    ga = 0
    for loc in locations:
        if loc.id == identification:
            return ga
        else:
            ga += 1

def select(event):
    #print("Selected Menu Item")
    selected = itemlist.item(itemlist.selection()[0])["values"][0]
    theItem = items[getItemIndexByGlobalId(selected)]

    itemNameEntry.delete(0, "end")
    itemNameEntry.insert(0, theItem.name)
    itemLocationValue.set(locations[getLocationIndexByGlobalId(theItem.locationid)].name)
#    try:
#        itemLocationValue.set(locations[getItemIndexByGlobalId(theItem.locationid)].name)
#    except:
#        pass
    var.item_selected_id = theItem.selectid

def selectLocation(event):
    print("Selected Location Item")
    selected = locationList.item(locationList.selection()[0])["values"][0]
    theLocation = locations[getLocationIndexByGlobalId(selected)]
    locNameEntry.delete(0, "end")
    locNameEntry.insert(0, theLocation.name)
    var.loc_selected_id = theLocation.selectid

def submit(event):
    # print(itemlist.item(itemlist.selection()))
    items[getItemIndexById(var.item_selected_id)].name = itemNameEntry.get()
    items[getItemIndexById(var.item_selected_id)].locationid = locations[getLocationIndexByName(itemLocationValue.get())].id
    updateItemList()

def submitLoc(event):
    global itemLocationSelect
    # print(locationList.item(locationList.selection()))
    print(str(var.loc_selected_id))
    locations[getLocationIndexById(var.loc_selected_id)].name = locNameEntry.get()
    itemLocationSelect["menu"].delete(0, 'end')
    for loc in returnAllLocationNames():
        itemLocationSelect = OptionMenu(root, itemLocationValue, *(["Location"] + returnAllLocationNames()))
        itemLocationSelect.grid(column=1, row=4)

    updateLocationList()
def clearItemName(event):
    if itemNameEntry.get() == "New Item":
        itemNameEntry.delete(0,"end")

def clearLocName(event):
    if(locNameEntry.get() == "New Location"):
        locNameEntry.delete(0,"end")
def deleteItem(event):
    theItem=getItemIndexById(var.item_selected_id)
    del items[getItemIndexById(var.item_selected_id)]
    var.itemCount -= 1
    currentVersion.itemDiff += "-" +theItem.name + ";" + theItem.id+";" + theItem.locationid + "."
    updateItemList()
def deleteLocation(event):
    theLocation = locations[getLocationIndexById(var.loc_selected_id)]
    del locations[getLocationIndexById(var.loc_selected_id)]
    var.locationCount -= 1
    currentVersion.locationDiff += "-" + theLocation.name + ";" + theLocation.id + "."
    updateLocationList()
def sync(event):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((HOST, PORT))

    currentVersion.finalise()
    soc.sendall((currentVersion.finalversion).encode())
    finaldata=""
    while True:
        data = soc.recv(1024)
        if not data: break
        finaldata+=repr(data)

    finaldata=pickle.loads(finaldata)

    soc.close()

    #print("Recieved" + repr(data))
# Item list
itemlist = Treeview(root)
itemlist.heading("#0", text="Item Name")
itemlist["columns"] = ("1", "2")
itemlist.column("1", width=50)
itemlist.heading("1", text="id")
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
newItemButton.grid(row=1, column=1)

# Name entry text field
itemNameEntry = Entry(root, width=25)
itemNameEntry.grid(row=3, column=1)
itemNameEntry.bind("<Button-1>", clearItemName)

# Submit Button
submitButton = Button(root, width=25, text="Submit")
submitButton.grid(row=5, column=1)
submitButton.bind("<Button-1>", submit)

itemDeleteButton = Button(root, width=25, text="Delete")
itemDeleteButton.grid(row=6, column=1)
itemDeleteButton.bind("<Button-1>", deleteItem)

locationList = Treeview(root)
locationList["columns"] = ("1")
itemlist.heading("#0", text="Location Name")
locationList.column("1", width=50)
locationList.heading("1", text="id")  # Initialise GUI
locationList.grid(row=2,column=3)
locationList.bind("<Double-1>", selectLocation)

Label(text="Name:").grid(row=3,column=2)

locNameEntry = Entry(root, width=25)
locNameEntry.grid(row=3, column=3)
locNameEntry.bind("<Button-1>", clearLocName)

locSubmitButton = Button(width=25,text="Submit")
locSubmitButton.grid(row=5,column=3)
locSubmitButton.bind("<Button-1>",submitLoc)

deleteButton = Button(width=25,text="Delete")
deleteButton.grid(row=6,column=3)
deleteButton.bind("<Button-1>",deleteLocation)

newLocButton = Button(text="New Location")
newLocButton.grid(row=1,column=3)
newLocButton.bind("<Button-1>", newLocation)

syncButton = Button(text="Sync")
syncButton.grid(row=5,column=0)
syncButton.bind("<Button-1>", sync)

# Begin loading
load()

# More gui that requires things to be loaded
# Location select
itemLocationValue = StringVar(root)
itemLocationValue.set("None")
itemLocationSelect = OptionMenu(root, itemLocationValue, *(["Location"] + returnAllLocationNames()))
itemLocationSelect.grid(column=1,row=4)

# Start GUI
root.mainloop()