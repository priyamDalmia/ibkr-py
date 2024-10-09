import threading
import time

from ibapi.client import *
from ibapi.common import TickerId
from ibapi.contract import Contract
from ibapi.wrapper import *


class TradeApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        self.orderId = orderId

    def nextId(self):
        self.orderId += 1
        return self.orderId

    def currentTime(self, time: int):
        print(time)

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


app = TradeApp()
app.connect("127.0.0.1", 7497, clientId=1)
threading.Thread(target=app.run).start()
time.sleep(1)


for i in range(5):
    time.sleep(1)
    app.reqAccountSummary(9001, "All", "NetLiquidation")

app.disconnect()
