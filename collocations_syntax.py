#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Python 3.7
# Author: Melanie Andresen (melanie.andresen@uni-hamburg.de)
# written in the context of the research project hermA (www.herma.uni-hamburg.de)
# funded by Landesforschungsförderung Hamburg


########################################################################################
# calculate syntax-based collocations
########################################################################################

import re
import pandas as pd
from collections import Counter
import llr  # by Ted Dunning, see https://github.com/tdunning/python-llr
from corpus_classes import Corpus


def get_relations(corpus):
    """
    Extract a list of binary syntactic relations from the corpus
    input: Corpus object (see corpus_classes.py)
    output: list of all binary syntactic relations in the corpus
    """
    relations = []
    no_of_complex_verbs = 0
    for text in corpus.files:
        for sentence in text.sentences:
            for word in sentence.words:
                if word.head == 0:      # skip the root
                    continue
                head = sentence.words[word.head - 1]        # identify head of current token
                relations.append((word.lemma, word.deprel, head.lemma))     # append token, relation and head token
                # additional handling of complex verb forms:
                if re.match('VA', head.pos):        # if head is auxiliary verb, search for dependent full verb
                    for word2 in sentence.words:
                        if word2.head == head.id and re.match('VV', word2.pos) and word2 != word:
                            relations.append((word.lemma, word.deprel, word2.lemma))
                            no_of_complex_verbs += 1

        print('Relations from {} extracted.'.format(text.path))

    print('(Added {} complex verbs)\n'.format(no_of_complex_verbs))

    return relations


def get_collocations(relations):
    """
    Calculate collocations based on the list of all relations in the corpus
    input: list of all binary syntactic relations in the corpus (result of get_relations())
    output: pandas DataFrame with all syntactic collocations and their llr scores
    """
    print('Calculating collocations (this may take a while)...')

    relation_types = set([item[1] for item in relations])
    results = pd.DataFrame(columns=['word_1', 'relation', 'word_2', 'llr', 'frequency'])

    for relation_type in relation_types:
        print('Calculating scores for {}...'.format(relation_type))
        instances = [item for item in relations if item[1] == relation_type]
        bigram_counts = Counter(instances)
        unigram_counts_pos1 = Counter([item[0] for item in instances])
        unigram_counts_pos2 = Counter([item[2] for item in instances])

        all_bigrams_count = sum(bigram_counts.values())
        for bigram in bigram_counts:
            ratio = llr.llr_2x2(bigram_counts[bigram],
                                unigram_counts_pos1[bigram[0]],
                                unigram_counts_pos2[bigram[2]],
                                all_bigrams_count)
            results = results.append(pd.DataFrame([[bigram[0], bigram[1], bigram[2], ratio, bigram_counts[bigram]]], columns=['word_1', 'relation', 'word_2', 'llr', 'frequency']))

    results = results.iloc[(-results['llr'].abs()).argsort()]  # sort dataframe by absolute value of llr
    results = results.reset_index(drop=True)  # update index

    return results


directory = 'demo-corpus/'
corpus = Corpus(directory)
relations = get_relations(corpus)
result = get_collocations(relations)
result.to_csv('collocations_syntax.txt', sep='\t')
