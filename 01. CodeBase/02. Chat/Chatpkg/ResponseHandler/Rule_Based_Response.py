# Imoporting the required library
import numpy as np
import json


# Imoporting the required custom library
import utils
import TextProcessor



# reading data
data = utils.readData()

# reading intents
intents = data['intents']

# reading responses
responses = data['responses']

# reading response type
response_type = data['response_type']

# reading bag of word
bag_of_words = data['bag_of_words']


# reading Food Database
food_DB = utils.readFoodDB() # food_DB is a pandas datarframe

# column name
col_item_name = 'item name'
col_price = 'price'
col_menu = 'menu'

# reading Food BOW
food_BOW = utils.readFoodBOW()


# accessing local database
DataBase = utils.DataBase



def generate_random_response(intent):
    responseList = responses[intent]['responses']
    resLength = len(responseList)
    resIndex = np.random.randint(resLength)
    return responseList[resIndex]

def generate_random_extension(intent):
    responseList = responses[intent]['extensions']
    resLength = len(responseList)
    resIndex = np.random.randint(resLength)
    return responseList[resIndex]

def capitalize_first_letter(item_name):
    return ' '.join( list( map( lambda x: x[0].upper() + x[1:] if x[0].isalpha() else x , item_name.split() ) ) )




def Greetings_Handler(intent, CacheDB, customer_message):
    CacheDB_OTI = CacheDB['one_time_intents']

    if intent not in CacheDB_OTI:
        CacheDB_OTI.append(intent)
        reply = generate_random_response(intent)
    else:
        CacheDB_OTI.append('CourtesyGreetings')
        reply = generate_random_extension(intent)

    CacheDB['one_time_intents'] = CacheDB_OTI

    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }




def CourtesyGreetings_Handler(intent, CacheDB, customer_message):
    CacheDB_OTI = CacheDB['one_time_intents']

    reply = generate_random_response(intent)

    if intent not in CacheDB_OTI:
        CacheDB_OTI.append('CourtesyGreetings')
        reply = reply + ' ' + generate_random_extension(intent)
    
    CacheDB['one_time_intents'] = CacheDB_OTI
    
    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }




def CourtesyGreetingResponse_Handler(intent, CacheDB, customer_message):
    reply = generate_random_response(intent)

    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }




def NameQuery_Handler(intent, CacheDB, customer_message):
    reply = generate_random_response(intent)

    keyword = '<NAME>'
    agentName = DataBase['myName']

    reply = reply.replace(keyword, agentName)

    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }




def HumanNameQuery_Handler(intent, CacheDB, customer_message):
    customer_name = CacheDB['customer_info']['customer_name']

    if customer_name:
        reply = generate_random_response(intent)
        keyword = '<NAME>'
        reply = reply.replace(keyword, customer_name)
    else:
        reply = generate_random_extension(intent)

    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }




def CustomerName_Handler(intent, CacheDB, customer_message):
    msg = customer_message.lower().split()
        
    word_to_remove = ['name', 'call', 'is'] # this item can conflict NLTK noun tagging
    for x in word_to_remove:
        if x in msg:
            msg.remove(x)
    
    # looping to find the noun
    customer_name = list(filter(lambda x: TextProcessor.get_pos_tag(x)=='n', msg))[0]

    customer_name = customer_name[0].upper() + customer_name[1:] 

    CacheDB['customer_info']['customer_name'] = customer_name

    reply = generate_random_response(intent)
    keyword = '<NAME>'
    reply = reply.replace(keyword, customer_name)

    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }




def OrderSummery_Handler(intent, CacheDB, customer_message):
    reply = "Here is your order list.\n\n"

    # calculating the max length of items
    max_length = np.max( food_DB[col_item_name].apply(lambda x: len(x)) )

    total_length = 3 + max_length + 5  + 3   + 5   + 3   + 5    + 3   + 2      + 3   + 5    + 3   + 6         + 3   + 3
    #           intend   item   intend space price space intend space quantity space intend space total-price space intend

    order = CacheDB['food_order']
    
    line = f"|{'-'*(total_length-2)}|"
    new_line = '\n'

     # dotted line
    reply = reply + line + new_line

    if len(order['items']) == 0:
        msg = 'Your cart is empty.'
        left = int( np.floor((total_length-len(msg)) / 2) ) - 1
        right = int( np.ceil((total_length-len(msg)) / 2) ) - 1

        # menu title
        empty_msg = f"|{' '*left}" + f"{msg}" + f"{' '*right}|"
        reply = reply + empty_msg + new_line
        
        # dotted line
        reply = reply + line + new_line
    else: 
        msg = f"You have {len(order['items'])} item(s) in your cart"
        left = int( np.floor((total_length-len(msg)) / 2) ) - 1
        right = int( np.ceil((total_length-len(msg)) / 2) ) - 1

        # menu title
        count_msg = f"|{' '*left}" + f"{msg}" + f"{' '*right}|"
        reply = reply + count_msg + new_line
        
        # dotted line
        reply = reply + line + new_line

        for item in order['items']:
            i_item_name = capitalize_first_letter(item['name']) # item name
            i_item_price = f"{item['price']:5.2f}" # price
            i_item_quantity = f"{item['quantity']}" # quantity
            i_item_total_price = f"{(item['quantity']*item['price']):6.2f}" # price

            front = f"|{' '*2}"  # front space

            back = f"{' '*2}|{' '*2}"  # ending

            middle = f"{' '*(max_length - len( i_item_name) ) }" # middle space

            final_item = front + i_item_name + middle + back


            front = f"{' '*3}"  # front space

            back = f"{' '*5}|{' '*2}"  # ending

            middle = f"{' '*(5 - len( i_item_price) ) }" # middle space

            final_item = final_item + front + middle + i_item_price + back


            front = f"{' '*3}"  # front space

            back = f"{' '*5}|{' '*2}"  # ending

            middle = f"{' '*(2 - len( i_item_quantity) ) }" # middle space

            final_item = final_item + front + middle + i_item_quantity + back


            front = f"{' '*3}"  # front space

            back = f"{' '*5}|"  # ending

            middle = f"{' '*(5 - len( i_item_total_price) ) }" # middle space

            final_item = final_item + front + middle + i_item_total_price + back



            reply = reply + final_item + new_line

        # dotted line
        reply = reply + line + new_line

        # total price
        summery = f"Total bill : {order['total_price']:6.2f}"
        right = 5 - 1
        left = ( total_length-len(summery)-right ) - 2
        
        summery = f"|{' '*left}" + f"{summery}" + f"{' '*right}|"
        reply = reply + summery + new_line + line + new_line + new_line

    
    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }
        


def OfferQuery_Handler(intent, CacheDB, customer_message):
    
    reply = 'Sorry, no offers are available at this time.'

    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }




def MostSellingDishes_Handler(intent, CacheDB, customer_message):
    
    text = [
        'The following foods are some of the most often ordered:\n\n',
        'Persian Chicken Biryani\n',
        'Tandoori Mixed Grill\n',
        'King Prawn Butterfly\n',
        'Lamb Shashlick\n',
        'Tandoori Roti\n',
    ]

    reply = ''.join(text)

    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }




def SpecialDishes_Handler(intent, CacheDB, customer_message):
    
    text = [
        'Our specialties on the menu include:\n\n',
        'Butter Chicken\n',
        'Special Fried Rice\n',
        'King Prawn Butterfly\n',
        
    ]

    reply = ''.join(text)

    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }




def RecommendDishes_Handler(intent, CacheDB, customer_message):
    
    text = [
        'You can enjoy some of our specialty foods.:\n\n',
        'Butter Chicken\n',
        'Special Fried Rice\n',
        'King Prawn Butterfly\n',
        
    ]

    reply = ''.join(text)

    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }




#-----------------------------------------------------------------------|
#   Handler definition fpr RuleBased Response                           |
#-----------------------------------------------------------------------|
def RuleBased(intent, CacheDB, customer_message):

    #-----------------------------------------------------------------------|
    #   'Greetings'                                                         |
    #-----------------------------------------------------------------------|
    if intent == 'Greetings':
        return Greetings_Handler(intent, CacheDB, customer_message)
        



    #-----------------------------------------------------------------------|
    #   'CourtesyGreetings'                                                 |
    #-----------------------------------------------------------------------|
    elif intent == 'CourtesyGreetings':
        return CourtesyGreetings_Handler(intent, CacheDB, customer_message)
        



    #-----------------------------------------------------------------------|
    #   'CourtesyGreetingResponse'                                          |
    #-----------------------------------------------------------------------|
    elif intent == 'CourtesyGreetingResponse':
        return CourtesyGreetingResponse_Handler(intent, CacheDB, customer_message)
        
        


    #-----------------------------------------------------------------------|
    #   'NameQuery'                                                         |
    #-----------------------------------------------------------------------|
    elif intent == 'NameQuery':
        return NameQuery_Handler(intent, CacheDB, customer_message)
       



    #-----------------------------------------------------------------------|
    #   'HumanNameQuery'                                                    |
    #-----------------------------------------------------------------------|
    elif intent == 'HumanNameQuery':
        return HumanNameQuery_Handler(intent, CacheDB, customer_message)



    
    #-----------------------------------------------------------------------|
    #   'CustomerName'                                                      |
    #-----------------------------------------------------------------------|
    elif intent == 'CustomerName':
        return CustomerName_Handler(intent, CacheDB, customer_message)




    #-----------------------------------------------------------------------|
    #   'OrderSummery'                                                      |
    #-----------------------------------------------------------------------|
    elif intent == 'OrderSummery':
        return OrderSummery_Handler(intent, CacheDB, customer_message)




    #-----------------------------------------------------------------------|
    #   'OfferQuery'                                                        |
    #-----------------------------------------------------------------------|
    elif intent == 'OfferQuery':
        return OfferQuery_Handler(intent, CacheDB, customer_message)
    



    #-----------------------------------------------------------------------|
    #   'MostSellingDishes'                                                 |
    #-----------------------------------------------------------------------|
    elif intent == 'MostSellingDishes':
        return MostSellingDishes_Handler(intent, CacheDB, customer_message)    




    #-----------------------------------------------------------------------|
    #   'SpecialDishes'                                                     |
    #-----------------------------------------------------------------------|
    elif intent == 'SpecialDishes':
        return SpecialDishes_Handler(intent, CacheDB, customer_message)    




    #-----------------------------------------------------------------------|
    #   'RecommendDishes'                                                     |
    #-----------------------------------------------------------------------|
    elif intent == 'RecommendDishes':
        return RecommendDishes_Handler(intent, CacheDB, customer_message)  
    



    #------------------------------------------------------------------------------|
    #   'Clever', 'Gossip', 'GoodBye', 'Jokes', 'SelfAware', 'Swearing', 'Thanks'  |
    #------------------------------------------------------------------------------|
    elif intent in ['Clever', 'Gossip', 'GoodBye', 'Jokes', 'SelfAware', 'Swearing', 'Thanks']:
        reply = generate_random_response(intent)
    
    
        

    #-----------------------------------------------------------------------|
    #   ** Other                                                            |
    #-----------------------------------------------------------------------|    
    else:
        reply = f'{intent} <Need to update>'
    
    
    
    
    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }






