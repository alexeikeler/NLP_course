import pandas as pd
import random
import nltk
import pickle
import time
import argparse

from nltk.corpus import treebank
from nltk.corpus import brown

from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer

from tabulate import tabulate

from preprocess_data import PPData

# Tree bank sents for test
tagged_sentences = treebank.tagged_sents(tagset='universal')

# Brown sents for train
brown_tagged_sents = brown.tagged_sents(categories='news', tagset='universal')
brown_sents = brown.sents(categories='news')

s, e = random.randint(0, 20), random.randint(20, 40) 
psb = brown_tagged_sents[s:e]


def process_command_line_arguments():
    
    parser = argparse.ArgumentParser(
        'Arguments description for POS tagging model based on sklearn DecisionTreeClassifier.\
        \nModel runs in 3 modes: train, test, predict.'
    )
    
    parser.add_argument(
        '-t',
        '--train',
        dest='train',
        action='store_true',
        help='If specified model runs in TRAIN MODE.',
        required=False
    )

    parser.add_argument(
        '-v',
        '--validate',
        dest='validate',
        action='store_true',
        help='If specified model runs in VALIDATION MODE.',
        required=False
    )

    parser.add_argument(
        '-p',
        '--predict',
        dest='predict',
        action='store_true',
        help='Run model in PREDICTION MODE',
        required=False
    )

    parser.add_argument(
        '-s',
        '--split',
        dest='split',
        help='Amount of data which will be used to train model. 1 - s is used to test model.',
        required=False,
        default=0.75
        )

    return parser.parse_args()


def train_model(training_sentences):
    
    train_start_time = time.time()

    x, y = PPData.transform_to_dataset(training_sentences)

    dict_vectorizer = DictVectorizer(sparse=False)
    dict_vectorizer.fit(x, y)

    classifier = Pipeline(
        [
            ('vectorizer', DictVectorizer(sparse=False)),
            ('classifier', DecisionTreeClassifier(criterion='entropy'))
        ]
    )

    # 21.4 Gb for all data set is too much, so we are using first 10k samples
    classifier.fit(x[:10000], y[:10000])

    dtc_model_file = 'dtc_model.sav'

    pickle.dump(classifier, open(dtc_model_file, 'wb'))

    print(f'Train time: {time.time() - train_start_time}')


def validate_model(test_sentences):
    
    test_model_time = time.time()

    try:
        with open('dtc_model.sav', 'rb') as model:
            descision_tree_classifier = pickle.load(model)

    except Exception as e:
        print(f'Error occured while loading model.\n{repr(e)}')

    x_test, y_test = PPData.transform_to_dataset(test_sentences)
    accuracy = descision_tree_classifier.score(x_test, y_test)

    print(f'Model accuracy: {accuracy}\nValidation time: {time.time() - test_model_time} sec')


def make_prediction(sentences):

    try:
        with open('dtc_model.sav', 'rb') as model:
            descision_tree_classifier = pickle.load(model)

    except Exception as e:
        print(f'Error occured while loading model.\n{repr(e)}')

    df_score = pd.DataFrame(
        columns=[
            'SENTECE LENGTH',
            'NLTK POS TAG TIME',
            'DTC POS TAG TIME',
            'DTC MODEL ACC',
            'NLTK POS_TAG METHOD ACC'
        ]
    )

    for sentence in sentences:

        words, tags = PPData.split(sentence)

        sentence_length = len(words)

        start_dtc_time = time.time()
        prediction_tags = descision_tree_classifier.predict(
            [PPData.features(words, index) for index in range(sentence_length)]
        )
        end_dtc_time = time.time() - start_dtc_time        
        
        start_nltk_time = time.time()
        nltk_pos_tag_prediction = nltk.pos_tag(words, tagset='universal')
        end_nltk_time = time.time() - start_nltk_time

        df_score['SENTECE LENGTH'] = [sentence_length]
        df_score['NLTK POS TAG TIME'] = [end_nltk_time]
        df_score['DTC POS TAG TIME'] = [end_dtc_time]

        df = pd.DataFrame(
            [words, tags, prediction_tags, PPData.unword(nltk_pos_tag_prediction)],
            index=['WORD', 'GROUND TRUTH','DTC MODEL TAG', 'NLTK POS_TAG METHOD TAG']
        ).transpose()

        df_score['DTC MODEL ACC'] = df[(df['DTC MODEL TAG'] == df['GROUND TRUTH'])].shape[0] / df.shape[0] 

        df_score['NLTK POS_TAG METHOD ACC'] = df[
                                                  (df['NLTK POS_TAG METHOD TAG'] == df['GROUND TRUTH'])
                                              ].shape[0] / df.shape[0]
      
        print('\n-----------------------------------------------------------------------------------------------------')
        
        print(
            tabulate(
                df,
                headers=['WORD', 'GROUND TRUTH','DTC MODEL TAG', 'NLTK POS_TAG METHOD TAG'],
                tablefmt='pretty'
            ),
            tabulate(
                df_score,
                headers=df_score.columns,
                tablefmt='pretty'
            ),
            sep='\n'
        )
        print('-----------------------------------------------------------------------------------------------------\n')


def main():

    args = process_command_line_arguments()
    
    train_test_split = float(args.split)

    # Test split = 1 - train_split (%)
    
    part = int(train_test_split * len(tagged_sentences))

    training_sentences = tagged_sentences[:part]
    test_sentences = tagged_sentences[part:]

    if args.train:
        train_model(training_sentences)
        validate_model(test_sentences)

    elif args.validate:
        validate_model(test_sentences)

    elif args.predict:
        make_prediction(psb)


if __name__ == '__main__':
    main()