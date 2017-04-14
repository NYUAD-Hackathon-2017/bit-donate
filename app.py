from flask import Flask
from flask import request, render_template, send_file, request
import config
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair


app = Flask(__name__)
blockchain_db = BigchainDB(config.BLOCKCHAIN_URL)

@app.route('/')
def index():
    return "Hello, world"

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    """
    Take a donater name and an amount and put a transaction into the blockchain
    """
    pass

@app.route('/pay', methods=['POST'])
def pay():
    """
    Take a vendor name and an amount and put that expenditure transaction into the blockchain
    """
    pass


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=3031,
    )
