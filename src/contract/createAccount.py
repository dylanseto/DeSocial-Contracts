from pyteal import *


def createAccount():
    # set escrow address
    on_set_escrow = Seq([
        Assert(Txn.sender() == Global.creator_address()),
        App.globalPut(Bytes('escrow'), Txn.application_args[1]),
        Int(1)
    ])

    on_create_account = Seq(
        Assert(App.localGet(Int(0), Bytes("signed_up")) == Int(0)),
        #Assert(Neq(Txn.application_args[1],Bytes(''))),
        # Create Account
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields(
            {
            TxnField.type_enum: TxnType.AssetConfig,
            TxnField.config_asset_name: Bytes("asa_account"),
            TxnField.config_asset_unit_name: Bytes("asa_account"),
            TxnField.config_asset_total: Int(1),
            TxnField.config_asset_decimals: Int(0),
            TxnField.config_asset_url: Txn.application_args[1],
            TxnField.config_asset_manager: Global.current_application_address(),
            TxnField.config_asset_reserve: Global.current_application_address(),
            TxnField.config_asset_freeze: Global.current_application_address(),
            TxnField.config_asset_clawback: Global.current_application_address(),
            }
        ),
        InnerTxnBuilder.Submit(),

        # Send Account NFT to user.
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: InnerTxn.created_asset_id(),
                TxnField.receiver: Global.current_application_address(),
                TxnField.amount: Int(1),

            }
        ),
        InnerTxnBuilder.Submit(),
        App.localPut(Int(0), Bytes("signed_up"), Int(1)),
        Int(1)
    )

    program = Cond( 
        [Txn.application_id() == Int(0), Int(1)],  # On app creation
        [Txn.application_args[0] == Bytes("create_account"), on_create_account]
    )
        
    return And(Txn.group_index() == Int(0), program)

if __name__ == "__main__":
    print(compileTeal(createAccount(), Mode.Application, version=5))