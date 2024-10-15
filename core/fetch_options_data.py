import time

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper


class OptionsData(EClient, EWrapper):
    """Fetches the option chains data for a Contract.

    Options Data class that opens a stream for a list option chains.

    Args:
        EClient (_type_): _description_
        EWrapper (_type_): _description_
    """

    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        """nextValidId

        Stores the first valid id returned on a new connection. This method is call implicitly on connect.

        Args:
            orderId (int): The next valid orderId.
        """
        self.orderId = orderId

    def nextId(self):
        self.orderId += 1
        return self.orderId

    def reqContractDetails(self, reqId: int, contract: Contract):
        return super().reqContractDetails(reqId, contract)
