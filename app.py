from flask import Flask, redirect
from flask import request, render_template, send_file, request
import config
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from mongoUtil import *
from utils import bdb_donate, bdb_pay, add_transaction_to_collection, get_transactions, get_transaction_by_id
from pymongo import MongoClient
import json
import sys
from random import *

app = Flask(__name__)
blockchain_db = BigchainDB(config.BLOCKCHAIN_URL)
client = MongoClient(config.MONGO_HOST, 27017).bitdonate
user = generate_keypair()

countries=['Algeria', 'Bahrain', 'Egypt', 'Iran', 'Iraq', 'Palestine', 'Jordan', 'Kuwait', 'Lebanon', 'Libya', 'Morocco', 'Oman', 'Qatar', 'Saudi Arabia', 'Syria', 'Tunisia', 'United Arab Emirates', 'Yemen', 'Ethiopia' , 'Sudan']
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
        country = countries[randrange(len(countries))]
        donater_name=first+"_"+last+"_"+email
        sent_txid = bdb_donate(blockchain_db, user, donater_name, amount)
        userId = addDonation(client,first,last,email,sent_txid,country)
        add_transaction_to_collection(client, 'donate', sent_txid)
        return redirect("/user_donations?id={}".format(userId))


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
        item = request.form.get('item')
        print(vendor_name)
        print(amount)
        sent_txid = bdb_pay(blockchain_db, user, vendor_name, amount, item)
        add_transaction_to_collection(client, 'pay', sent_txid)
        print("added transaction id to mongo")
        return redirect('/portal')



@app.route('/user_donations', methods=['GET'])
def userDonations():
    if request.args.get('id'):
        donations=getDonersAllDonations(client,request.args.get('id'))
        tids=list(map(lambda x: x['tid'],donations))
        transactoions=list(map(lambda x: get_transaction_by_id(blockchain_db,x), tids))
        amounts= list(map(lambda x: x['amount'],transactoions))
        amounts= list(map(lambda x: int(x),amounts))
        total=0
        for amount in amounts:
            total+=amount
        DonationsList=list()
        for i in range(len(amounts)):
            DonationsList.append({"amount": amounts[i],"timestamp":donations[i]['timestamp']})
        return "total: {} \n donations: \n you donated in {}".format(total,DonationsList)
    return redirect("/")


@app.route('/donate_transactions', methods=['GET'])
def donate_transactions():
    """
    Shows all the donations made to the charity
    """
    collection = client.donate_transactions
    tx_list = get_transactions(client, blockchain_db, 'donate')
    sum = 0
    for tx in tx_list:
        try:
            sum += int(tx['amount'])
        except Exception as e:
            pass
    return render_template(
        'donate_transactions.html',
        tx_list=get_transactions(client, blockchain_db, 'donate'),
        sum=sum,
    )


@app.route('/pay_transactions', methods=['GET'])
def pay_transactions():
    """
    Shows all the vendor payments made by the charity.
    """
    collection = client.pay_transactions
    tx_list = get_transactions(client, blockchain_db, 'pay')
    sum = 0
    for tx in tx_list:
        try:
            sum += int(tx['amount'])
            print("hello", file=sys.stderr)
        except Exception as e:
            print(str(e), file=sys.stderr)
            print("error", file=sys.stderr)
            pass
    return render_template(
        'pay_transactions.html',
        tx_list=get_transactions(client, blockchain_db, 'pay'),
        sum=sum,
    )
@app.route('/portal')
def portal():
    dtx_list = get_transactions(client, blockchain_db, 'donate')
    dsum = 0
    for tx in dtx_list:
        try:
            dsum += int(tx['amount'])
        except:
            pass
    ptx_list = get_transactions(client, blockchain_db, 'pay')
    psum=0
    for tx in ptx_list:
        try:
            psum += int(tx['amount'])
        except:
            pass
    return render_template(
        'bootstrap.html',
        dtx_list=dtx_list,
        ptx_list=ptx_list,
        dsum=dsum,
        psum=psum,
    )


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=3031,
    )
