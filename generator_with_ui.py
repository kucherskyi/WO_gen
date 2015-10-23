# -*- coding: UTF-8 -*-

import requests
import json
from suds import tostr
import time
from Tkinter import *
import random
import datetime
import os
import urllib2


def sendWo():
    
    def addSecs(tm, secs):
        fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
        fulldate = datetime.datetime.now().replace(microsecond=0) + \
                   datetime.timedelta(seconds=secs)
        return fulldate
    
    workoutType = 11
    workoutId = 0
    deviceId = 8
    zoneType = 0
    hrMonitorPresent = "false"
    strideSensorPresent = "false"
    speedCellPresent = "false"
    startTime = datetime.datetime.now().replace(microsecond=0)
    times = 0
    strideRate = 0
    distance = 0
    pace = 0
    steps = 0
    endTi = wotime.get()
    speedArray = 0
    endTime = addSecs(startTime, endTi)
    timestr =time.strftime("%Y%d%m-%H%M%S") + ".json"
    calories = 0
    avgHeartRate = 0
    maxHR = 0
    minHR = 0
    counte = 0
    heartRate = 80
    wonamemain = woname.get()
    sens = """  "sensors": [
        {
          "name": "FIT SMART",
          "calibrationFactor": 1.0000000,
          "lastUpdated": "2015-06-17T12:46:08Z",
          "serial": "D0:62:1B:C1:55:F6",
          "type": "batelliSDM"
        },
        {
          "type": "hrm",
          "name": "HRM_test",
          "serial": "qwerty123",
          "calibrationFactor": 1.0000000,
          "lastUpdated": "2013-10-28T16:14:33Z"
        },
      ], \n"""
      
          
    # random.sample(4, 3)
    # maxSpeed =  max(speedArray)
    # avgSpeed = sum(speedArray) / float(len(speedArray))
    
#--------------------------------------------------------
#   GENERATE WORKOUT
#--------------------------------------------------------

    file = open(timestr, "w")
    
    #     {
    #       "type": "hrm",
    #       "name": "HRM_test",
    #       "serial": "qwerty123",
    #       "calibrationFactor": 1.0000000,
    #       "lastUpdated": "2013-10-28T16:14:33Z"
    #     },
    
    file.write("{\n")
    file.write('"zoneType": "paceZone",\n')
    file.write('"startDateTime":"')
    file.write(str(startTime.isoformat())+"Z")
    file.write('" ,\n')
    file.write('"stopDateTime":"')
    file.write(str(endTime.isoformat())+"Z")
    file.write('" ,\n')
    file.write(' "fitnessZones": [], \n')
    file.write('"deviceType": "batelli",\n')
    file.write(sens)
    # file.write(' "events": [], \n')
    file.write(' "dataPoints": [\n')

    while times <= endTi:
                file.write("{\n")
                file.write('"timeFromStart":')
                file.write(str(times))
                file.write(",\n")
                file.write('"heartRate":')
                file.write(str(heartRate))
                file.write(",\n")
                file.write('"strideRate": ')
                file.write(str(strideRate))
                file.write(",\n")
                file.write('"steps":')
                file.write(str(steps))
                file.write(",\n")
                # file.write( '"calories":')
                # file.write(str(calories))
                # file.write( ",\n")
                file.write('"pace":')
                file.write(str(pace))
                file.write(",\n")
                file.write('"distance":')
                file.write(str(distance))
                file.write("\n")
                if times == endTi:
                    file.write("} \n")
                else:
                    file.write("},\n")
                calories = int(distance / 100)
                times = times + 5
                steps = steps + random.randint(5, 15)
                strideRate = random.randint(80, 180)
                heartRate = random.randint(120, 160)
                distanceDelta = random.randint(8, 19)
                distance = distance + distanceDelta
                pace = int(5.0 / distanceDelta * 1000)
                avgHeartRate += heartRate
                counte += 1
    
    avgHeartRate = int(avgHeartRate/counte)
    file.write("],\n")
    file.write(''' "gears": [], \n''')
    file.write(' "stats": { "avgHeartRate": ' + str(avgHeartRate) + '}, \n')
    file.write('"workoutType": "free",\n')
    file.write('"workoutName": "'+wonamemain+'",\n')
    file.write('"activityType": "run"\n')
    file.write("}\n")
    file.close()
    
#--------------------------------------------------------
#   POST WORKOUT
#--------------------------------------------------------

    email = mail.get()
    password = pword.get()
    envi = env.get() 
    authInfo = json.dumps({'email': str(email), 'password': str(password)})
    WOjson = open(timestr,'r')  
    lamble = Label().pack_forget()
    if envi == 1:
        
        urlAuthDev = "http://api.devdesign.micoach.adidas.com/v3/OAuth2/Authorize" 
        headersAuthDev = {'Host': 'api.devdesign.micoach.adidas.com',
                          'Connection': 'keep-alive',
                          'Authorization': 'Basic c2VjcmV0Q2xpZW50OjY0OGNlZmNmOWMyZTQ3ZmU5YWZjMzA4MjZhYTFhZWNl',
                          'Origin': 'http://api.devdesign.micoach.adidas.com',
                          'Referer': 'http://api.devdesign.micoach.adidas.com/consumer/Home/Login'
                          }
        r = requests.post(urlAuthDev, headers=headersAuthDev, data=authInfo)
        if r.status_code == 200:
            lamble = Label (root, text = '200 Authorised').grid(row=10,column=0, sticky=W) 
        resp_body = r.json()
        userId = str(resp_body[u'userId'])
        accessToken = str(resp_body[u'accessToken'])
        urlGetDev = "https://api.devdesign.micoach.adidas.com/v3/Users/" + userId + "/workouts"
        headersPostDev = {'Host': 'api.devdesign.micoach.adidas.com',
                          'Content-Type': 'application/json; charset=UTF-8',
                          'Connection': 'keep-alive',
                          'Proxy-Connection': 'keep-alive',
                          'Cookie': 'adidas_country=v3; TS01237701=01b0ab2260cd1c92c3d669db1f4bcd2100c5dc7296bae67905f05bc001a34050d004819de4',
                          'Authorization': 'Bearer ' + accessToken
                          }
        b = requests.post(urlGetDev, headers=headersPostDev, data=WOjson.read(), verify=False)
        if b.status_code == 201:
            lamble = Label (root, text = '201 Posted').grid(row=11,column=0, sticky=W)
    elif envi == 2:
        urlAuthTest = "http://api.test.micoach.adidas.com/v3/OAuth2/Authorize" 
        headersAuthTest = {'Host': 'api.test.micoach.micoach.adidas.com',
                           'Connection': 'keep-alive',
                           'Authorization': 'Basic c2VjcmV0Q2xpZW50OjY0OGNlZmNmOWMyZTQ3ZmU5YWZjMzA4MjZhYTFhZWNl',
                           'Origin': 'http://api.test.micoach.adidas.com',
                           'Referer': 'http://api.test.micoach.micoach.adidas.com/consumer/Home/Login'
                           }
        r = requests.post(urlAuthTest, headers=headersAuthTest, data=authInfo)
        if r.status_code == 200:
            lamble = Label (root, text = '200 Authorised').grid(row=10,column=0, sticky=W) 
        resp_body = r.json()
        userId = str(resp_body[u'userId'])
        accessToken = str(resp_body[u'accessToken'])
        urlGetTest = "https://api.test.micoach.adidas.com/v3/Users/" + userId + "/workouts"
        headersPostTest = {'Host': 'api.test.micoach.adidas.com',
                           'Content-Type': 'application/json; charset=UTF-8',
                           'Connection': 'keep-alive',
                           'Proxy-Connection': 'keep-alive',
                           'Cookie': 'adidas_country=v3; TS01237701=01b0ab2260cd1c92c3d669db1f4bcd2100c5dc7296bae67905f05bc001a34050d004819de4',
                           'Authorization': 'Bearer ' + accessToken 
                           }
        b = requests.post(urlGetTest, headers=headersPostTest, data=WOjson.read(), verify=False)
        if b.status_code == 201:
            lamble = Label (root, text = '201 Posted').grid(row=11,column=0, sticky=W)
    elif envi == 3:
        urlAuthStag = "http://api.staging.micoach.adidas.com/v3/OAuth2/Authorize" 
        headersAuthStaging = {'Host': 'api.staging.micoach.adidas.com',
                              'Connection': 'keep-alive',
                              'Authorization': 'Basic c2VjcmV0Q2xpZW50OjY0OGNlZmNmOWMyZTQ3ZmU5YWZjMzA4MjZhYTFhZWNl',
                              'Origin': 'http://api.staging.micoach.micoach.adidas.com',
                              'Referer': 'http://api.staging.micoach.adidas.com/consumer/Home/Login'
                              }
        r = requests.post(urlAuthStag, headers=headersAuthStaging, data=authInfo)
        if r.status_code == 200:
            lamble = Label (root, text = '200 Authorised').grid(row=10,column=0, sticky=W) 
        resp_body = r.json()
        userId = str(resp_body[u'userId'])
        accessToken = str(resp_body[u'accessToken'])
        urlGetStaging = "https://api.staging.micoach.adidas.com/v3/Users/" + userId + "/workouts"
        headersPostStaging = {'Host': 'api.staging.micoach.adidas.com',
                              'Content-Type': 'application/json; charset=UTF-8',
                              'Connection': 'keep-alive',
                              'Proxy-Connection': 'keep-alive',
                              'Cookie': 'adidas_country=v3; TS01237701=01b0ab2260cd1c92c3d669db1f4bcd2100c5dc7296bae67905f05bc001a34050d004819de4',
                              'Authorization': 'Bearer ' + accessToken 
                              }
        b = requests.post(urlGetStaging, headers=headersPostStaging, data=WOjson.read(), verify=False)
        if b.status_code == 201:
            lamble = Label (root, text = '201 Posted').grid(row=11,column=0, sticky=W)
    elif envi == 4:
        urlAuth = "http://api.micoach.adidas.com/v3/OAuth2/Authorize" 
        headersAuth = {'Host': 'api.micoach.adidas.com',
                       'Connection': 'keep-alive',
                       'Authorization': 'Basic c2VjcmV0Q2xpZW50OjY0OGNlZmNmOWMyZTQ3ZmU5YWZjMzA4MjZhYTFhZWNl',
                       'Origin': 'http://api.micoach.adidas.com',
                       'Referer': 'http://api.micoach.adidas.com/consumer/Home/Login'
                       }
        r = requests.post(urlAuth, headers=headersAuth, data=authInfo)
        if r.status_code == 200:
            lamble = Label (root, text = '200 Authorised').grid(row=10,column=0, sticky=W)
        elif r.status_code == 401:
            lamble = Label (root, text = str (r.status_code) + ' Unauthorized!').grid(row=10,column=0, sticky=W)
            
        else: 
            lamble = Label (root, text = str (r.status_code) + ' ERROR!').grid(row=10,column=0, sticky=W)
        resp_body = r.json()
        userId = str(resp_body[u'userId'])
        accessToken = str(resp_body[u'accessToken'])
        urlGet = "https://api.micoach.adidas.com/v3/Users/" + userId + "/workouts"
        headersPost = {'Host': 'api.micoach.adidas.com',
                       'Content-Type': 'application/json; charset=UTF-8',
                       'Connection': 'keep-alive',
                       'Proxy-Connection': 'keep-alive',
                       'Cookie': 'adidas_country=v3; TS01237701=01b0ab2260cd1c92c3d669db1f4bcd2100c5dc7296bae67905f05bc001a34050d004819de4',
                       'Authorization': 'Bearer ' + accessToken 
                       }
        b = requests.post(urlGet, headers=headersPost, data=WOjson.read(), verify=False)
        #lamble = Label (root, text = '...').grid(row=11,column=0, sticky=W)
        b = requests.post(urlGet, headers=headersPost, data=WOjson.read(), verify=False)
        if b.status_code == 201:
            lamble = Label (root, text = '201 Posted').grid(row=11,column=0, sticky=W)
            
        else:
            lamble = Label (root, text = str(r.status_code) + ' ERROR!').grid(row=11,column=0, sticky=W)
        
    return


def closeWo():
    root.quit()
    

#--------------------------------------------------------
#   FORM
#--------------------------------------------------------

root=Tk()

#   Variables inside form

mail = StringVar()
pword = StringVar()
env=IntVar()
woname=StringVar()
wotime=IntVar()

#   Form look

root.geometry('250x300')
root.title("Micoach Workouter")
root.resizable(False, False)

#--------------------------------------------------------
#   FORM VARIABLES
#--------------------------------------------------------

just_text1 = Label(root, text = "EMAIL")
mail_enter = Entry (root, textvariable=mail)
just_text2 = Label(root, text = "PASSWORD")
pass_enter = Entry (root, textvariable=pword)

woname_text = Label(root, text = "Name of WO")
woname_enter = Entry (root, textvariable=woname)
wotime_text = Label(root, text = "Time of WO (in sec.)")
wotime_enter = Entry (root, textvariable=wotime)

dev=Radiobutton(root,text='Dev',variable=env,value=1)
test=Radiobutton(root,text='Test',variable=env,value=2)
staging=Radiobutton(root,text='Staging',variable=env,value=3)
prod=Radiobutton(root,text='Prod',variable=env,value=4)

send_Button = Button(root,text="Send", width = 10, command=sendWo)
close_Button = Button (root, text="Close", width = 10, command= closeWo)

#--------------------------------------------------------
#   FORM BUILDER
#--------------------------------------------------------

just_text1.grid(row=0,column=0, sticky=W)
mail_enter.grid(row=1,column=0,columnspan=2, sticky=W)
just_text2.grid(row=2,column=0, sticky=W)
pass_enter.grid(row=3,column=0, sticky=W)

dev.grid(row=4,column=0, sticky=W)
test.grid(row=4,column=1, sticky=W)
staging.grid(row=5,column=0, sticky=W)
prod.grid(row=5,column=1, sticky=W)

woname_text.grid(row=6,column=0, sticky=W)
woname_enter.grid(row=7,column=0, sticky=W)
wotime_text.grid(row=8,column=0, sticky=W)
wotime_enter.grid(row=9,column=0,  sticky=W)

send_Button.grid(row=14,column=0, sticky=W)
close_Button.grid(row=14,column=1, sticky=S)

root.mainloop()
