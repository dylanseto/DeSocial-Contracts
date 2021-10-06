from pyteal import *


def createAccount():
    # set escrow address
    on_set_escrow = Seq([
        Assert(Txn.sender() == Global.creator_address()),
        App.globalPut(Bytes('escrow'), Txn.application_args[1]),
        Int(1)
    ])

    on_create_account = Seq([
                    Assert(Global.group_size() == Int(2)), # Check that this is a group transaction.
                    Assert(Gtxn[1].sender() == App.globalGet(Bytes('escrow'))), # Check that the sender is the escrow account.
                    Assert(Gtxn[1].type_enum() == TxnType.AssetConfig),
                    Assert(Eq(Gtxn[1].config_asset_name(), Bytes("asa_account"))), # Check Asset name.
                    Assert(Gtxn[1].config_asset_total() == Int(1)), # That supply == 1 (NFT)
                    Assert(Txn.config_asset_decimals() == Int(0)), # Decimal == 0 (NFT)
                    #TODO: Check for malformation of IPFS CID
                    Int(1)
    ])

    on_get_account =  Seq([
                    Assert(Global.group_size() == Int(2)),
                    Assert(Gtxn[1].sender() == App.globalGet(Bytes('escrow'))),
                    Assert(Gtxn[1].type_enum() == TxnType.AssetTransfer),
                    Int(1)
    ])

    # The post must be frozen so that users cannot transfer it elsewhere
    on_freeze_post = Seq([
                    Assert(Global.group_size() == Int(3)),
                    Assert(Gtxn[2].type_enum() == TxnType.AssetFreeze),
                    Int(1)
    ])
    
    program = Cond( 
        [Txn.application_id() == Int(0), Int(1)],  # On app creation
        [Txn.application_args[0] == Bytes("set_escrow"), on_set_escrow],
        [Txn.application_args[0] == Bytes("create_account"), on_create_account],
        [Txn.application_args[0] == Bytes("get_account"), on_get_account]
        #[Txn.application_args[0] == Bytes("freeze_post"), on_freeze_post]
    )
        
    return And(Txn.group_index() == Int(0), program)

if __name__ == "__main__":
    print(compileTeal(createAccount(), Mode.Application, version=3))