from typing import Literal

import beaker as bk
from pyteal import (
    Expr,
    Global,
    InnerTxnBuilder,
    Int,
    Seq,
    Txn,
    TxnField,
    TxnType,
    abi,
)

app = bk.Application("EventTicket")


@app.external
def create_asset(
    assetName: abi.String,
    assetUrl: abi.String,
    assetTotal: abi.Uint64,
    managerAddress: abi.Address,
    metadataHash: abi.StaticBytes[Literal[32]],
) -> Expr:
    return Seq(  # Seq is used to group a set of operations with only the last returning a value on the stack
        # Start to build the transaction builder
        InnerTxnBuilder.Begin(),
        # This method accepts a dictionary of TxnField to value so all fields may be set
        InnerTxnBuilder.SetFields(
            {
                TxnField.type_enum: TxnType.AssetConfig,
                TxnField.config_asset_name: assetName.get(),
                TxnField.config_asset_url: assetUrl.get(),
                TxnField.config_asset_manager: managerAddress.get(),
                TxnField.config_asset_clawback: Global.current_application_address(),
                TxnField.config_asset_reserve: Global.current_application_address(),
                TxnField.config_asset_freeze: Global.current_application_address(),
                TxnField.config_asset_total: assetTotal.get(),
                TxnField.config_asset_metadata_hash: metadataHash.get(),
                TxnField.config_asset_decimals: Int(0),
            }
        ),
        # Submit the transaction we just built
        InnerTxnBuilder.Submit(),
    )


@app.external
def get_asset(asset: abi.Asset) -> Expr:
    return Seq(  # Seq is used to group a set of operations with only the last returning a value on the stack
        # Start to build the transaction builder
        InnerTxnBuilder.Begin(),
        # This method accepts a dictionary of TxnField to value so all fields may be set
        InnerTxnBuilder.SetFields(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: asset.asset_id(),
                TxnField.asset_amount: Int(1),
                TxnField.asset_receiver: Txn.sender(),
                TxnField.asset_sender: Global.current_application_address(),
            }
        ),
        # Submit the transaction we just built
        InnerTxnBuilder.Submit(),
    )


if __name__ == "__main__":
    spec = app.build()
    spec.export("artifacts")
