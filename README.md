# AlgoSocial-Contracts

## Requirements
- Pip3: https://pip.pypa.io/en/stable/getting-started/

## Project setup
1) Run the installPackages.bat:
```
installPackages.bat
```
2) Update algod_address, algod_token, header and m_mnemonic in algo_config.py to the appropriate network and your own wallet address. By default, it's set to use my own PureStake API account (https://purestake.io/) and wallet address.

See here for the different options: https://developer.algorand.org/docs/build-apps/setup/#how-do-i-obtain-an-algod-address-and-token
```
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "SxyeYnXjIi7sydMnmi85L8mqXypdroBv1ZdTcBmp"
headers = {
    "X-API-Key": algod_token,
}
m_mnemonic = "employ fly ahead odor finger olympic virtual suffer sugar fold hand shop latin fortune elephant valve timber notable oblige screen pioneer tiger snake abandon visit"
```
4) Run buildContracts.bat to compile and deploy the contracts on the Algorand network specified
buildContracts.bat
```
installPackages.bat
```
