from pyteal import *


def createAccount():

    on_create_account = Seq(
        Assert(Txn.type_enum() == TxnType.ApplicationCall),
        Assert(Gtxn[1].on_completion() == OnComplete.OptIn),
        # Create Account
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields(
            {
            TxnField.type_enum: TxnType.AssetConfig,
            TxnField.config_asset_name: Bytes("asa_acc"),
            TxnField.config_asset_unit_name: Bytes("asa_acc"),
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
        App.localPut(Int(0), Bytes("acc_id"), InnerTxn.created_asset_id()),        
        Int(1),
    )

    # Delete Account
    # Note: The local state auto clear by the Close Out Operation.
    # See: https://developer.algorand.org/docs/clis/goal/app/closeout/
    on_delete_account = Seq(
        Assert(Txn.type_enum() == TxnType.ApplicationCall),
        Assert(Txn.on_completion() == OnComplete.CloseOut),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields(
            {
            TxnField.type_enum: TxnType.AssetConfig,
            TxnField.config_asset: App.localGet(Int(0), Bytes("acc_id"))
            }
        ),
        InnerTxnBuilder.Submit(), 
        Int(1),
    )

    program = Cond( 
        [Txn.application_id() == Int(0), Int(1)],  # On app creation
        [Txn.application_args[0] == Bytes("create_account"), on_create_account],
        [Txn.application_args[0] == Bytes("delete_account"), on_delete_account],
        #For Debugging Purpose
        [Txn.application_args[0] == Bytes("delete_app"), Int(1)]
    )
        
    return And(Txn.group_index() == Int(0), program)

if __name__ == "__main__":
    print(compileTeal(createAccount(), Mode.Application, version=5))