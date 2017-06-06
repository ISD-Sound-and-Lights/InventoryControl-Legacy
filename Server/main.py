import socket
import pickle
import threading

#Load Settings
settings=open("settings.conf", "r")
paramaters=settings.read().split("\n")
settings.close()
HOST=''
PORT=int(paramaters[0])

# Define classes
class globalvars: #This class exists because im an idiot, PM me to find out more
    itemCount = 0
    locationCount = 0
    next_free_item_id = 0
    next_free_location_id = 0
    item_selected_id = 0
    loc_selected_id = 0

var = globalvars()


class Location:
    def __init__(self, name, id):
        self.name = name
        self.id = id
class Item:
    locationid = -1
    def __init__(self, name, id, location):
        self.name = name
        self.id = id
        self.locationid = location
class Version:
    def __init__(self, id, itemDiff = "", locationDiff = ""):
        self.id = id
        self.itemDiff = itemDiff
        self.locationDiff = locationDiff

items = []
locations = []
versions={}

genItems = []
genLocations = []

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

    versionfile = open("versions.csv", "w")
    for version,mod in versions.items():
        versionfile.write(version + "," + mod.itemDiff + "," + mod.locationDiff+"\n")

def load():
    try:
        open("items.csv", "r").close()
    except FileNotFoundError:
        open("items.csv", "w").close()

    itemfile = open("items.csv", "r")
    rows = itemfile.read().split("\n")
    itemfile.close()
    for row in rows:
        values = row.split(",")
        if not values == ['']:
            var.next_free_item_id += 1
            var.itemCount += 1
            items.append(Item(values[0], int(values[1]),values[2]))
            items[var.itemCount - 1].locationid = int(values[2])
            items[var.itemCount - 1].selectid = var.itemCount-1

    try:
        open("locations.csv", "r").close()
    except FileNotFoundError:
        open("locations.csv", "w").close()

    locationfile = open("locations.csv", "r")
    rows = locationfile.read().split("\n")
    locationfile.close()
    for row in rows:
        values = row.split(",")
        if not values == ['']:
            var.next_free_location_id\
                += 1
            var.locationCount += 1
            locations.append(Location(values[0],int(values[1])))
            locations[var.locationCount - 1].selectid = var.locationCount - 1

    try:
        open("versions.csv").close()
    except FileNotFoundError:
        open("versions.csv", "w").close()

    versionfile = open("versions.csv")

    rows = versionfile.read().split("\n")
    for row in rows:
        values = row.split(",")
        if not values == ['']:
            versions[values[0]]=Version(values[0],itemDiff=values[1], locationDiff=values[2])
    versionfile.close()

def generateVersionFrom(version):
    genLocations.clear()
    doGenerate = False # This keeps track of weather or not we have reached the version in the iterator
    for versionID, information in versions.items():
        if versionID == version:
            doGenerate = True # We have got to the point where we need to generate, so we set it to true`
        if doGenerate:
            itemChanges = information.itemDiff.split(".")
            for itemChange in itemChanges:
                if "+" in itemChange:
                    itemChange = itemChange.strip("+")
                    itemChange = itemChange.split(";")
                    genItems.append(Item(itemChange[0],int(itemChange[1]),int(itemChange[2])))
                elif "-" in itemChange:
                    itemChange = itemChange.strip("-")
                    itemChange = itemChange.split(";")
                    index = getGenItemIndexByGlobalId(int(itemChange[1]))
                    del genItems[index]
                elif "=" in itemChange:
                    itemChange = itemChange.strip("=")
                    itemChange = itemChange.split(";")
                    index = getGenItemIndexByGlobalId(itemChange[1])
                    genItems[index].locationid = itemChange[2]
                    genItems[index].name = itemChange[0]
            locationChanges = information.locationDiff.split(".")
            for locationChange in locationChanges:
                if "+" in locationChange:
                    locationChange = locationChange.strip("+")
                    locationChange = locationChange.split(";")
                    genLocations.append(Location(locationChange[0], int(locationChange[1])))
                elif "-" in locationChange:
                    locationChange = locationChange.strip("-")
                    locationChange = locationChange.split(";")
                    index = getGenLocationIndexByGlobalId(int(locationChange[1]))
                    del genLocations[index]
def generateVersionTo(version):
    genLocations.clear()
    doGenerate = True # This keeps track of weather or not we have reached the version in the iterator
    for versionID, information in versions.items():
        if doGenerate:
            itemChanges = information.itemDiff.split(".")
            for itemChange in itemChanges:
                if "+" in itemChange:
                    itemChange = itemChange.strip("+")
                    itemChange = itemChange.split(";")
                    genItems.append(Item(itemChange[0],int(itemChange[1]),int(itemChange[2])))
                elif "-" in itemChange:
                    itemChange = itemChange.strip("-")
                    itemChange = itemChange.split(";")
                    index = getGenItemIndexByGlobalId(int(itemChange[1]))
                    del genItems[index]
                elif "=" in itemChange:
                    itemChange = itemChange.strip("=")
                    itemChange = itemChange.split(";")
                    index = getGenItemIndexByGlobalId(itemChange[1])
                    genItems[index].locationid = itemChange[2]
                    genItems[index].name = itemChange[0]

            locationChanges = information.locationDiff.split(".")
            for locationChange in locationChanges:
                if "+" in locationChange:
                    locationChange = locationChange.strip("+")
                    locationChange = locationChange.split(";")
                    genLocations.append(Location(locationChange[0], int(locationChange[1])))
                elif "-" in locationChange:
                    locationChange = locationChange.strip("-")
                    locationChange = locationChange.split(";")
                    index = getGenLocationIndexByGlobalId(int(locationChange[1]))
                    del genLocations[index]
        if versionID == version:
            doGenerate = False # We have got to the point where we dont want to generate, so we set it to false`

def newItem():
    var.itemCount += 1
    items.append(Item("New Item", var.next_free_item_id))
    var.next_free_item_id += 1

def newLocation():
    var.locationCount += 1
    locations.append(Location("New Location", var.next_free_location_id))
    var.next_free_location_id += 1

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

def getGenItemIndexByGlobalId(identification):
    ga = 0
    for item in genItems:
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
def getGenLocationIndexByGlobalId(identification):
    ga = 0
    for loc in genLocations:
        if loc.id == identification:
            return ga
        else:
            ga += 1
def applyGenToAcual():
    global items
    global locations
    items = genItems
    locations = genLocations

def currentVersion():
    return (list(versions.values())[-1:])[0].id
def generateCurrentVersion():
    generateVersionTo(currentVersion())
def getConentsOfItemFile():
    return open("items.csv").read()
def getContentsOfLocationFile():
    return open("locations.csv").read()
load()
save()

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((HOST, PORT))
def recieveInformation():
    while True:

        soc.listen()
        conn, addr = soc.accept()

        print("Connection recieved from " + str(addr))
        data = conn.recv(1024)
        if not data: break
        recievedData = repr(data)
        recievedData = recievedData[2:-1]
        print("Recieved " + recievedData)
        if not recievedData == "None":
            recievedData = recievedData.split(",")
            versions[recievedData[0]] = Version(recievedData[0], recievedData[1], recievedData[2])
        generateCurrentVersion()
        applyGenToAcual()
        save()
        print("Sending " + repr(getConentsOfItemFile() + ">" + getContentsOfLocationFile() + ">" + currentVersion()))
        conn.sendall((getConentsOfItemFile().replace("\n",";") + ">" + getContentsOfLocationFile().replace("\n",";") + ">" + currentVersion()).encode())

recieveInformation()