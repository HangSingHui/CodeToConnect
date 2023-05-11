import json

f = open("sample_events.json")

obj = json.load(f)

currency_states = {}

newest_currency_states = {}

#Create a new config event hash map
config_event = {}
#Key - eventID
#values is m,b,b divisorRatio, spread

#Create a new rate hash map based on event
rate_event = {}
#Key: eventID, Value: rate

trade_events = {}
#Key: eventID, Value: Currency object



tenor_dict={"1M": 30, "2M": 60, "3M": 90,"6M":180, "9M":270, "12M":360 }

class Currency():
    def __init__(self):
        self.rate = None
        self.ccy = None
        self.tenor = None
        self.quantity = None
        self.config = None #this links to a configEvent ID

for event in obj:
    # print(event)
    #Get event type
    
    #Get the id of the event
    id  = event["EventId"]

    # #Create a Currency object
    # id = Currency()

    name = event["EventType"]
    print(name)

    currency = event["Ccy"]

    #Create the key to store in the currency state

    # if name == "ConfigEvent":
    #     #Create a new configEvent element in configElement dictionary
    #     config_event[id] = event
    
    if name == "FXMidEvent":
        #Update the rate event list
        rate_event[id] = 
        
print(rate_event)

#Dont need to store the eventID, can just get the rate directly eg. anything after event 6 (supposing that rate changes at event 6) will have the rate till the next one



    # if event["EventType"] == "TradeEvent":
    #     #Extract Tenor and position
    #     id.tenor = tenor_dict[event["Tenor"]]
    #     id.quantity = event["Quantity"]


    # elif event["EventType"] == "FXMidEvent":
    #     #Extract rate
    #     #Extract ccy
    #     pass
    # else:
    #     #Extract m, b ,divsior, spread
    #     pass
    
    #Store in currency dictionary





