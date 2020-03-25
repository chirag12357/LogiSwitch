'''
-----------------------------------------------
SERVER CODE FOR MANAGEMENT OF INCOMING REQUESTS
-----------------------------------------------

To-Do:
    --> Create a log file for every transaction that takes place
    --> Make an offline database of every account created
    --> Reroute request from phones to correct device with correct switch code
'''

#Importing required packages
import pyrebase

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
        data = FDB.get() #get request for data on database
        if str(data.each()) == 'None':
            rebuildBasicDatabaseFramework(FDB)
        else:
            print('Server is functional')
    except Exception as e:
        print('error:',e) 

def rebuildBasicDatabaseFramework(FDB):
    '''
    create the basic framework for normal functioning of application

    tables to be created:
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
    basicFramework = {'UserData':{'000001':{'UserID':'000001','Email':'united.intelligence.ltd@gmail.com','Password':'Qas123@#$','Username':'United Intelligence','Devices':'1234567890'}},\
                      'DeviceData':{'1234567890':{'DeviceID':'1234567890','DeviceType':'4','DeviceOwner':'000001'}},\
                      'CommandStream':{'000001':'Free'},\
                      'OutputStream':{'1234567890':'Free'}}
    FDB.set(basicFramework)
initServer()
