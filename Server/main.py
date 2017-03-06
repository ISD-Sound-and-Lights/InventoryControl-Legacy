import socket
#Load Settings
settings=open("settings.conf", "r")
paramaters=settings.read().split("\n")
settings.close()

PORT=paramaters[0]

from tkinter import *
from tkinter.ttk import *


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


items = []
locations = []

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

def load():
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

    print(var.next_free_id)

def newItem():
    var.itemCount += 1
    items.append(Item("New Item", var.next_free_id,selectid=var.itemCount-1))
    var.next_free_id += 1

def newLocation():
    var.locationCount+=1
    locations.append(Item("New Location", var.next_free_id,selectid=var.locationCount-1))
    var.next_free_id+=1

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
def getLocationIndexByGlobalId(identification):
    ga = 0
    for loc in locations:
        if loc.id == identification:
            return ga
        else:
            ga += 1
