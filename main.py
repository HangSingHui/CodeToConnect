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

for event in obj:
    #Get event type
    id  = event["EventId"]
    id = Currency()
    if event["EventType"] == "TradeEvent":
        #Extract Tenor and position
        id.tenor = date_dict[event["Tenor"]]
        id.position = event["Quantity"]
    elif event["EventType"] == "FXMidEvent":
        #Extract rate
        #Extract ccy
        pass
    else:
        #Extract m, b ,divsior, spread
        pass
    
    #Store in currency dictionary
    currency_states[id] = id









changes = {}





