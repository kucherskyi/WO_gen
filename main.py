import requests
import json
from suds import tostr
import time
from Tkinter import *

list1=[]

user = 'assd111@mailinator.com'
passw = '1111111a'

authInfo = json.dumps({'email': str(user), 'password': str(passw)})
# authentification info

urlAuthDev = "http://api.test.micoach.adidas.com/v3/OAuth2/Authorize" 
headersAuthDev = {'Host': 'api.test.micoach.adidas.com',
                  'Connection': 'keep-alive',
                  'Authorization': 'Basic c2VjcmV0Q2xpZW50OjY0OGNlZmNmOWMyZTQ3ZmU5YWZjMzA4MjZhYTFhZWNl',
                  'Origin': 'http://api.test.micoach.adidas.com',
                  'Referer': 'http://api.test.micoach.adidas.com/consumer/Home/Login'
                  }
r = requests.post(urlAuthDev, headers=headersAuthDev, data=authInfo,  verify=False)

resp_body = r.json()
userId = str(resp_body[u'userId'])
accessToken = str(resp_body[u'accessToken'])
urlGetDev = "https://api.test.micoach.adidas.com/v3/Users/" + userId + "/workouts?isScheduled=true&isCompleted=false"
headersPostDev = {'Host': 'api.test.micoach.adidas.com',
                  'Content-Type': 'application/json; charset=UTF-8',
                  'Connection': 'keep-alive',
                  'Proxy-Connection': 'keep-alive',
                  'Cookie': 'adidas_country=v3; TS01237701=01b0ab2260cd1c92c3d669db1f4bcd2100c5dc7296bae67905f05bc001a34050d004819de4',
                  'Authorization': 'Bearer ' + accessToken
                  }
b = requests.get(urlGetDev, headers=headersPostDev, verify=False)

re_body = b.json()
userWO = re_body[u'results']
res = {}
for xxx in userWO:
    res[xxx.get('workoutId')] = 'Is ' + xxx.get(u'workoutType') + ' workout' 

for key,value in res.iteritems():
    list1.append(key)


master = Tk()

master.geometry('250x300')

variable = StringVar(master)
variable.set(list1[0]) # default value

w = apply(OptionMenu, (master, variable) + tuple(list1))
w.pack()

mainloop()
