import numpy
import sys
import string
import os
from pickle import dump
from random import randint
from pickle import load
from numpy import array
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Embedding
from keras.layers import BatchNormalization
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from keras.utils import to_categorical
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


# sample program to load in a dataset (Trump_2016-11-06.txt)

'''
NOTE:

The below code is for an LSTM that uses Keras. 
Currently, training this model, using the above dataset described,
will take around 2.5 hours.
The commented-out portions are the portions of the code that involve training (for approximately 20 rounds, or epochs.)
To generate text, simply run by typing python3 lstm.py in the Linux terminal. 
As an additional feature, prestuplenie_i_nakazanie.txt is included in the LSTM folder. 
It just takes 20 hours to train on it. But that's Russian Lit for you.

'''


# here, we are loading in the ASCII text and making everything uniformly lowercase.

def generate_seq(model, tokenizer, seq_length, seed_text, n_words):
    result = list()
    in_text = seed_text
    # generate a fixed number of words
    for _ in range(n_words):
	# encode the text as integer
        encoded = tokenizer.texts_to_sequences([in_text])[0]
	# truncate sequences to a fixed length
        encoded = pad_sequences([encoded], maxlen=seq_length, truncating='pre')
        # predict probabilities for each word
        yhat = model.predict_classes(encoded, verbose=0)
        # map predicted word index to word
        out_word = ''

        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
        in_text += ' ' + out_word
        result.append(out_word)

    return ' '.join(result)


# function for loading documents from local files

def load_doc(filename):
    file = open(filename, 'r')
    # read all text
    text = file.read()
    # close the file
    file.close()
    
    return text

# save tokens to file, one dialog per line
def save_doc(lines, filename):
	data = '\n'.join(lines)
	file = open(filename, 'w')
	file.write(data)
	file.close()

# we will be cleaning our dataset in order to obtain better word representations.

def gen_yelp_review(inputtext):
    
    # define the structure of word sequences we will be training on
    
    # organize into sequences of tokens
        
    cleaned_txt = load_doc("yelp.txt_clean.txt")
    lines = cleaned_txt.split('\n')
    
    # Begin integer encoding
    
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(lines)
    sequences = tokenizer.texts_to_sequences(lines)
        
    # get vocabulary size for bookkeeping
    vocab_size = len(tokenizer.word_index) + 1

    
    # separate into input and output arrays: x and y, respectively
    sequences = array(sequences)
    X =  sequences[:,:-1]
    y = sequences[:,-1]
    y = to_categorical(y, num_classes=vocab_size)
    seq_length = X.shape[1]


    # save the tokenizer
    dump(tokenizer, open('tokenizer.pkl', 'wb'))

        
    # load the saved model from file
    model = load_model('yelp_model.h5')
    

    # load the tokenizer
    tokenizer = load(open('tokenizer.pkl', 'rb'))

    #load the clean text
    seq_length = len(lines[0].split()) - 1

    if (not inputtext):
        
        # select a seed text
        seed_text = lines[randint(0,len(lines))]

    else:
        seed_text = inputtext
        
    print(seed_text + '\n')
        
    # generate new text
    generated = generate_seq(model, tokenizer, seq_length, seed_text, 50)
    print(generated)
        
    return seed_text + " " + generated

