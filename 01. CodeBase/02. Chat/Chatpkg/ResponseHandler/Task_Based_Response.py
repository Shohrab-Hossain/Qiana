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

# number list
word2Num = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 
        'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16,'seventeen': 17, 'eighteen': 18,
        'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90, 'zero': 0
    }

num_list = [
        'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 
        'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen','seventeen', 'eighteen',
        'nineteen', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety', 'zero'
    ]



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

def suggest_item(item_bow):
    suggested_items = []

    required_num_of_suggestion = 6
    per_item = required_num_of_suggestion // len(item_bow)

    for word in item_bow:
        is_item_has_the_word = food_DB[col_item_name].apply(lambda x: word in x.lower().split())
        related_item = food_DB[ is_item_has_the_word ]

        
        number_of_item_to_pick = per_item if per_item <= len(related_item) else len(related_item)

        picked_item_name = related_item[:number_of_item_to_pick][col_item_name]

        suggested_items.extend( list(picked_item_name) )

    suggested_items.sort()

    return suggested_items


def capitalize_first_letter(item_name):
    return ' '.join( list( map( lambda x: x[0].upper() + x[1:] if x[0].isalpha() else x , item_name.split() ) ) )


def search_item(item_name):
    item = food_DB[food_DB[col_item_name] == item_name]

    if len(item): # item exists in the DB
        return  {
            'name' : capitalize_first_letter(item_name),
            'price': float( item[col_price] )
        }
    else: # item not found, so returning empty dict
        return {}
        



def PriceQuery_Handler(intent, CacheDB, customer_message):
    # spliting the customer message to list of words
    msg = customer_message.lower().split()
    
    # looping to find which words are in food-BOW
    item_bow = list( filter(lambda x: x in food_BOW, msg) )
    
    if( len(item_bow) ): # query contains valid item name

        # joining the words to get the full-name of the Item
        item_name = ' '.join(item_bow)
        
        # searching the database for the details of the item
        item = search_item(item_name)

        if( len(item) ): # item exists in the DB
            reply = f"The price of {item['name']} is {item['price']} pounds."
        else: # item not found
            reply = f"Sorry, we don't have that item. Here are the price of some of the related items:\n\n"

            for item_name in suggest_item(item_bow):
                item = search_item(item_name)
                if( len(item) ): # item exists in the DB
                    reply = reply + f"{item['name']}  ---  {item['price']:.2f} pounds.\n"
    
    else: # query does not contain any valid item name
        reply = f"Sorry, we don't have that item."


    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }



def FoodQuery_Handler(intent, CacheDB, customer_message):
    # spliting the customer message to list of words
    msg = customer_message.lower().split()
    
    # looping to find which words are in food-BOW
    item_bow = list( filter(lambda x: x in food_BOW, msg) )
    
    if( len(item_bow) ): # query contains valid item name

        # joining the words to get the full-name of the Item
        item_name = ' '.join(item_bow)
        
        # searching the database for the details of the item
        item = search_item(item_name)

        if( len(item) ): # item exists in the DB
            reply = f"{item['name']} is available."
        else: # item not found
            if len(item_name.split()) == 1: # asking for related item
                reply = f"Yes, here are some of the items you may like:\n\n"
            else: # asking for specific food
                reply = f"Pardon, we don't have that item. Here are some of the related items you may like:\n\n"

            for item_name in suggest_item(item_bow):
                item = search_item(item_name)
                if( len(item) ): # item exists in the DB
                    reply = reply + f"{item['name']}\n"
    
    else: # query does not contain any valid item name
        reply = f"Sorry, we don't have that item."


    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }




def MenuQuery_Handler(intent, CacheDB, customer_message):
    reply = "Here is the menu.\n\n"

    # calculating the max length of items
    max_length = np.max( food_DB[col_item_name].apply(lambda x: len(x)) )

    # accessign the menu list and sorting alphabetically to diosplay
    menu_list = food_DB[col_menu].unique()
    total_length = 3 + max_length + 4 + 5 + 9

    # sorting the menu
    menu_list.sort()

    line = f"|{'-'*(total_length-2)}|"
    new_line = '\n'

    for m in menu_list:
        # dotted line
        reply = reply + line + new_line

        left = int( np.floor((total_length-len(m)) / 2) ) - 1
        right = int( np.ceil((total_length-len(m)) / 2) ) - 1

        # menu title
        name_of_the_menu = f"|{' '*left}" + f"{m.upper()}" + f"{' '*right}|"
        reply = reply + name_of_the_menu + new_line
        
        # dotted line
        reply = reply + line + new_line

        item_names = food_DB[ food_DB[col_menu] == m ][col_item_name]
        item_names = list(item_names)
        item_names.sort()

        for i_item_name in item_names:
            item_price = float(food_DB[ food_DB[col_item_name] == i_item_name ][col_price] )

            front = f"|{' '*2}"  # front space

            i_name = capitalize_first_letter(i_item_name) # item name
            
            i_price = f"{item_price:3.2f}  Pounds" # price

            back = f"{' '*2}|"  # ending

            middle = f"{' '*(total_length - len( front + i_name + str(i_price) + back ) ) }" # middle space

            # item details
            final_item = front + i_name + middle + str(i_price) + back

            reply = reply + final_item + new_line
        
        # dotted line
        reply = reply + line + new_line + new_line




    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }



def TakeOrder_Handler(intent, CacheDB, customer_message):
    # order quantity
    quantity = 0

    # spliting the customer message to list of words
    msg = customer_message.lower().split()
    
    # looping to find which words are in food-BOW
    item_bow = list( filter(lambda x: x in food_BOW, msg) )
    
    if( len(item_bow) ): # query contains valid item name

        # joining the words to get the full-name of the Item
        item_name = ' '.join(item_bow)
        
        # searching the database for the details of the item
        item = search_item(item_name)

        if( len(item) ): # item exists in the DB
            # looping to find numbers from word
            qty_digit = list( filter(lambda x: x.isnumeric(), msg) )

            # looping to find numbers from word
            qty_word = list( filter(lambda x: x in num_list, msg) )

            if len(qty_digit) and len(qty_word):
                reply = f"Pardon, the quantity of food is not clear. Can not take the order. Could you please make sure the quanity with name?"
            elif not len(qty_digit) and not len(qty_word):
                reply = f"Pardon, the quantity of food is not provided. Could you please make sure the quanity with food name?"
            else:
                if len(qty_digit):
                    if len(qty_digit)==1:
                        quantity = int( qty_digit[0] )
                    else:
                        reply = f"Pardon, the quantity of food is not clear. Can not take the order. Could you please make sure the quanity with name?"
                elif len(qty_word):
                    for word in qty_word:
                        quantity = quantity + word2Num[word]


            if quantity:
                order = CacheDB['food_order']

                if item['name'] not in order['item_names']:
                    create_item = {
                        'name': item['name'],
                        'price': item['price'],
                        'quantity': quantity
                    }
                    order['items'].append(create_item)
                    order['item_names'].append(item['name'])

                else:
                    for i_item in order['items']:
                        if i_item['name'] == item['name']:
                            i_item['quantity'] = i_item['quantity'] + quantity

                order['total_price'] = order['total_price'] + item['price']*quantity
                CacheDB['food_order'] = order

                reply = f"{item['name']} added to the cart."

        else: # item not found
            reply = f"Pardon, we don't have that item."
    
    else: # query does not contain any valid item name
        reply = f"Sorry, we don't have that item."
    

    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }



def PlaceOrder_Handler(intent, CacheDB, customer_message):
    # calculating the max length of items
    max_length = np.max( food_DB[col_item_name].apply(lambda x: len(x)) )

    total_length = 3 + max_length + 5  + 3   + 5   + 3   + 5    + 3   + 2      + 3   + 5    + 3   + 6         + 3   + 3
    #           intend   item   intend space price space intend space quantity space intend space total-price space intend

    order = CacheDB['food_order']
    
    line = f"|{'-'*(total_length-2)}|"
    new_line = '\n'

    if len(order['items']) == 0:
        reply = "Sorry, you have not ordered any item. Select some foods to place the order."
    else:
        reply = "Your order has been confirmed. Here is the summary of your order.\n\n"

        msg = f"You have ordered {len(order['items'])} item(s)"
        left = int( np.floor((total_length-len(msg)) / 2) ) - 1
        right = int( np.ceil((total_length-len(msg)) / 2) ) - 1

        # dotted line
        reply = reply + line + new_line
        
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




#-----------------------------------------------------------------------|
#   Handler definition fpr TaskBased Response                           |
#-----------------------------------------------------------------------|
def TaskBased(intent, CacheDB, customer_message):

    #-----------------------------------------------------------------------|
    #   'PriceQuery'                                                        |
    #-----------------------------------------------------------------------|
    if intent == 'PriceQuery':
        return PriceQuery_Handler(intent, CacheDB, customer_message)

    

    #-----------------------------------------------------------------------|
    #   'FoodQuery'                                                         |
    #-----------------------------------------------------------------------|
    elif intent == 'FoodQuery':
        return FoodQuery_Handler(intent, CacheDB, customer_message)



    #-----------------------------------------------------------------------|
    #   'MenuQuery'                                                         |
    #-----------------------------------------------------------------------|
    elif intent == 'MenuQuery':
        return MenuQuery_Handler(intent, CacheDB, customer_message)



    #-----------------------------------------------------------------------|
    #   'TakeOrder'                                                         |
    #-----------------------------------------------------------------------|
    elif intent == 'TakeOrder':
        return TakeOrder_Handler(intent, CacheDB, customer_message)

    

    #-----------------------------------------------------------------------|
    #   'PlaceOrder'                                                         |
    #-----------------------------------------------------------------------|
    elif intent == 'PlaceOrder':
        return PlaceOrder_Handler(intent, CacheDB, customer_message)




    #-----------------------------------------------------------------------|
    #   ** Other                                                            |
    #-----------------------------------------------------------------------|
    else:
        reply = f'{intent} <Need to update>'




    return {
        "reply" : reply, 
        "CacheDB" : CacheDB
    }



