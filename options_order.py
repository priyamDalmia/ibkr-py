import threading
import time

from ibapi.client import *
from ibapi.common import TickerId
from ibapi.contract import Contract, ContractDetails
from ibapi.wrapper import *


class TradeApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        self.orderId = orderId

    def nextId(self):
        self.orderId += 1
        return self.orderId

    def currentTime(self, currtime: int):
        print(currtime)

    def error(
        self, reqId: int, errorCode: int, errorString: str, advancedOrderRejectJson=""
    ):
        print(f"{reqId} - {errorCode}: {errorString}")

    def accountSummary(
        self, reqId: int, account: str, tag: str, value: str, currency: str
    ):
        print(
            "AccountSummary. ReqId:",
            reqId,
            "Account:",
            account,
            "Tag: ",
            tag,
            "Value:",
            value,
            "Currency:",
            currency,
        )

    def accountSummaryEnd(self, reqId: int):
        print("AccountSummaryEnd. ReqId:", reqId)

    def contractDetails(self, reqId: TickerId, contractDetails: ContractDetails):
        print(f"{reqId} - {contractDetails}")

    def contractDetailsEnd(self, reqId: TickerId):
        print(f"{reqId} - All details fetched!")

    def openOrder(
        self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState
    ):
        print(
            f"openOrder: {orderId}, contract: {contract}, order: {order}, Maintenance Margin: {orderState.maintMarginChange}"
        )

    def orderStatus(
        self,
        orderId: OrderId,
        status: str,
        filled: float,
        remaining: float,
        avgFillPrice: float,
        permId: int,
        parentId: int,
        lastFillPrice: float,
        clientId: int,
        whyHeld: str,
        mktCapPrice: float,
    ):
        print(
            f"orderStatus. orderId: {orderId}, status:  {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}"
        )

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(
            f"execDetails. reqId: {reqId}, contract: {contract}, execution:  {execution}"
        )


app = TradeApp()
app.connect("127.0.0.1", 7497, clientId=0)
threading.Thread(target=app.run).start()
print("Waiting 5 second to finish initialization...")
time.sleep(5)

# defining a contract
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"  # stocks, OPT for options, FUT for futures
contract.currency = "USD"
contract.exchange = "SMART"

app.reqContractDetails(app.nextId(), contract=contract)

# building an options order
# symbol = "GOOG"
# secType = "OPT"
# exchange = "BOX"
# currency = "USD"
# lastTradeDateOronth = "20190315"
# strike = 1180
# right = "C"
# multiplier = "100"
myorder = Order()
myorder.orderId = app.nextId()
myorder.action = "BUY"
myorder.orderType = "MKT"
myorder.totalQuantity = 10

# place an order


# ideally give five minutes to receive any remaining messages
print("Tasks completed, waiting 5 second before disconnection...")
time.sleep(5)
app.disconnect()
