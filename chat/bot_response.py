import pickle
import os
module_dir = os.path.dirname(__file__)  # get current directory

model_folder_path = module_dir + os.path.normpath('/chatbot_tf')
training_file_path = model_folder_path+ os.path.normpath('/training_data')

print("current folder path is " + model_folder_path)
data = pickle.load( open( training_file_path, "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

# import our chat-bot intents file
import json

dataset_path = model_folder_path + os.path.normpath('/dataset/new-dataset.json')

with open(dataset_path) as json_data:
    dataset = json.load(json_data)


"""
Tflearn model
"""
import tflearn
import tensorflow as tf
import numpy as np
import h5py
import warnings
import random
import nltk

nltk.download('punkt')

"""
Choosing a stemmer 
"""

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

warnings.filterwarnings("ignore",category=FutureWarning)
# reset underlying graph data
tf.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')


# load our saved model

model_path = model_folder_path + os.path.normpath('/model.tflearn')
model.load(model_path)

"""
Creating bag of words from user input

"""

def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))


"""
contextualisation and response generation
"""    

# create a data structure to hold user context
context = {}

ERROR_THRESHOLD = 0.25
def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for key in dataset.keys():
                # find a tag matching the first result
                if dataset[key]['intent'] == results[0][0]:
                    # a random response from the intent
                    intent = dataset[key]['intent']
                    
                    # set context for this intent if necessary
                    if 'context_set' in dataset[key]:
                        if show_details: print ('context:', dataset[key]['context_set'])
                        context[userID] = dataset[key]['context_set']
                    
                    if 'webhook' in dataset[key]:
                        pass # request the webhook to activate
                        
                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in dataset[key] or \
                        (userID in context and 'context_filter' in intent and intent['context_filter'] == context[userID]):
                        if show_details: print ('Answer:', intent['Answer'])
                        # a random response from the intent
                        return random.choice(dataset[key]['response'])

    results.pop(0)    

