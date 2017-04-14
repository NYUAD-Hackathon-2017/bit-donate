from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
import json

bdb = BigchainDB('http://localhost:9984')
alice = generate_keypair()

money = {
    'data': {
        'transaction': {
            'money_sent': 'rs 50'
        }
    }
}

metadata = {
    'hello': 'world'
}

ptx = bdb.transactions.prepare(
    operation='CREATE',
    signers=alice.public_key,
    asset=money,
    metadata=metadata
)

print(json.dumps(ptx, indent=4))

fulfilled_tx = bdb.transactions.fulfill(
    ptx,
    private_keys=alice.private_key,
)

print(json.dumps(fulfilled_tx, indent=4))

sent_tx = bdb.transactions.send(fulfilled_tx)
assert(sent_tx == fulfilled_tx)
print(sent_tx['id'])


