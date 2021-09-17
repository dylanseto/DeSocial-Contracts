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

try:
    # create an algod client
    algod_client = algod.AlgodClient(algo_config.algod_token, algo_config.algod_address, algo_config.headers);

    # get account from mnemonic
    private_key = mnemonic.to_private_key(algo_config.m_mnemonic)
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = algod_client.suggested_params()
    
    # Declare on_complete as NoOp
    on_complete = transaction.OnComplete.NoOpOC

    callAppTxn = transaction.ApplicationCallTxn(sender, params, 27149634, on_complete, app_args=["set_escrow", "ZHMY4GKYNL4IC3P4EONUNRNBE6RZRPDFEB3VYAIQNFRFDFDTLAOLO2APFM"])
    
    signedTxn = callAppTxn.sign(private_key)
    algod_client.send_transaction(signedTxn)
except AlgodHTTPError as err:
    print(err)
    print(err.code)