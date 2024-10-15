import threading
import time

import pandas as pd
from ibapi.client import EClient
from ibapi.common import TickerId
from ibapi.contract import Contract, ContractDetails
from ibapi.wrapper import EWrapper

from core.utils import override


class BaseClient(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self._contract_details_event = threading.Event()
        self.contract_details = []

        self._account_summary_event = threading.Event()
        self.req_id_counter = 1  # Initialize request ID counter
        self.order_id = None  # valid order id

    def next_request_id(self):
        reqId = self.req_id_counter
        self.req_id_counter += 1  # Increment for the next request
        return reqId

    def next_order_id(self):
        self.order_id += 1
        return self.order_id

    @override(EWrapper)
    def error(self, reqId: TickerId, errorCode: int, errorString: str, *args):
        """Override EWrapper error method."""
        super().error(reqId, errorCode, errorString)
        print(reqId)

    @override(EWrapper)
    def nextValidId(self, orderId: int):
        """Method of EWrapper.
        Sets the order_id class variable.
        This method is called from after connection completion, so
        provides an entry point into the class.
        """
        super().nextValidId(orderId)
        self.order_id = orderId

    @override(EWrapper)
    def accountSummary(
        self, reqId: int, account: str, tag: str, value: str, currency: str
    ):
        super().accountSummary(reqId, account, tag, value, currency)
        self.account_summaries.append({"account": account, "tag": tag, "value": value})

    @override(EWrapper)
    def accountSummaryEnd(self, reqId: int):
        super().accountSummaryEnd(reqId)
        self.cancelAccountSummary(reqId)
        self._account_summary_event.set()

    def get_account_summary(self):
        """Get the account summaary.

        Returns (pandas DataFrame): Dataframe of the account information.
        """
        self.account_summaries = []
        self.reqAccountSummary(9001, "All", "$LEDGER:USD")

        self._account_summary_event.wait()

        return pd.DataFrame.from_dict(self.account_summaries).set_index("account")

    def contractDetails(self, reqId: TickerId, contractDetails: ContractDetails):
        print(contractDetails)
        self.contract_details.append(contractDetails)

    def contractDetailsEnd(self, reqId: TickerId):
        print("Finished reciving contract details")
        self._contract_details_event.set()

    # get the details for a given contract
    @override(EClient)
    def reqContractDetails(self, **contract_details):
        self._contract_details_event.clear()
        contract = Contract()
        contract.symbol = contract_details["Symbol"]
        reqId = self.next_request_id()
        super().reqContractDetails(reqId, contract)
        self._contract_details_event.wait()
        return self.contract_details
