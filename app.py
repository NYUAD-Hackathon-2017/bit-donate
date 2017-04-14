from flask import Flask
from flask import request, render_template, send_file, request
from utils import bdb_donate

app = Flask(__name__)
blockchain_db = BigchainDB(config.BLOCKCHAIN_URL)
user = generate_keypair()

@app.route('/')
def index():
    return "Hello, world"

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    """
    Take a donater name and an amount and put a transaction into the blockchain
    """
    if request.method == 'GET':
        return render_template('donate.html')
    elif request.method == 'POST':
        donater_name = request.form.get('donater_name')
        amount = request.form.get('amount')
        sent_txid = bdb_donate(blockchain_db, user, donater_name, amount)
        return "Transaction {} sent".format(sent_txid)


@app.route('/pay', methods=['GET', 'POST'])
def pay():
    """
    Take a vendor name and an amount and put that expenditure transaction into the blockchain
    """
    if request.method == 'GET':
        return render_template('pay.html')
    elif request.method == 'POST':
        vendor_name = request.form.get('vendor_name')
        amount = request.form.get('amount')
        sent_txid = bdb_pay(blockchain_db, user, vendor_name, amount)
        return "Transaction {} sent".format(sent_txid)


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=3031,
    )
