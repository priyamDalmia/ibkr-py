import sys
import threading
import time
import traceback

import pandas as pd
from omegaconf import OmegaConf

from core.base_client import BaseClient

# read the config
config = OmegaConf.load("config.yaml")

# connect to the client
try:
    client = BaseClient()
    client.connect("127.0.0.1", 7497, clientId=1)
    print("Connection Successful!")
except Exception as e:
    traceback.print_exc()
    print(f"Could not connect to the client.")
    client.disconnect()

# start a Ewrapper thread in the background
threading.Thread(target=client.run).start()
print("Waiting 2 seconds to finish initialization...")
time.sleep(5)

# build a contract from config
for contract_details in config.contracts:
    contract = client.reqContractDetails(**contract_details)

print("Job completed")
client.disconnect()
