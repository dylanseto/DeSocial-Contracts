# compile teal code
import base64
import subprocess

from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import account
from algosdk.future import transaction
from algosdk.error import AlgodHTTPError

import algo_config

# Helper function that waits for a given txid to be confirmed by the network
def wait_for_confirmation(client, txid):
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation...")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo
    
def create_app(client, private_key, 
               approval_program, clear_program, 
               global_schema, local_schema): 
    print("Creating new app")

    # Define sender as creator
    sender = account.address_from_private_key(private_key)

    # Declare on_complete as NoOp
    on_complete = transaction.OnComplete.NoOpOC.real

    # Get node suggested parameters
    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = 1000

    # Create unsigned transaction
    txn = transaction.ApplicationCreateTxn(
        sender, params, on_complete, \
        approval_program, clear_program, \
        global_schema, local_schema)

    # Sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # Send transaction
    algod_client.send_transactions([signed_txn])

    # Await confirmation
    wait_for_confirmation(algod_client, tx_id)

    # Display results
    transaction_response = algod_client.pending_transaction_info(tx_id)
    app_id = transaction_response['application-index']
    print("Created new app-id: ", app_id)

    return app_id
        
try:
    # create an algod client
    algod_client = algod.AlgodClient(algo_config.algod_token, algo_config.algod_address, algo_config.headers);
  
    # compile createPost
    createPost_teal = "../contracts/build/createPost.teal"
    createPost_teal_data = open(createPost_teal, 'r').read()
    create_post_response = algod_client.compile(createPost_teal_data, headers={'X-API-Key': 'SxyeYnXjIi7sydMnmi85L8mqXypdroBv1ZdTcBmp', 'content-type': 'application/x-binary'})
    
    createPost_address = create_post_response["hash"]
    createPost_program = base64.b64decode(create_post_response['result'])
    
    # compile clearProgram
    clear_teal = "../contracts/build/clearProgram.teal"
    clear_teal_data = open(clear_teal, 'r').read()
    clear_response = algod_client.compile(clear_teal_data, headers={'X-API-Key': 'SxyeYnXjIi7sydMnmi85L8mqXypdroBv1ZdTcBmp', 'content-type': 'application/x-binary'})
    
    clear_address = clear_response["hash"]
    clear_program = base64.b64decode(create_post_response['result'])
    
    
    # get account from mnemonic
    private_key = mnemonic.to_private_key(algo_config.m_mnemonic)
    sender = account.address_from_private_key(private_key)
    # print("Sender: " + sender)
    
    # get node suggested parameters
    params = algod_client.suggested_params()
    
    # Declare on_complete as NoOp
    on_complete = transaction.OnComplete.NoOpOC
    
    # Declare application state storage (immutable)
    local_ints = 0
    local_bytes = 1
    global_ints = 0
    global_bytes = 1
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)
    
    createPostId = create_app(algod_client, private_key, createPost_program, clear_program, global_schema, local_schema)
    
    # compile pyteal for the escrow account   
    cmd = "python ./src/contract/escrow_account.py " + str(createPostId) + " >> ./build/escrow_account.teal"
    subprocess.call(cmd, shell=false)
    
    # compile escrow
    escrow_teal = "../contracts/build/escrow_account.teal"
    escrow_teal_data = open(escrow_teal, 'r').read()
    escrow_response = algod_client.compile(escrow_teal_data, headers={'X-API-Key': 'SxyeYnXjIi7sydMnmi85L8mqXypdroBv1ZdTcBmp', 'content-type': 'application/x-binary'})
    
    escrowStr = escrow_response['result']
    
    #Note: Uses CRLF line breaking to conform with ESLint
    f = open("../contracts/lib/contracts_post_config.js", "a")
    f.write("export const escrowTealAddress = '" + escrowStr + "'")
    f.write("\nexport const createPostTealAddress = '" + createPost_address + "'")
    f.write("\nexport const createPostAppID = " + str(createPostId))
    f.write("\n"); # EOL +1 Extra Line
    f.close()

    f = open("../contracts/src/contract_config.py", "a")
    f.write("escrowTealAddress = '" + escrowStr + "'")
    f.write("\ncreatePostAppID = " + str(createPostId))
    f.write("\n"); # EOL +1 Extra Line
    f.close()

except AlgodHTTPError as err:
    print(err)
    print(err.code)