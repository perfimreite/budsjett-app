import os

def delete():
    source = "./empty_history.json"
    target = "./history.json"

    with open(source, 'rb') as src, open(target, 'wb') as trg:
        trg.write(src.read())
        print("INFO: file `history.json` has been reset. You have a clean history.")

delete()
