from pymongo import MongoClient
from  pprint import pprint
import datetime


def addDonation(client,first,last,email,tid):
    # print(client )
    first=first.lower()
    last=last.lower()
    email=email.lower()
    doners = client.doners
    result = doners.find_one(
      {"$and":
        [ 
            {'email': email},
            {'first': first},
            {'last': last}
        ]
    })
    if result:
        doners.update({"_id": result['_id']},{
            "$push":
                {'donation':
                    {
                        "tid": 1,
                        "timestamp": datetime.datetime.utcnow()
                    }
                }
        })
    else:    
        post = {
            "first": first,
            "last": last,
            "email": email,
            "donation": [
                {
                    "tid": tid,
                    "timestamp": datetime.datetime.utcnow()
                },
            ]
        }
    return "{}_{}_{}".format(first,last,email)
def listDonations(client):
    doners = client.doners
    result = doners.find()
    return list(result)
    
