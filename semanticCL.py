
import numpy as np
import pandas as pd
import nltk
import re
import string
import random
import json


from nltk.stem.wordnet import WordNetLemmatizer

from pymystem3 import Mystem

from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

from pprint import pprint




def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

def lemmatize_sentence(tokens):
    mystem = Mystem()
    lemmatized_sentence = []
    cleaned_tokens=[]
    for word, tag in pos_tag(tokens, lang='rus'):
       lemmatized_sentence.append(mystem.lemmatize(word))
       if word.lower() not in stop_words:
            cleaned_tokens.append(word.lower())
    return cleaned_tokens

def work(jsonFileDay):
    lists = jsonFileDay['Column1'].tolist()  # поменять название
    m = Mystem()
    newLemms = list()
    for i in lists:  # поменять название
        lemmas = m.lemmatize(i)
        lemmas2 = ' '.join(lemmas)
        
        tokenss = nltk.word_tokenize(lemmas2)  # токенизируем слова епт его
        pos_tag(tokenss, lang='rus')  # позиции
        newLemms.append(lemmatize_sentence(tokenss))  # достаем леммы(без предлогов и тд)
        print(newLemms)
    return newLemms


if __name__ == "__main__":

    ####---Рабочий код
    stop_words = stopwords.words("russian")
    positive = pd.read_json('C:/Users/btema/Desktop/negativeJSON1.json')
    #negative = pd.read_json('C:/Users/mikha/Desktop/negative.json')
    #text = pd.read_json('C:/Users/mikha/Desktop/negative.json') #подключаем джисон предложений из бд
    positive_lemms = work(positive)
    #negative_lemms = work(negative)
    #text = work(positive)

    ####-----------
    ####-----------дальше
    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []


    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))


    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    freq_dist_pos = FreqDist(all_pos_words)
    print(freq_dist_pos.most_common(10))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))

    print(classifier.show_most_informative_features(10))

    custom_tweet = "я и грустная и вижу Отцов."

    custom_tokens = remove_noise(word_tokenize(custom_tweet))

    print(custom_tweet, classifier.classify(dict([token, True] for token in custom_tokens)))
    """
    

    
    ###

    """

