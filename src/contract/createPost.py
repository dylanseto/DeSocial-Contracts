from pyteal import *


def createPost():
    # set escrow address
    on_set_escrow = Seq([
        Assert(Txn.sender() == Global.creator_address()),
        App.globalPut(Bytes('escrow'), Txn.application_args[1]),
        Int(1)
    ])

    on_create_post = Seq([
                    Assert(Global.group_size() == Int(2)), # Check that this is a group transaction.
                    Assert(Gtxn[1].sender() == App.globalGet(Bytes('escrow'))), # Check that the sender is the escrow account.
                    Assert(Gtxn[1].type_enum() == TxnType.AssetConfig),
                    Assert(Eq(Gtxn[1].config_asset_name(), Bytes("asa_post"))), # Check Asset name.
                    Assert(Gtxn[1].config_asset_default_frozen() == Int(1)), # Check frozen
                    Assert(Gtxn[1].config_asset_total() == Int(1)), # That supply == 1 (NFT)
                    Assert(Len(Gtxn[1].config_asset_metadata_hash()) > Int(0)), # Metadata is not empty
                    Int(1)
    ])
    
    program = Cond( 
        # On app creation
        [Txn.application_id() == Int(0), Int(1)],
        [Txn.application_args[0] == Bytes("set_escrow"), on_set_escrow],
        [Txn.application_args[0] == Bytes("create_post"), on_create_post]
        )
        
    return And(Txn.group_index() == Int(0), program)

if __name__ == "__main__":
    print(compileTeal(createPost(), Mode.Application, version=3))