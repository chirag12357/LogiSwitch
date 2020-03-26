'''
-----------------------------------------------
SERVER CODE FOR MANAGEMENT OF INCOMING REQUESTS
-----------------------------------------------
'''

#Importing required packages
import pyrebase
import time
import os
#import threading
import json

#Global variables
StreamCount = 0

#initialize server
def initServer():
    '''
    To initialize server, and to create basic template of firebase if not present
    '''
    #Begin Initialization
    print("Initializing SERVER...")
    #Configuration variable to initialize pyrebase
    #Service account is being used as this code is only run by the server, which has admin privileges
    config = {
      "apiKey": "AIzaSyCKD9xqSm1Xbf-QIa6BiDaVqUec0X1fpfk",
      "authDomain": "logiswitch2020.firebaseapp.com",
      "databaseURL": "https://logiswitch2020.firebaseio.com",
      "storageBucket": "logiswitch2020.appspot.com",
      "serviceAccount": "logiswitch2020-firebase-adminsdk-ujnzz-a2c5fab218.json"
    }
    #Firebase is an object of pyrebase that is connected to the project in config file
    firebase = pyrebase.initialize_app(config)
    AUTH = firebase.auth()         #Auth module
    STORAGE = firebase.storage()   #Storage bucket module
    FDB = firebase.database()      #Realtime database module

    try:  #Catch any 401 or 404 requests
        data = FDB.child('UserData').child('000001').get() #get request for data on database
        if str(data.each()) == 'None': #Checking if database is empty
            rebuildBasicDatabaseFramework(FDB) #If database is empty, make basic framework
            startStreams(FDB)
        else:
            #Database has pre-existing data
            print('Server is functional')
            print('Initalization is completed sucsessfully')
            #starting listeners for incoming commands
            startStreams(FDB)
            
    except Exception as e:
        print('error:',e) 

def rebuildBasicDatabaseFramework(FDB):
    '''
    Create the basic framework for normal functioning of application

    Tables to be created:
    UserData:
        --> Email
        --> Username
        --> Password
        --> Devices owned
        --> UserID
    DeviceData:
        --> DeviceID
        --> DeviceType
        --> DeviceOwner
    CommandStream
    OutputStream
    '''
    # Setup of basic Framework
    basicFramework = {'UserData':{'000001':{'UserID':'000001','Email':'united.intelligence.ltd@gmail.com','Password':'Qas123@#$','Username':'United Intelligence','Devices':'1234567890'}},\
                      'DeviceData':{'1234567890':{'Regulators':'0','SSID':'Chirag-2','Passwd':'chirag12357','DeviceID':'1234567890','DeviceType':'4','DeviceOwner':'000001'}},\
                      'CommandStream':{'000001':'Free'},\
                      'OutputStream':{'1234567890':'Free'}}
    #Pushing basic framework onto database
    FDB.set(basicFramework)
    print('Database now has basic working framework')

def startStreams(FDB):
    '''
    This function starts a listener stream for listening to changes made on the database
    Streams required:
        --> CommandStream
    '''
    global StreamCount
    #creating stream function
    #change variable is the variable that contains info on changes detected
    def CommandStream(change):
        global StreamCount
        StreamCount += 1
        if StreamCount > 1:
            event = change['event'] #Put, Delete etc
            path = change['path'] #/{uid}
            data = change['data'] #data after change
            #if command to handle only put commands
            if event == 'put':
                #command received, processing
                handleEvent(FDB,path,data)
        else:
            print('Stream is ready')
    #begin stream on commandstream
    StreamCount = 0
    Stream = FDB.child("CommandStream").stream(CommandStream)
    #Creating a threaded function for debug commands
    #x = threading.Thread(target=handleDebugCommand,args=(FDB,))
    #start thread
    #x.start()

def handleEvent(FDB,path,data):
    '''
    Handles incoming commands
    to-do:
        --> check if user is allowed to access device
        --> check if device can handle request
        --> send command, or shedule command
    '''
    #split command into components [deviceID,switchNo,On/Off,timedelay,repeat]
    command = data.split('-')
    #Get details of device
    data = FDB.child('DeviceData').child(command[0]).get().val()
    #get list of devices owned by the user
    try:
        owner = json.loads(json.dumps(data))['DeviceOwner']
        #split command into components [deviceID,switchNo,On/Off,timedelay,repeat]
        if path.lstrip('/')== owner:
            #Has access to device, can proceed
            devicetype = json.loads(json.dumps(data))['DeviceType']
            if devicetype >= command[1]:
                #perfect access
                print('Access granted')
            else:
                print('Error, Device',command[0],"was accessed with incorrect device type")
        else:
            print('ERROR: User',path,'has accessed a device which they do not own')
    except TypeError:
        print('ERROR: Device',command[0],"was accessed, but doesn't exist!")


#Initialize server
initServer()
