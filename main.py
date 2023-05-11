import json
import time 

f = open("sample_events.json")

obj = json.load(f)

currency_states = {}

newest_currency_states = {}

#Create a new config event hash map
config_details = {}
#Key - eventID
#values is m,b,b divisorRatio, spread

trade_events = {}


tenor_dict={"1M": 30, "2M": 60, "3M": 90,"6M":180, "9M":270, "12M":360 }

class Currency():
    def __init__(self):
        self.rate = None
        self.tenor = None
        self.ccy = None
        self.quantity = 0
        self.bid = None
        self.ask = None
        self.quoteStatus = None
    
    
    def __str__(self):
        #Just to check
        return f"{self.rate} . {self.ccy} . {self.quantity} . {self.bid} . {self.ask} . {self.quoteStatus}"

    # after every event > calculation of ask and bid (save as a method)

    # one dataset for all the current rates (temp data storage) - store the latest rate per currency 
    # key as currency, tenor > will be considered as the latest value for your calc (position tied to currency and tenor≥)


def calculate_bid_ask(rate, m, tenor, b, net_position, skew_ratio_divisor, spread):
    # Calculating variables
    variance = m * tenor_dict[tenor] + b
    skew = net_position / skew_ratio_divisor * variance
    new_mid = rate - skew
    bid = new_mid - (0.5 * spread / 10000)
    ask = new_mid + (0.5 * spread / 10000)

    # Returning results as a tuple
    return bid, ask

def determine_QuoteStatus(bid, ask, quantity, tenor, rate):
    if bid == "NA" or ask == "NA" or quantity == None or tenor == None:
        return "EXCEPTION"
    elif bid > ask or bid > rate * 1.10 or bid < rate * 0.9 or ask > rate * 1.10 or ask < rate * 0.9:
        return 'NON-TRADABLE'
    else:
        return "TRADABLE"

def print_dashboard(events,eventName):
    # Print the dashboard header
    print("---------------- Dashboard ----------------")
    print("EventId:" + str(num))
    print("Event Type: "+ eventName)
    print("|{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|".format("Ccy - Tenor", "Position", "Ask", "Bid","QuoteStatus"))
    print("-----------------------------------------------------------------------------------------------------------")

   
    
    # Print each event's information
    for event in events:
        event_id = num
        event_type = eventName
        # for quote in event['quotes']:
        ccy_tenor = event
        position = events[event].quantity
        ask = events[event].ask
        bid = events[event].bid
        quote_status = events[event].quoteStatus
        print("{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|".format(ccy_tenor, position, ask, bid,quote_status))
        # print("{:^15}|{:^15}|{:^15}|".format("", "", ask, bid, ""))
    print("-----------------------------------------------------------------------------------------------------------")


num = 1
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
            currency_states[key] = temp_class
        
        else:
            #Retrieve the class
            temp_class = currency_states[key]

        
        #update quantites in the respective ccy and tenor

        temp_class.tenor = event["Tenor"]
        action = event["BuySell"]
        #Update quantity based on buy and sell
        #Get quantity

        qty = event["Quantity"]
        if action == "buy":
            #Means plus
            temp_class.quantity += qty
        else:
            temp_class.quantity -= qty
        
        latest_key = list(config_details)[-1]
        m, b, divisorRatio, spread = config_details[latest_key]["m"],config_details[latest_key]["b"],config_details[latest_key]["DivisorRatio"],config_details[latest_key]["Spread"]

        if temp_class.rate != None:
            #Recalcaute for this one object
            bid, ask = calculate_bid_ask(temp_class.rate,m,temp_class.tenor, b, temp_class.quantity, divisorRatio,spread )
        else:
            bid, ask = "NA", "NA"

        temp_class.bid, temp_class.ask = bid, ask

        state = determine_QuoteStatus(temp_class.bid,temp_class.ask, temp_class.quantity, temp_class.tenor,temp_class.rate)
                
        temp_class.quoteStatus = state

        
        #Attach the key to the class

        #Get the last config details and do calculations for all bid and ask

        #use temp_class values

    

    elif eventName == "ConfigEvent":
        id = event["EventId"]
        #Store in global config details list
        config_details[id] = event

        #Get the last config details and do calculations for all bid and ask
        latest_key = list(config_details)[-1]
        m, b, divisorRatio, spread = config_details[latest_key]["m"],config_details[latest_key]["b"],config_details[latest_key]["DivisorRatio"],config_details[latest_key]["Spread"]
        
       
        
        #reculculate for everything
        for key in currency_states:
            if currency_states[key].rate != None:
                #Recalcaute for this one object
                bid, ask = calculate_bid_ask(currency_states[key].rate,m,currency_states[key].tenor, b, currency_states[key].quantity, divisorRatio,spread )
            else:
                bid, ask = "NA", "NA"

            currency_states[key].bid, currency_states[key].ask = bid, ask
            state = determine_QuoteStatus(currency_states[key].bid,currency_states[key].ask, currency_states[key].quantity, currency_states[key].tenor,currency_states[key].rate)
                
            currency_states[key].quoteStatus = state
        

    #Eventname == FXMidEvent
    elif eventName== "FXMidEvent":
        #Update the rate of all contracts with a particular currency
        rate = event["rate"]
        currency = event["Ccy"]
        latest_key = list(config_details)[-1]
        m, b, divisorRatio, spread = config_details[latest_key]["m"],config_details[latest_key]["b"],config_details[latest_key]["DivisorRatio"],config_details[latest_key]["Spread"]

        for key in currency_states:
            # print(key)
            if currency == key.split("-")[0]:
                #Then update the rate of the currency
                currency_states[key].rate = rate
                currency_states[key].ccy = currency

                if currency_states[key].rate != None:
                    #Recalcaute for this one object
                    bid, ask = calculate_bid_ask(currency_states[key].rate,m,currency_states[key].tenor, b, currency_states[key].quantity, divisorRatio,spread )
                else:
                    bid, ask = "NA", "NA"
                currency_states[key].bid, currency_states[key].ask = bid, ask

                #Update quote status
                state = determine_QuoteStatus(currency_states[key].bid,currency_states[key].ask, currency_states[key].quantity, currency_states[key].tenor,currency_states[key].rate)
                
                currency_states[key].quoteStatus = state


                        # 
        # Recalculate bid and ask for all the same currency at ccy
    
    print_dashboard(currency_states, eventName)

    num +=1
    

        

    #Dashboard



############ REAL- TIME #############


f1 = open("sample_input.json")
obj1 = json.load(f1)

with open('output.json', 'w') as put_in:
    for record in obj1:
        print(record)
        input_currency = record["Ccy"]
        input_tenor = record["Tenor"]
        input_eventid = record["EventId"]
        
        key = input_currency + "-" + input_tenor 
        # print(key)

        if key in currency_states.keys():
            position = currency_states[key].quantity
            bid = currency_states[key].bid
            ask = currency_states[key].ask
            quoteStatus = currency_states[key].quoteStatus


        # Read the specific values for particular contract at event
        output = {
            "EventId": input_eventid,
            "Ccy": input_currency,
            "Tenor": input_tenor,
            # change the below variable names to match
            "Position": position,
            "Bid": bid,
            "Ask": ask,
            "QuoteStatus": quoteStatus
        }   
        json_string = json.dumps(output, indent = 4)
        put_in.write(json_string)




# for currency in currency_states:
#     # time.sleep(5)
#     print(currency, currency_states[currency])


# #Dashboard






