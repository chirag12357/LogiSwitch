import random
piexists = True
while exists:
    registration_no = str(random.randint(1000000000,9999999999))
    with open("Registered.txt","r") as f:
    	registered = f.read().split("\n")
    f=open("Registered.txt","a+")
    if registration_no not in registered:
      f.write(registration_no+"\n")
      exists = False


f=open("src/Registration.cpp","r")
code = f.read().split("\n")
print(registration_no)
DeviceType = input("Enter Device type : ")
code[20]="const char* Registration_no="+'"'+registration_no+'"'+';'
code[19]="const char* DeviceType="+'"'+DeviceType+'"'+';'
code[83]='Firebase.set("/DeviceData/'+registration_no+'"'+',Registration_no);'
code[41]='Firebase.stream("/OutputStream/'+registration_no+'");'
