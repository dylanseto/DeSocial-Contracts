from pyteal import *


def createPost():
    # set escrow address
    on_set_escrow = Seq([
        Assert(Txn.sender() == Global.creator_address()),
        App.globalPut(Bytes('escrow'), Txn.application_args[1]),
        Int(1)
    ])

    on_create_post = Seq([
                    Assert(Global.group_size() == Int(3)), # Check that this is a group transaction.
                    Assert(Gtxn[0].receiver() == App.globalGet(Bytes('escrow'))), # Check that the receiver is the escrow account.
                    Assert(Gtxn[0].type_enum() == TxnType.AssetConfig),
                    Assert(Eq(Gtxn[0].config_asset_name(), Bytes("asa_post"))), # Check Asset name.
                    #Assert(Gtxn[0].config_asset_default_frozen() == Int(1)), # Check frozen
                    Assert(Gtxn[0].freeze_asset_account() == App.globalGet(Bytes('escrow'))), # Freeze account
                    Assert(Gtxn[0].config_asset_total() == Int(1)), # That supply == 1 (NFT)
                    Assert(Len(Gtxn[0].config_asset_metadata_hash()) > Int(0)), # Metadata is not empty
                    #TODO: Check for malformation of IPFS CID
                    Int(1)
    ])

    on_get_post =  Seq([
                    Assert(Global.group_size() == Int(3)),
                    Assert(Gtxn[1].sender() == App.globalGet(Bytes('escrow'))),
                    Assert(Gtxn[1].type_enum() == TxnType.AssetTransfer),
                    Int(1)
    ])

    # The post must be frozen so that users cannot transfer it elsewhere
    on_freeze_post = Seq([
                    Assert(Global.group_size() == Int(3)),
                    Assert(Gtxn[2].type_enum() == TxnType.AssetFreeze)
    ])
    
    program = Cond( 
        # On app creation
        [Txn.application_id() == Int(0), Int(1)],
        [Txn.application_args[0] == Bytes("set_escrow"), on_set_escrow],
        [Txn.application_args[0] == Bytes("create_post"), on_create_post],
        [Txn.application_args[0] == Bytes("get_post"), on_get_post],
        [Txn.application_args[0] == Bytes("freeze_post"), on_freeze_post]
    )
        
    return And(Txn.group_index() == Int(0), program)

if __name__ == "__main__":
    print(compileTeal(createPost(), Mode.Application, version=3))