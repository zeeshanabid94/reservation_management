# This file generates a fixture.json object for
# reservations. This can be used to generate new
# reservations and load them into the data base

import argparse
import datetime, time, random, json

parser = argparse.ArgumentParser()

args = parser.parse_args()

start = time.time()
users = [
    {  
   "model":"auth.user",
   "pk":1,
   "fields":{  
      "password":"",
      "last_login":None,
      "is_superuser":False,
      "username":"",
      "first_name":"Zeeshan",
      "last_name":"Abid",
      "email":"Zeeshan Abid",
      "is_staff":False,
      "is_active":True,
      "date_joined":"2018-09-19T09:23:22.925Z",
      "groups":[  

      ],
      "user_permissions":[  

      ]
   }
},
{  
   "model":"auth.user",
   "pk":2,
   "fields":{  
      "password":"!Y8GHSrYaF6fjGGGp7DW057C89Yxh8xFpbR9SWGnR",
      "last_login":None,
      "is_superuser":False,
      "username":"AK@hotmail.com",
      "first_name":"Aayush",
      "last_name":"Khanna",
      "email":"AK@hotmail.com",
      "is_staff":False,
      "is_active":True,
      "date_joined":"2018-09-19T23:33:55.000Z",
      "groups":[  

      ],
      "user_permissions":[  

      ]
   }
},
{  
   "model":"auth.user",
   "pk":3,
   "fields":{  
      "password":"!27AFoYBJZ48NUvTtqBzSCeTHfGGbDrfk7N6DRA4b",
      "last_login":None,
      "is_superuser":False,
      "username":"XIng@yang.com",
      "first_name":"XINGIXNG",
      "last_name":"XINGIXNG",
      "email":"XIng@yang.com",
      "is_staff":False,
      "is_active":True,
      "date_joined":"2018-09-20T21:50:32.066Z",
      "groups":[  

      ],
      "user_permissions":[  

      ]
   }
},
{  
   "model":"auth.user",
   "pk":4,
   "fields":{  
      "password":"!d4pdsd33LeDTYUZl388dB6mcQLVUESlfFqxYgQmL",
      "last_login":None,
      "is_superuser":False,
      "username":"dora@explorer.com",
      "first_name":"zeehsna",
      "last_name":"zeehsna",
      "email":"dora@explorer.com",
      "is_staff":False,
      "is_active":True,
      "date_joined":"2018-09-20T21:52:24.614Z",
      "groups":[  

      ],
      "user_permissions":[  

      ]
   }
}
]
reservations = []
reservations.extend(users)
for i in range(1, 4):
    start = start + 3 * random.random() * 86400
    end = start + 3 * random.random() * 86400
    obj = {
        "model":"reservation.reservation",
        "pk":i,
        "fields":{
            "user":i,
            "start_date":int(start),
            "end_date":int(end)
        }
        
    }
    reservations.append(obj)

print(json.dumps(reservations))