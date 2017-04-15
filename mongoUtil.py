from pymongo import MongoClient
from  pprint import pprint
import datetime


def addDonation(client,first,last,email,tid,country):
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
            "country" : country,
            "donation": [
                {
                    "tid": tid,
                    "timestamp": datetime.datetime.utcnow()
                },
            ]
        }
        doners.insert(post)
    return "{}_{}_{}".format(first,last,email)
def listDonations(client):
    doners = client.doners
    result = doners.find()
    return list(result)

def getDonersAllDonations(client,id):
    doners = client.doners
    params=id.split('_')
    first=params[0]
    last=params[1]
    email=params[2]
    result= doners.find_one(
      {"$and":
        [
            {'email': email},
            {'first': first},
            {'last': last}
        ]
    })
    if result:
        donations=result['donation']
        return donations
    else:
        return "no id found"

