import socket
#Load Settings
settings=open("settings", "r")
paramaters=settings.read().split("\n")
settings.close()

PORT=paramaters[0]
