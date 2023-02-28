# -----------------------------------------------
#                   MODULE                      |
# -----------------------------------------------
#                                               |
# This module uses NLTK to process text and     |
#   creates function for more functionality     |
#                                               |
# -----------------------------------------------


# Initializing NLTK
import nltk

# downloading the required nltk files
nltk.download('punkt')
# nltk.download("stopwords")
nltk.download('averaged_perceptron_tagger')
# nltk.download('tagsets')
nltk.download('wordnet')
nltk.download('omw-1.4')

# -----------------------------------------------
#                 Tokenization                  |
# -----------------------------------------------
def _tokenize(words):
    from nltk.tokenize import word_tokenize
    _word_token = word_tokenize(words)

    return _word_token



# -----------------------------------------------
#                 Lemmatizing                   |
# -----------------------------------------------
def get_wordnet_pos(word):
    '''
    Map POS tag to first character lemmatize() accepts
    '''
    
    from nltk.corpus import wordnet
    tag = nltk.pos_tag([word])[0][1][0].lower()
    
    tag_dict = {"a": wordnet.ADJ,
                "n": wordnet.NOUN,
                "v": wordnet.VERB,
                "r": wordnet.ADV}
    
    return tag_dict.get(tag, wordnet.NOUN)


def _lemmatize(words):
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()

    _lemma_word = []

    for word in words:
        pos = get_wordnet_pos(word)
        lemma = lemmatizer.lemmatize(word=word, pos=pos)
        _lemma_word.append(lemma.lower())

    return _lemma_word



# -----------------------------------------------
#                   POS tag                     |
# -----------------------------------------------
def get_pos_tag(word):
    '''
    Map POS tag to first character 
        "a": ADJ,
        "n": NOUN,
        "v": VERB,
        "r": ADV
    '''
    
    tag = nltk.pos_tag([word])[0][1][0].lower()
    
    return tag