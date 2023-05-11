import json

f = open("sample_events.json")

obj = json.load(f)

currency_states = {}

newest_currency_states = {}

#Create a new config event hash map
config_details = {}
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
        self.quantity = 0
        self.m = None
        self.b = None
        self.divisorRatio = None
        self.spread = None

    # after every event > calculation of ask and bid (save as a method)

    # one dataset for all the current rates (temp data storage) - store the latest rate per currency 
    # key as currency, tenor > will be considered as the latest value for your calc (position tied to currency and tenor≥)

for event in obj:
    # read event 
    # edit the dataset based on the type of event - currency, rate, m, b, divisorratio, spread
    # calc bid and ask for all contracts based on the global dataset 
    # add to list - {'eventid': []}


    #Check events
    eventName = event["EventType"]
    if eventName == "TradeEvent":
        key = event["Ccy"] + "-" + event["Tenor"]

        if key not in currency_states:
            #Create new currency class
            temp_class = Currency()
        
        else:
            #Retrieve the class
            temp_class = currency_states[key]

        #update quantites in the respective ccy and tenor

        action = event["BuySell"]
        #Update quantity based on buy and sell
        #Get quantity
        qty = event["Quantity"]
        if action == "buy":
            #Means plus
            temp_class.quantity += qty
        else:
            temp_class.quantity -= qty
    

    elif eventName == "ConfigEvent":
        id = event["EventId"]
        #Store in global config details list
        config_details[id] = event
    
    #Eventname == FXMidEvent
    else:
        #Update the rate of all contracts with a particular currency
        rate = event["rate"]
        currency = event["Ccy"]
        for key in currency_states:
            if currency == key.split("-")[0]:
                #Then update the rate of the currency
                currency_states[key].rate = rate
        


print(config_details)







