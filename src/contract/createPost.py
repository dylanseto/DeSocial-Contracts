from pyteal import *


def createPost():
    # set escrow address
    on_set_escrow = Seq([
        Assert(Txn.sender() == Global.creator_address()),
        App.globalPut(Bytes('escrow'), Txn.application_args[1]),
        Int(1)
    ])
    
    program = Cond( 
        # On app creation
        [Txn.application_id() == Int(0), Int(1)],
        [Txn.application_args[0] == Bytes("set_escrow"), on_set_escrow]
        )
        
    return And(Txn.group_index() == Int(0), program)

if __name__ == "__main__":
    print(compileTeal(createPost(), Mode.Application, version=3))