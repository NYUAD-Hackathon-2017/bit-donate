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

if __name__ == '__main__':
    bdb = BigchainDB(config.BLOCKCHAIN_URL)
    bdb_donate(bdb, generate_keypair(), 'param', '50')
    bdb_pay(bdb, generate_keypair(), 'test', '60')
