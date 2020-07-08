'''
-----------------------------------------------
SERVER CODE FOR MANAGEMENT OF INCOMING REQUESTS
-----------------------------------------------
'''

#Importing required packages
import pyrebase
import time
import os
import threading
import json

#Global variables
CommandStreamCount = 0
ScheduleStreamCount = 0

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
      "apiKey": "AIzaSyAOEVrJnc1hL2vQGyboxvGbYlh2Ij39xTo",
      "authDomain": "logiswitch-2020.firebaseapp.com",
      "databaseURL": "https://logiswitch-2020.firebaseio.com",
      "storageBucket": "logiswitch-2020.appspot.com",
      "serviceAccount": "logiswitch-2020-firebase-adminsdk-k8xry-b0c8f8675f.json"
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
        --> Regulators
        --> SSID
        --> password
    CommandStream
    OutputStream
    ScheduleStream
    '''
    # Setup of basic Framework
    basicFramework = {'UserData':{'000001':{'UserID':'000001','Email':'united.intelligence.ltd@gmail.com','Password':'Qas123@#$','Username':'United Intelligence','Devices':'1234567890'}},\
                      'DeviceData':{'1234567890':{'Regulators':'0','SSID':'Chirag-2','Passwd':'chirag12357','DeviceID':'1234567890','DeviceType':'4','DeviceOwner':'000001'}},\
                      'CommandStream':{'000001':'Free'},\
                      'OutputStream':{'1234567890':'Free'},\
                      'ScheduleStream':{"000001" : {"R0001" : {"Active" : "True","Command" : "1234567890-3-1/1234567890-2-0","InitialDelay" : "6","Repeat" : "20"}}}}
    #Pushing basic framework onto database
    FDB.set(basicFramework)
    print('Database now has basic working framework')

def startStreams(FDB):
    '''
    This function starts a listener stream for listening to changes made on the database
    Streams required:
        --> CommandStream
        --> ScheduleStream
    '''
    global StreamCount
    #creating stream function
    #change variable is the variable that contains info on changes detected
    def CommandStream(change):
        #Variable to keep track of initial false change
        global CommandStreamCount
        CommandStreamCount += 1
        if CommandStreamCount > 1:
            event = change['event'] #Put, Delete etc
            path = change['path'] #/{uid}
            data = change['data'] #data after change
            #if command to handle only put commands
            if event == 'put':
                #command received, processing
                handleSimpleEvent(FDB,path,data)
        else:
            print('CommandStream is ready')
    
    def ScheduleStream(change):
        #Variable to keep track of initial false change
        global ScheduleStreamCount
        ScheduleStreamCount += 1
        if ScheduleStreamCount > 1:
            event = change['event'] #Put, Delete etc
            path = change['path'] #/{uid}
            data = change['data'] #data after change
            #if command to handle only put commands
            if event == 'put':
                #command received, processing
                handleScheduleEvent(FDB,path,data,event)
        else:
            print('ScheduleStream is ready')
    #begin stream on commandstream
    CommandStreamCount = 0
    ScheduleStreamCount = 0
    Stream1 = FDB.child("CommandStream").stream(CommandStream)
    Stream2 = FDB.child("ScheduleStream").stream(ScheduleStream)
    #Creating a threaded function for debug commands
    #x = threading.Thread(target=handleDebugCommand,args=(FDB,))
    #start thread
    #x.start()

def handleSimpleEvent(FDB,path,data):
    '''
    Handles incoming commands
    to-do:
        --> check if user is allowed to access device --> check if
        device can handle request --> send command, or Schedule command
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
                #building command
                print('Command received from User',path,'sucsessfully')
                destination = command[0]
                directiveCommand = command[1]+'-'+command[2]
                FDB.child('OutputStream').update({destination:directiveCommand})
            else:
                print('Error, Device',command[0],"was accessed with incorrect device type")
        else:
            print('ERROR: User',path,'has accessed a device which they do not own')
    except TypeError:
        print('ERROR: Device',command[0],"was accessed, but doesn't exist!")

#function to handle Scheduling commands
def handleScheduleEvent(FDB,path,data,event):
    '''
    This function handles Scheduling tasks
    to-do:
        --> check if user has authorization
        --> check if device is correct type
        --> start a thread that waits for given delay, then checks active tag
        --> uses all channels to broadcast commands
    '''
    #Only allow new shedule requests
    if event == "put" and data != None:
        #threaded function
        def delayFunction(FDB,path,command,delay,repeat,index):
            #first delay, then repeat
            if index<0:
                time.sleep(int(delay))
            else:
                time.sleep(int(repeat[index]))
            #increase index
            index+=1
            if index>=len(repeat):
                index=0
            #get data of schedule
            data = FDB.child('ScheduleStream').child(path).get().val()
            data = json.loads(json.dumps(data))
            active = data['Active']
            #if active, continue, otherwise stop and delete
            if active == 'True':
                print('Schedule',path,'Executed')
                #send command to firebase
                FDB.child('OutputStream').update(command_dict)
                #repeat routine
                delayFunction(FDB,path,command,delay,repeat,index)
            else:
                print('Schedule',path,'Cancelled')
                #delete schedule
                FDB.child('ScheduleStream').child(path).remove()
        if len(path.split('/')) == 3:
            #New routine added
            #creating command list
            command = data['Command'].split('/')
            #creating command dict
            command_dict = {}
            #formation of command dict
            for i in command:
                j = i.split('-')
                #add to dict
                if j[0] in command_dict.keys():
                    command_dict[j[0]] = command_dict[j[0]]+'/'+j[1]+'-'+j[2]
                else:
                    command_dict[j[0]] = j[1]+'-'+j[2]
            #Verification of owner
            #get owner id
            owner = path.split('/')[1]
            #flag to verify tests
            flag = True
            for i in command_dict.keys():
                #get device data from firebase
                deviceData = FDB.child('DeviceData').child(i).get().val()
                deviceData = json.loads(json.dumps(deviceData))
                #check registered owner
                if deviceData['DeviceOwner'] != owner:
                    #not owned by sender
                    flag = False
                    break
                #checking device type
                indivisualCommand = command_dict[i]
                for j in indivisualCommand.split('/'):
                    k = j.split('-')
                    #comparing switch number and device type
                    if k[0] > deviceData['DeviceType']:
                        flag = False
                        break
            if flag:
                #Starting thread for schedule
                thread = threading.Thread(target=delayFunction, args=(FDB,path,command_dict,data['InitialDelay'],data['Repeat'].split('-'),-1))
                thread.start()
            else:
                print('Something went wrong with schedule',path)
            
#Initialize server
initServer()
