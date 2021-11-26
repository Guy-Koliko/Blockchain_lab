import datetime
import json

import requests
from flask import render_template, redirect, request

from app import app

CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"
posts = []

#this function gets the data from the node’s /chain endpoint, parses the data, and stores it locally.

def fetch_posts():
    
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    respons = requests.get(get_chain_address)
    if respons.status_code == 200:
        content = []
        chain = json.loads(respons.content)
        for block in chain['chain']:
            for tx in block['transactions']:
                tx['index'] = block['index']
                tx['hash']=block['previous_hash']
                content.append(tx)
            
        global posts
        posts = sorted(content,key=lambda k:k['timestamp'],reverse=True)
    
@app.route('/submit',methods=['POST'])
def submit_textarea():
    post_content = request.form["content"]
    author = request.form["author"]
    vote = request.form['vote']
    post_object = {
        'author': author,'content': post_content,'vote':vote
}
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)
    requests.post(new_tx_address,json=post_object,headers={'Content-type': 'application/json'})
    return redirect('/')

@app.route('/')
def home():
    return render_template('/index.html')
port = 8000

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=port)