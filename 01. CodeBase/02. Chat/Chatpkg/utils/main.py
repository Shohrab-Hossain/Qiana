# -----------------------------------------------
#                  Package                      |
# -----------------------------------------------
#                                               |
#   This module has the utilities               |
#                                               |
# -----------------------------------------------


# importing required library
import numpy as np
import pandas as pd
import json
import pickle



# -----------------------------------------------
#        Check the OS is Colab or not           |
# -----------------------------------------------
import sys
is_running_on_colab = 'google.colab' in sys.modules




# -----------------------------------------------
#               Root Directory                  |
# -----------------------------------------------
# this directory will be used as Root Directory to read/write any file
if is_running_on_colab:
    rootDir = '/content/drive/MyDrive/_ML/Qiana/03. Generated Data/'    # for google-colab
else:
    rootDir = './mlData/'   # for application



# -----------------------------------------------
#                   Read Data                   |
# -----------------------------------------------
def readData():
    # defining file name
    fileName = 'data.json'
    filePath = rootDir + fileName

    # reading the data
    with open(filePath,'r') as f: 
        data = json.load(f)

    return data




# -----------------------------------------------
#               Read Food Database              |
# -----------------------------------------------
def readFoodDB():
    # defining file name
    fileName = 'Food_DB.csv'
    filePath = rootDir + fileName

    # reading the CSV dataset
    df = pd.read_csv(filePath)

    return df




# -----------------------------------------------
#                  Read Food BOW                |
# -----------------------------------------------
def readFoodBOW():
    # defining file name
    fileName = 'Food_BOW.json'
    filePath = rootDir + fileName

    # reading the data
    with open(filePath,'r') as f: 
        food_BOW = json.load(f)

    return food_BOW['Food_BOW']




# -----------------------------------------------
#                   Read Model                  |
# -----------------------------------------------
def readModel():
    # defining the name of the model
    modelName = 'Qiana.h5'

    # creating the path
    path = rootDir + modelName

    # reading the model
    # loading saved models
    from keras.models import load_model
    model = load_model(path)
    # model = pickle.load(open(path, 'rb'))
    
    return model




# -----------------------------------------------
#              Generate Data Matrix             |
# -----------------------------------------------
def generate_data_matrix(customer_message):
    # Imoporting the required custom library
    from Chatpkg import TextProcessor

    # generating data matrix
    data_matrix = TextProcessor.generate_data_matrix(customer_message)

    # returning the generated dat_matrix
    return data_matrix




# -----------------------------------------------
#    Filter Customer message                    |
# -----------------------------------------------
def filter_message(customer_message):
    # reading Food BOW
    food_BOW = readFoodBOW()

    # spliting the customer message to list of words
    msg = customer_message.lower().split()
    
    # looping to find which words are in food-BOW
    item_bow = list( map(lambda x: 'FOODITEM' if x in food_BOW else x, msg) )

    # joinng the words back to get the message
    customer_message = ' '.join(item_bow)
    
    return customer_message




# -----------------------------------------------
#    Prediction - using locally stored model    |
# -----------------------------------------------
def local_prediction(data_matrix):
    # loading model
    model = readModel()

    # predicting on data-matrix using trained ML model
    predictions = model.predict(data_matrix, verbose=0)
    
    # returning the predictions
    return predictions




# -----------------------------------------------
#    Prediction - using api model               |
# -----------------------------------------------
def api_prediction(data_matrix):
    # predicting on data-matrix using trained ML model
    predictions = 'Add Api before prediciton'
    
    # returning the predictions
    return predictions



# -----------------------------------------------
#    Prediction                                 |
# -----------------------------------------------
def get_prediction(customer_message):
    # filtering the message for better prediction
    customer_message = filter_message(customer_message)

    # generating data matrix from the customer message
    data_matrix = generate_data_matrix(customer_message)

    # predicting on data-matrix using trained ML model
    if is_running_on_colab:
        predictions = local_prediction(data_matrix) # prediction by local model
    else:
        predictions = api_prediction(data_matrix)   # prediction by api model
    

    # checking the prediction maximum accuracy
    max_prediction = np.max(predictions, axis=1)
    if max_prediction < 0.6:
        return 'not_sure'

    # extracting the index of class with maximum prediction percentage
    predicted_intent_index = int( np.argmax(predictions, axis=1) )


    # reading data
    data = readData()

    # reading intents
    intents = data['intents']

    # extracting the name of predicted intent
    predicted_intent = intents[predicted_intent_index]
    

    # returning the prediction
    return predicted_intent





# -----------------------------------------------
#                Defining Database              |
# -----------------------------------------------
DataBase = {
    "myName" : 'Qiana',
    "restaurent_info" : {},
    "food_offer" : 'Show food offer. [update DataBase]',
    "special_dishes" : 'Show special dishes. [update DataBase]',
}



# -----------------------------------------------
#             Defining Cache Database           |
# -----------------------------------------------
CacheDB = {
    "one_time_intents" : [],
    "customer_info" : {
        'customer_name': ''
    },
    "food_order" : {
        'items': [],
        'item_names': [],
        'total_price': 0

    }
}


