# -----------------------------------------------
#                  Package                      |
# -----------------------------------------------
#                                               |
#   This package takes a sentence as input      |
#         and generates data-matrix.            |
#                                               |
#   This package uses local module 'nltkFunc'   |
#   to process text and generate Data-Matrix    |
#   which will be used for prediction           |
#   by the ML Model.                            |
#                                               |
# -----------------------------------------------


# Imoporting the required library
import json

# Imoporting the required custom library
import nltkFunc 
import utils


# reading data
data = utils.readData()

# reading bag of word
bag_of_words = data['bag_of_words']



# Data Matrix Generator
def matrix_generator(words):
  mat_row = [0 for _ in range(0, len(bag_of_words))]

  for word in words:
    if word in bag_of_words:
      word_index = bag_of_words.index(word)
      count = bag_of_words.count(word)
      mat_row[word_index] = count
  
  # reshaping the data
  mat_row = [mat_row]

  return mat_row



def generate_data_matrix(customer_message):
    # tokenizing
    tokenized_words = nltkFunc._tokenize(customer_message)

    # lemmatizing
    lemmatized_words = nltkFunc._lemmatize(tokenized_words)

    # generating matrix
    data_matrix = matrix_generator(lemmatized_words)

    # returning the generated data matrix
    return data_matrix
