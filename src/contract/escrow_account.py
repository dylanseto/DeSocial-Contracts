import sys
from pyteal import *


def escrow_account(app_id):

    asset_close_to_check = Txn.asset_close_to() == Global.zero_address()
    rekey_check = Txn.rekey_to() == Global.zero_address()
    linked_with_app_call = And(
        Gtxn[0].type_enum() == TxnType.ApplicationCall,
        Gtxn[0].application_id() == Int(app_id)
    )
    fee_check = Txn.fee() <= Int(1000)

    # create asa from escrow
    on_create_asa = Gtxn[1].type_enum() == TxnType.AssetConfig

    # fund 1 asa that has been created by escrow
    on_fund_asa = Seq([
        Assert(Txn.type_enum() == TxnType.AssetTransfer),
        Assert(Txn.asset_sender() == Global.zero_address()),
        Assert(asset_close_to_check),
        Assert(Txn.asset_amount() == Int(1)),
        Int(1)
    ])

    on_fund_escrow = Seq([
                    Assert(Txn.type_enum() == TxnType.Payment)
    ])

    return Seq([
                Assert(rekey_check),
                Assert(linked_with_app_call),
                Assert(fee_check),
                Cond(
                [Gtxn[0].application_args[0] == Bytes("create_post"), on_create_asa],
                [Gtxn[0].application_args[0] == Bytes("get_post"), on_fund_asa])
            ])



arg = int(sys.argv[1])
print(compileTeal(escrow_account(arg), Mode.Signature, version=5))