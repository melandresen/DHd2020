#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Python 3.7
# Author: Melanie Andresen (melanie.andresen@uni-hamburg.de)
# written in the context of the research project hermA (www.herma.uni-hamburg.de)
# funded by Landesforschungsförderung Hamburg


########################################################################################
# calculate surface-based collocations
########################################################################################

import os
import re
import nltk
from corpus_classes import Corpus


def load_corpus_lemma(directory):
    """
    Extract words from a directory of annotated files
    input: path to directory as string
    output: list of lemmas in all files in the directory (no punctuation)
    """
    result = []
    corpus = Corpus(directory)
    for text in corpus.files:
        for sentence in text.sentences:
            for word in sentence.words:
                if word.pos not in ['$.', '$,', '$(']:
                    result.append(word.lemma)

    return result


def load_corpus_token(directory):
    """
    Use this function instead of load_corpus_lemma() if you only have raw text
    """
    files = os.listdir(directory)  # get list of files in directory
    files = [f for f in files if not re.match('\.', f)]  # filter for system files (mac)
    print('{} files will be searched...'.format(len(files)))
    result = []
    for file in files:
        with open(directory + file, 'r') as in_file:
            text = in_file.read()
        tokens = nltk.word_tokenize(text)
        result.extend(tokens)

    return result


def generate_collocations(tokens):
    """
    Calculate collocations from a list of all words in the corpus
    input: list of tokens,
    output: list of collocations with scores
    """
    print('Calculating collocations...')

    stopwords = ['--']
    # stopwords = nltk.corpus.stopwords.words('german')     # uncomment to exclude stop words
    bigram_measures = nltk.collocations.BigramAssocMeasures()

    finder = nltk.BigramCollocationFinder.from_words(tokens, window_size=3)
    finder.apply_word_filter(lambda w: w.lower() in stopwords)
    finder.apply_freq_filter(1)
    llr_scores = finder.score_ngrams(bigram_measures.likelihood_ratio)
    frequencies = sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))

    return llr_scores, frequencies


directory = 'demo-corpus/'
corpus = load_corpus_lemma(directory)
llrs, abs_freq = generate_collocations(corpus)
abs_freq_dict = dict(abs_freq)

with open('collocations_surface.txt', 'w') as out_file:
    for item in llrs:
        word_1 = item[0][0]
        word_2 = item[0][1]
        llr = item[1]
        absolute_frequency = abs_freq_dict[item[0]]
        out_file.write('{}\t{}\t{}\t{}\n'.format(word_1, word_2, llr, absolute_frequency))

# ToDo: Text- und Satzgrenzen berücksichtigen?
