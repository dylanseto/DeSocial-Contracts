import base64

from algosdk.v2client import algod
from algosdk import mnemonic, constants, util, encoding
from algosdk import account
from algosdk.future import transaction
from algosdk.error import AlgodHTTPError

import algo_config
import contract_config

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

    #Get Logic Address of the escrow account
    # programstr = 'AyAGBpSR7w3oBwQBAyYCC2NyZWF0ZV9wb3N0CGdldF9wb3N0MSAyAxJEMwAQIhIzABgjEhBEMQEkDkQ3ABoAKBJAACY3ABoAKRJAAAEAMRAlEkQxEzIDEkQxFTIDEkQxEiEEEkQhBEIABjMBECEFEg=='
    t = contract_config.escrowTealAddress.encode()
    program = base64.decodebytes(t) #hex encode string
    lsig = transaction.LogicSig(program)
    print("lsig Address: " + lsig.address())
    lAddress = lsig.address()
    lAddressDecoded = encoding.decode_address(lAddress)
    print("decoded: "+ str(lAddressDecoded))
    

    callAppTxn = transaction.ApplicationCallTxn(sender, params, contract_config.createPostAppID, on_complete, app_args=["set_escrow", lAddressDecoded])
    
    # print("tran: " + str(callAppTxn))

    signedTxn = callAppTxn.sign(private_key)
    algod_client.send_transaction(signedTxn)

    ## Fund The Escrow account
    '''
    fundEscrowTxn = transaction.PaymentTxn(
                                    sender,
                                    params,
                                    lAddress,
                                    util.algos_to_microalgos(10))
    signedEscrowFundTxn = fundEscrowTxn.sign(private_key)
    algod_client.send_transaction(signedEscrowFundTxn)
    '''

except AlgodHTTPError as err:
    print(err)
    print(err.code)