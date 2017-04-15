import config
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

def prepare_and_send(bdb, user, data):
    """
    Prepares and sends a transaction to the blockchain server with the data passed.
    The user passed is used to sign the transaction.

    Returns the id of the transaction just sent.
    """

    prepared_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=user.public_key,
        asset=data,
    )
    fulfilled_tx = bdb.transactions.fulfill(
        prepared_tx,
        private_keys=user.private_key
    )
    return bdb.transactions.send(fulfilled_tx)['id']


def bdb_donate(bdb, user, donater_name, amount):
    """
    Prepares and sends a donate transaction that contains the donater name and the amount
    donated

    Returns the id of the transaction just created.
    """
    tx = {
        'data': {
            'type': 'donation',
            'donater_name': donater_name,
            'amount': amount,
        }
    }
    return prepare_and_send(bdb, user, tx)

def bdb_pay(bdb, user, vendor_name, amount):
    """
    Prepares and sends a pay transaction that contains the vendor name and the amount donated.

    Returns the id of the transaction just created.
    """
    tx = {
        'data': {
            'type': 'payment',
            'vendor_name': vendor_name,
            'amount': amount,
        }
    }
    return prepare_and_send(bdb, user, tx)



def get_transaction_by_id(bdb, txid):
    """ Returns data about a transaction from its id

    Returns: dict of form
        {
            'id': transaction_id,
            'donater_name OR vendor_name': name of the donater or the vendor depending on what type
                                           of transaction it is,
            'amount': amount of money associated with the transaction,
        }

    """
    return bdb.transactions.retrieve(txid)['asset']['data']
  
def add_transaction_to_collection(client, transaction_type, txid):
    """
    Add the transaction id to MongoDB

    Args: txid
    """
    if transaction_type == 'donate':
        collection = client.donate_transactions
    elif transaction_type == 'pay':
        collection = client.pay_transactions
    data =  {
        'id': txid
    }
    return collection.insert_one(data).inserted_id


def get_transactions(mongoclient, bdb, transaction_type):
    """
    Returns a list of all transactions of type passed
    """
    if transaction_type == 'donate':
        collection = mongoclient.donate_transactions
        name_field = 'donater_name'
    elif transaction_type == 'pay':
        collection = mongoclient.pay_transactions
        name_field = 'vendor_name'

    tx_list = []
    for tx in collection.find():
        chain_tx = bdb.transactions.retrieve(tx['id'])
        data = {
            'id': tx['id'],
            name_field: chain_tx['asset']['data'][name_field],
            'amount': chain_tx['asset']['data']['amount'],
        }
        tx_list.append(data)

    return tx_list

if __name__ == '__main__':
    bdb = BigchainDB(config.BLOCKCHAIN_URL)
    bdb_donate(bdb, generate_keypair(), 'param', '50')
    bdb_pay(bdb, generate_keypair(), 'test', '60')
