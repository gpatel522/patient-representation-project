import nltk
import gensim
from nltk.corpus import abc
from keras.preprocessing.text import Tokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
import warnings

warnings.filterwarnings(action='ignore')
from gensim.models import Word2Vec

if __name__ == "__main__":
    #nltk.download('punkt')
    # print('abc', abc.sents())  # actual text that is tokenized. Each line is a list of tokenized words
    # print(type(abc.sents()))
    # model = gensim.models.Word2Vec(abc.sents())
    #
    # X = list(model.wv.vocab)
    # # print('X:', X)
    #
    # findSimilarWords = 'science'
    # data = model.most_similar(findSimilarWords)
    # print("similar to ", findSimilarWords, data)

    lines = []
    with open('../data/MimicIII/Patients/mimic-cuis.txt') as fin:
        for line in fin:
            lines.append(line.strip())
            print(line.strip())
        print(lines)
        vocab = [s.encode('utf-8').split() for s in lines]





    docs = ['Well done!',
            'Good work',
            'Great effort',
            'nice work',
            'Excellent!',
            'Weak',
            'Poor effort!',
            'not good',
            'poor work',
            'Could have done better.']
    vocab = [s.encode('utf-8').split() for s in docs]
    print(vocab)

    data = []
    for doc in docs:
        for i in sent_tokenize(doc):
            temp = []

            # tokenize the sentence into words
            for j in word_tokenize(i):
                temp.append(j.lower())

            data.append(temp)
    model = gensim.models.Word2Vec(vocab, min_count=1)

    X = list(model.wv.vocab)
    print('X:', X)

    findSimilarWords = 'Weak'
    data = model.most_similar(findSimilarWords)
    print("similar to ", findSimilarWords, data)