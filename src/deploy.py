# compile teal code
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk.error import AlgodHTTPError

algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "YOUR API KEY"
headers = {
   "X-API-Key": algod_token,
}

algod_client = algod.AlgodClient(algod_token, algod_address, headers);

try:
    # create an algod client
    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = "SxyeYnXjIi7sydMnmi85L8mqXypdroBv1ZdTcBmp"
    headers = {
        "X-API-Key": algod_token,
    }

    algod_client = algod.AlgodClient(algod_token, algod_address, headers);

    # compile escrow
    myprogram = "../contracts/build/escrow_account.teal"
    # read teal program
    data = open(myprogram, 'r').read()
    # compile teal program
    response = algod_client.compile(data, headers={'X-API-Key': 'SxyeYnXjIi7sydMnmi85L8mqXypdroBv1ZdTcBmp', 'content-type': 'application/x-binary'})
    print("Hash: " + response["hash"])
    print("Result: " + response["result"])
except AlgodHTTPError as err:
    print(err)
    print(err.code)
