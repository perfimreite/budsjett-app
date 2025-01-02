import os

source = "./empty_history.json"
target = "./history.json"

with open(source, 'rb') as src, open(target, 'wb') as trg:
    origin = src.read()
    trg.write(origin)
    print("INFO: file `history.json` has been reset. You have a clean history.")
