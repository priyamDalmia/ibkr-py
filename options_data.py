from ib_async import *
from omegaconf import OmegaConf

config = OmegaConf.load("config.yaml")
ib = IB()
ib.connect("127.0.0.1", 7497, clientId=13)

contract_details = config.contracts[0]
contract = Stock(symbol=contract_details.symbol, exchange=contract_details.exchange)
quals = ib.qualifyContracts(contract)
if not len(quals) > 0:
    raise Exception("Invalid contract")
print(f"Contract: {contract}")

# set market data type to delayed data
ib.reqMarketDataType(4)
# for contract in [contract]:
#     ib.reqMktData(contract, "", False, False)

# reqTickers; internally calls reqMarketData to subscribe to data streams
[ticker] = ib.reqTickers(contract)

print(f"Ticker: {ticker.contract.symbol} MarketPrice {ticker.marketPrice()}")


# def updateTick(tickers):
#     print(f"Updating {len(tickers)} tickers...")
#     for t in tickers:
#         print(f"{t.contract.symbol}, Last: {t.last}")


# ib.pendingTickersEvent += updateTick
# ib.sleep(100)
# ib.pendingTickersEvent -= updateTick
# print(ib.tickers())

# fetch a list of valid option chains given contracts, and security types
chains = ib.reqSecDefOptParams(contract.symbol, "", contract.secType, contract.conId)
chains_df = util.df(chains)
print(chains_df[["exchange", "tradingClass"]])

# options will be like any other contract; build the contract
# and request tickers thereafter.
option_chain = next(c for c in chains if c.tradingClass == contract.symbol)
market_value = ticker.marketPrice()
last_price = ticker.last
strikes = [
    strike
    for strike in option_chain.strikes
    if strike % 5 == 0 and market_value - 20 < strike < market_value + 20
]
# latest expiration
expirations = sorted(exp for exp in option_chain.expirations)[0:2]
rights = ["P", "C"]
options = [
    Option(
        contract.symbol,
        exp,
        strike=strike,
        right=rights[1],
        exchange="ASX",
        tradingClass=contract.symbol,
    )
    for exp in expirations
    for strike in strikes
]
options = ib.qualifyContracts(*options)
print(f"Found {len(options)} matching Options contracts!")


# get the market data for all these options;
# if MarketDataType == 4, frozen data will be returned.
# tickers = ib.reqTickers(*options)
# print(util.df(tickers))
# print(chains_df.loc[["exchange", "tradingClass"]])
# place a dummy order for the first option on the list
option = options[0]
order = LimitOrder("BUY", 10, last_price - 1, transmit=False)
ib.placeOrder(option, order)

order_2 = LimitOrder("BUY", 10, last_price - 10, transmit=True)
ib.placeOrder(option, order_2)
ib.sleep(5)

trades = ib.openTrades()
breakpoint()
print("Waiting for 5 seconds before disconnecting...")
ib.sleep(5)
ib.disconnect()
