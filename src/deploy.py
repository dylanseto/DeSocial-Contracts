# compile teal code
import base64

from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import account
from algosdk.future import transaction
from algosdk.error import AlgodHTTPError

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
    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = "SxyeYnXjIi7sydMnmi85L8mqXypdroBv1ZdTcBmp"
    headers = {
        "X-API-Key": algod_token,
    }

    algod_client = algod.AlgodClient(algod_token, algod_address, headers);

    # compile escrow
    escrow_teal = "../contracts/build/escrow_account.teal"
    escrow_teal_data = open(escrow_teal, 'r').read()
    escrow_response = algod_client.compile(escrow_teal_data, headers={'X-API-Key': 'SxyeYnXjIi7sydMnmi85L8mqXypdroBv1ZdTcBmp', 'content-type': 'application/x-binary'})
    
    escrow_teal_address = escrow_response["hash"]
    
    # compile createPost
    createPost_teal = "../contracts/build/createPost.teal"
    createPost_teal_data = open(createPost_teal, 'r').read()
    create_post_response = algod_client.compile(createPost_teal_data, headers={'X-API-Key': 'SxyeYnXjIi7sydMnmi85L8mqXypdroBv1ZdTcBmp', 'content-type': 'application/x-binary'})
    
    createPost_address = create_post_response["hash"]
    createPost_program = base64.b64decode(create_post_response['result'])
    
    # compile clearProgram
    clear_teal = "../contracts/build/clearProgram.teal"
    clear_teal_data = open(createPost_teal, 'r').read()
    clear_response = algod_client.compile(clear_teal_data, headers={'X-API-Key': 'SxyeYnXjIi7sydMnmi85L8mqXypdroBv1ZdTcBmp', 'content-type': 'application/x-binary'})
    
    clear_address = clear_response["hash"]
    clear_program = base64.b64decode(create_post_response['result'])
    
    f = open("../contracts/lib/contracts.js", "a")
    f.write('export const escrow_teal_address = "' + escrow_teal_address + '"')
    f.write('\nexport const createPost_teal_address = "' + createPost_address + '"')
    f.close()
    
    # get account from mnemonic
    private_key = mnemonic.to_private_key("horse slow toward twelve win kiwi delay keen steak survey second syrup sponsor stumble favorite below physical indoor nominee area team desert current abstract weather")
    sender = account.address_from_private_key(private_key)
    print("Sender: " + sender)
    
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
    
    create_app(algod_client, private_key, createPost_program, clear_program, global_schema, local_schema)

except AlgodHTTPError as err:
    print(err)
    print(err.code)