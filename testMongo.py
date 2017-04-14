from pymongo import MongoClient
from  pprint import pprint
import datetime
client = MongoClient('52.66.27.92', 27017).bitdonate


def addDonation(first,last,email,amount,cc):
  # fill me
    id=0
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
                    "tid": 1,
                    "timestamp": datetime.datetime.utcnow()
                },
            ]
        }
        id=doners.insert_one(post).inserted_id
    return id
def listDonations():
    doners = client.doners
    result = doners.find()
    for record in result:
        pprint(record)
    
def test():
    print(addDonation("ahmad","ilaiwi","sssss",46,"3453345"))
    listDonations()

if __name__ == '__main__':
    test()