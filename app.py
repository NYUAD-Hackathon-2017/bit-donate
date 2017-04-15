from flask import Flask, redirect
from flask import request, render_template, send_file, request
from utils import bdb_donate
import config
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from pymongo import MongoClient
from mongoUtil import *


app = Flask(__name__)
mongodb = MongoClient('52.66.27.92', 27017).bitdonate
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
        first=request.form.get('first')
        last=request.form.get('last')
        cc=request.form.get('cc')
        email=request.form.get('email')
        amount= request.form.get('amount')
        donater_name=first+last
        sent_txid = bdb_donate(blockchain_db, user, donater_name, amount)
        addDonation(mongodb,first,last,email,sent_txid)
        return redirect("/user_donations?id=34")


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

@app.route('/user_donations', methods=['GET'])
def userDonations():
    if request.args.get('id'):
        return "my page"
    return redirect("/")

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=3031,
    )
