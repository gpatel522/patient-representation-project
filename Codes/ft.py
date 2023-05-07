#!/usr/bin/env python
import gensim
import numpy as np

np.random.seed(1337)

import sys

sys.path.append('../../Neural/Lib/')
sys.dont_write_bytecode = True
import ConfigParser, os
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split
import keras as k
from keras.utils.np_utils import to_categorical
from keras.optimizers import RMSprop
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers import GlobalAveragePooling1D
from keras.layers.embeddings import Embedding
from keras.models import load_model
import dataset
from gensim.models import Word2Vec
#import word2vec


# ignore sklearn warnings
def warn(*args, **kwargs):
    pass


import warnings

warnings.warn = warn

RESULTS_FILE = '../data/MimicIII/Results/Model/results.txt'
MODEL_FILE = '../data/MimicIII/Results/Model/model.h5'


def print_config(cfg):
    """Print configuration settings"""

    print 'train:', cfg.get('data', 'train')
    if cfg.has_option('data', 'embed'):
        print 'embeddings:', cfg.get('data', 'embed')
    print 'test_size', cfg.getfloat('args', 'test_size')
    print 'batch:', cfg.get('dan', 'batch')
    print 'epochs:', cfg.get('dan', 'epochs')
    print 'embdims:', cfg.get('dan', 'embdims')
    print 'hidden:', cfg.get('dan', 'hidden')
    print 'learnrt:', cfg.get('dan', 'learnrt')


def get_model(cfg, init_vectors, num_of_features):
    """Model definition"""

    model = Sequential()
    model.add(Embedding(input_dim=num_of_features,
                        output_dim=cfg.getint('dan', 'embdims'),
                        input_length=maxlen,
                        trainable=True,
                        #weights=init_vectors,
                        embeddings_initializer="uniform",
                        name='EL'))
    model.add(GlobalAveragePooling1D(name='AL'))

    model.add(Dense(cfg.getint('dan', 'hidden'), name='HL'))
    model.add(Activation('relu'))

    model.add(Dense(classes))
    model.add(Activation('sigmoid'))

    return model


if __name__ == "__main__":

    os.environ['DATA_ROOT'] = '../data/'

    cfg = ConfigParser.ConfigParser()
    cfg.read(sys.argv[1])
    print_config(cfg)

    base = os.environ['DATA_ROOT']
    train_dir = os.path.join(base, cfg.get('data', 'train')) # CUI codes
    code_file = os.path.join(base, cfg.get('data', 'codes')) # files for CPT, Diagnoses, Procedure events

    print('train_dir:', train_dir) #'/Users/gpatel/Library/CloudStorage/Dropbox/Coursera/DL_in_Health/data/MimicIII/Patients/Cuis/'
    print('code_file:', code_file) #'/Users/gpatel/Library/CloudStorage/Dropbox/Coursera/DL_in_Health/data/MimicIII/Source/'

    dataset = dataset.DatasetProvider(
        train_dir,
        code_file,
        cfg.getint('args', 'min_token_freq'),
        cfg.getint('args', 'max_tokens_in_file'),
        cfg.getint('args', 'min_examples_per_code'))
    x, y = dataset.load()
    #print('x:', x)
    #print('y:', y)
    train_x, test_x, train_y, test_y = train_test_split(
        x,
        y,
        test_size=cfg.getfloat('args', 'test_size'))
    #print('train_x:', train_x)
    #print('test_x:', test_x)
    #print('train_y:', train_y)
    #print('test_y:', test_y)
    maxlen = max([len(seq) for seq in train_x])

    init_vectors = None
    if cfg.has_option('data', 'embed'):
        embed_file = os.path.join(base, cfg.get('data', 'embed'))
        #w2v = word2vec.Model(embed_file)
        lines = []
        with open(embed_file) as fin:
            for line in fin:
                lines.append(line.strip())
                # print(line.strip())
            # print(lines)
        v = [s.encode('utf-8').split() for s in lines]
        w2v = gensim.models.Word2Vec(v, min_count=1)
        vocab = list(w2v.wv.vocab)
        #print('vocab:', vocab)
        print 'number of features:', len(dataset.token2int)
        print 'features:', type(dataset.token2int), dataset.token2int
        # max_no_cuis = len(vocab)
        # embedding_matrix = np.zeros((max_no_cuis, cfg.getint('dan', 'embdims')))
        # for word, i in word_index.items():
        #     if i < max_no_cuis:
        #         embedding_vector = embeddings_index.get(word)
        #         if embedding_vector is not None:
        #             embedding_matrix[i] = embedding_vector
        #init_vectors = [w2v.select_vectors(dataset.token2int)]

    # turn x into numpy array among other things
    classes = len(dataset.code2int)
    train_x = pad_sequences(train_x, maxlen=maxlen)
    test_x = pad_sequences(test_x, maxlen=maxlen)
    train_y = np.array(train_y)
    test_y = np.array(test_y)

    print 'train_x shape:', train_x.shape
    print 'train_y shape:', train_y.shape
    print 'test_x shape:', test_x.shape
    print 'test_y shape:', test_y.shape
    print 'number of features:', len(dataset.token2int)
    print 'number of labels:', len(dataset.code2int)

    model = get_model(cfg, init_vectors, len(dataset.token2int))
    optimizer = RMSprop(lr=cfg.getfloat('dan', 'learnrt'))
    model.compile(loss='binary_crossentropy',
                  optimizer=optimizer,
                  metrics=['accuracy'])
    model.fit(train_x,
              train_y,
              epochs=cfg.getint('dan', 'epochs'),
              batch_size=cfg.getint('dan', 'batch'),
              validation_split=0.0)

    model.save(MODEL_FILE)

    # do we need to evaluate?
    if cfg.getfloat('args', 'test_size') == 0:
        exit()

    # probability for each class; (test size, num of classes)
    distribution = model.predict(test_x, batch_size=cfg.getint('cnn', 'batch'))

    # turn into an indicator matrix
    distribution[distribution < 0.5] = 0
    distribution[distribution >= 0.5] = 1

    f1 = f1_score(test_y, distribution, average='macro')
    precision = precision_score(test_y, distribution, average='macro')
    recall = recall_score(test_y, distribution, average='macro')
    print 'macro average p =', precision
    print 'macro average r =', recall
    print 'macro average f1 =', f1

    outf1 = open(RESULTS_FILE, 'w')
    int2code = dict((value, key) for key, value in dataset.code2int.items())
    f1_scores = f1_score(test_y, distribution, average=None)
    outf1.write("%s|%s\n" % ('macro', f1))
    for index, f1 in enumerate(f1_scores):
        outf1.write("%s|%s\n" % (int2code[index], f1))
