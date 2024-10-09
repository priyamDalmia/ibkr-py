import threading
import time

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.wrapper import EWrapper


class TradeApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.contract_details = []  # To store multiple contracts
        self.contract_selected = None  # To store the selected contract

    # Callback for contract details
    def contractDetails(self, reqId, contractDetails):
        print(
            f"Received Contract: {contractDetails.contract.symbol} on {contractDetails.contract.exchange}"
        )
        self.contract_details.append(contractDetails.contract)

    # When all contract details have been received
    def contractDetailsEnd(self, reqId):
        print(f"End of contract details for reqId: {reqId}")
        # Assuming you want the first contract for simplicity, you can add more logic here to filter
        if len(self.contract_details) > 0:
            self.contract_selected = self.contract_details[
                0
            ]  # Select the first contract
        self.contract_details_received.set()  # Signal that contract details are done

    # Override for nextValidId to set orderId
    def nextValidId(self, orderId):
        self.nextOrderId = orderId

    # Override for order execution error
    def error(self, reqId, errorCode, errorString):
        print(
            f"Error. ReqId: {reqId}, ErrorCode: {errorCode}, ErrorString: {errorString}"
        )

    def placeOrder(self, orderId, contract, order):
        if contract:
            super().placeOrder(orderId, contract, order)
        else:
            print("Contract not selected yet!")


app = TradeApp()

# Connect to IB
app.connect("127.0.0.1", 7497, 0)
threading.Thread(target=app.run).start()

# Wait for the connection to be established
time.sleep(1)

# Request contract details
contract = Contract()
contract.symbol = "AAPL"
contract.secType = "STK"
contract.currency = "USD"
contract.exchange = "SMART"

# Create an event to wait for the contract details to be received
app.contract_details_received = threading.Event()
app.reqContractDetails(1001, contract)

# Wait for contract details to be received
app.contract_details_received.wait()  # Block until contract details are done

# If contract is selected, proceed to place an order
if app.contract_selected:
    # Create an order
    order = Order()
    order.action = "BUY"
    order.orderType = "MKT"
    order.totalQuantity = 10

    # Place the order using the selected contract
    app.placeOrder(app.nextOrderId, app.contract_selected, order)

# Keep the app running to process any responses
time.sleep(5)
