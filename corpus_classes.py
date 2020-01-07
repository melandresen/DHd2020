#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Python 3.7
# Author: Melanie Andresen (melanie.andresen@uni-hamburg.de)
# written in the context of the research project hermA (www.herma.uni-hamburg.de)
# funded by Landesforschungsförderung Hamburg

########################################################################################
# classes for representing a corpus based on conll files
########################################################################################

import sys
import os
import re


class Word:
    """word with linguistic features
    input: feature list as conll
    output: Word object with linguistic features
    """

    def __init__(self, feature_list):

        if len(feature_list) == 10:
            self.id = int(feature_list[2])
            self.token = feature_list[3]
            self.lemma = feature_list[4]
            self.pos = feature_list[5]
            self.morph = feature_list[6]
            self.head = int(feature_list[7])
            self.deprel = feature_list[8]
            self.coref = feature_list[9]

        elif len(feature_list) == 14:
            self.id = int(feature_list[0])
            self.token = feature_list[1]
            self.lemma = feature_list[3]
            self.pos = feature_list[5]
            self.morph = feature_list[7]
            self.head = int(feature_list[9])
            self.deprel = feature_list[11]
            self.coref = ''

        elif len(feature_list) == 8:
            self.id = int(feature_list[0])
            self.token = feature_list[1]
            self.lemma = feature_list[2]
            self.pos = feature_list[4]
            self.morph = feature_list[5]
            self.head = int(feature_list[6])
            self.deprel = feature_list[7]
            self.coref = ''

        else:
            print(len(feature_list))
            sys.exit('Sorry, unknown Conll format!')

    def __repr__(self):
        return 'Word({})'.format(self.token)


class Sentence:
    """ list of words
    input: conll-String
    ouput: Sentence-Object (nested list)
    """

    def __init__(self, conll_string):

        self.words = []
        word_list = conll_string.split('\n')  # transforms sentences to lists of words
        for word in word_list:
            word = re.sub(' {2}', '\t', word)
            word = word.split('\t')  # transforms words to lists of features
            self.words.append(Word(word))

        self.token_string = ' '.join([word.token for word in self.words])  # adds token string for readability

    def get_subjects(self):

        for word in self.words:
            if word.deprel == 'SUBJ':
                return word.token

    def __repr__(self):
        return 'Sentence({})'.format(' '.join([word.token for word in self.words]))


class Text:
    """ list of sentences
    input: path to conll-file
    output: list of Sentences
    """

    def __init__(self, file):
        self.path = file
        self.sentences = []
        self.is_valid = True  # variable for marking invalid (empty) texts
        with open(file, 'r', encoding='utf8') as input_data:
            text = input_data.read()
        if not text:  # if the file is empty
            print('WARNING: Empty file: {}'.format(file))
            self.is_valid = False  # mark the text as invalid for later exclusion
        else:
            text = text.strip()
            text = re.sub('#begin document.*?\n', '', text)
            text = re.sub('#end document.*', '', text)
            text = text.strip()
            conll_strings = text.split('\n\n')  # transforms text to list of sentences
            for conll_string in conll_strings:
                self.sentences.append(Sentence(conll_string))


class Corpus:
    """list of Texts
    input: path to directory
    output: list of Texts
    """

    def __init__(self, path, files=None):

        print('Corpus is being compiled...\n')

        self.files = []
        if not files:
            files = os.listdir(path)
            files = [f for f in files if re.search('(conll|txt)', f)]  # reduction to txt and conll files
            files = [f for f in files if not re.match('\.', f)]  # exclusion of mac system files
        for file in files:
            self.files.append(Text(path + file))
            print('File {} imported.'.format(file))
        self.files = [obj for obj in self.files if
                      obj.is_valid]  # excludes texts that were declared invalid for some reason
        print('Corpus import finished.')

    def search(self, search_term):
        """returns a list of all sentences with a given search term (currently token only)
        """
        results = []
        for text in self.files:
            for sentence in text.sentences:
                lemmas = [word.lemma for word in sentence.words]
                if search_term in lemmas:
                    results.append(sentence)
        return results
