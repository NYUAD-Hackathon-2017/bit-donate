from pymongo import MongoClient
from  pprint import pprint
import datetime


def addDonation(client,first,last,email,tid):
    id=-1
    print(client )
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
        id=doners.update({"_id": result['_id']},{
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
        id=doners.insert_one(post).inserted_id
    return id
def listDonations(client):
    doners = client.doners
    result = doners.find()
    return list(result)
    
