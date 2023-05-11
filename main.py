import json

f = open("sample_events.json")

obj = json.load(f)

currency_states = {}

trade_events = {}
#Key: eventID, Value: Currency object

date_dict={"1M": 30, "2M": 60, "3M": 90,"6M":180, "9M":270, "12M":360 }

class Currency():
    def __init__(self):
        self.rate = None
        self.ccy = None
        self.m = None
        self.b = None
        self.DivisorRatio = None
        self.spread = None
        self.tenor = None
        self.quantity = None

    # after every event > calculation of ask and bid (save as a method)

    # one dataset for all the current rates (temp data storage) - store the latest rate per currency 
    # key as currency, tenor > will be considered as the latest value for your calc (position tied to currency and tenor≥)

for event in obj:
    # read event 
    # edit the dataset based on the type of event 
    # calc bid and ask for all contracts based on the global dataset 
    # add to list - {'eventid': []}

    ######################
    #Get event type
    id  = event["EventId"]
    id = Currency()
    if event["EventType"] == "TradeEvent":
        #Extract Tenor and position
        id.tenor = date_dict[event["Tenor"]]
        id.position = event["Quantity"]
    elif event["EventType"] == "FXMidEvent":
        #Extract rate
        id.rate = event["Ccy"]
        #Extract ccy
        id.ccy = event["rate"]
        
        pass
    else:
        #Extract m, b ,divsior, spread
        pass
    
    #Store in currency dictionary
    currency_states[id] = id









changes = {}





