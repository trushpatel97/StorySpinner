import numpy
import sys
import string
import os
from pickle import dump
from random import randint
from pickle import load
from numpy import array

# Updated imports for modern TensorFlow/Keras
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, LSTM, Embedding, BatchNormalization
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# TensorFlow compatibility settings
tf.compat.v1.disable_eager_execution()

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
        # predict probabilities for each word - UPDATED METHOD
        yhat = model.predict(encoded, verbose=0)
        yhat = tf.argmax(yhat, axis=-1).numpy()[0]
        # map predicted word index to word
        out_word = ''

        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
        in_text += ' ' + out_word
        result.append(out_word)

    return ' '.join(result)

def load_model_with_compatibility(model_path):
    """Load model with compatibility fixes for older TensorFlow versions"""
    try:
        # Try normal loading first
        model = load_model(model_path)
        return model
    except Exception as e:
        print(f"Normal model loading failed: {str(e)}")
        try:
            # Try loading with compile=False to avoid optimizer issues
            model = load_model(model_path, compile=False)
            return model
        except Exception as e2:
            print(f"Model loading with compile=False failed: {str(e2)}")
            # Return None to indicate failure
            return None

# function for loading documents from local files

def load_doc(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except UnicodeDecodeError:
        # Fallback to different encodings if UTF-8 fails
        try:
            with open(filename, 'r', encoding='latin1') as file:
                text = file.read()
            return text
        except:
            with open(filename, 'r', encoding='cp1252', errors='ignore') as file:
                text = file.read()
            return text

# save tokens to file, one dialog per line
def save_doc(lines, filename):
    data = '\n'.join(lines)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)

# we will be cleaning our dataset in order to obtain better word representations.

def gen_don(inputtext):
    
    try:
        # define the structure of word sequences we will be training on
        
        # organize into sequences of tokens
            
        cleaned_txt = load_doc("Trump_2016-11-06.txt_clean.txt")
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

            
        # load the saved model from file with compatibility fixes
        model = load_model_with_compatibility('don_model.h5')
        
        if model is None:
            return "Error: Could not load the model. The model may be incompatible with this version of TensorFlow."
        

        # load the tokenizer
        tokenizer = load(open('tokenizer.pkl', 'rb'))

        #load the clean text
        seq_length = len(lines[0].split()) - 1
            
        # select a seed text
        if (not inputtext):
            seed_text = lines[randint(0,len(lines))]
        else:
            seed_text = inputtext
        
        print(seed_text + '\n')

        # generate new text
        generated = generate_seq(model, tokenizer, seq_length, seed_text, 50)
        print(generated)

        return  seed_text + " " + generated
        
    except Exception as e:
        error_msg = f"Error in text generation: {str(e)}"
        print(error_msg)
        return error_msg

