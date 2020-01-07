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
    """
    relations = []
    i = 0
    for text in corpus.files:
        for sentence in text.sentences:
            for word in sentence.words:
                if word.head != 0:      # skip the root
                    head = sentence.words[word.head - 1]        # identify head of current token
                    relations.append((word.lemma, word.deprel, head.lemma))     # append token, relation and head token
                    # additional handling of complex verb forms:
                    if re.match('VA', head.pos):  # if head is auxiliary verb, search for dependent full verb
                        for word2 in sentence.words:
                            if word2.head == head.id and re.match('VV', word2.pos) and word2 != word:
                                relations.append((word.lemma, word.deprel, word2.lemma))
                                i += 1

        print('Finished working on {}.'.format(text.path))

    print('(Added {} complex verbs)'.format(i))

    return relations


def get_collocations(relations):
    """
    calculate collocations based on the list of all relations in the corpus
    """
    relation_types = set([item[1] for item in relations])
    results = pd.DataFrame(columns=['word_1', 'relation', 'word_2', 'llr', 'frequency'])
    i = 1
    for relation_type in relation_types:
        print('Calculating scores for {}...'.format(relation_type))
        instances = [item for item in relations if item[1] == relation_type]
        bigram_counts = Counter(instances)
        unigrams_pos1 = [item[0] for item in instances]
        unigrams_pos2 = [item[2] for item in instances]
        unigram_counts_pos1 = Counter(unigrams_pos1)
        unigram_counts_pos2 = Counter(unigrams_pos2)

        for bigram in bigram_counts:
            ratio = llr.llr_2x2(bigram_counts[bigram],
                                unigram_counts_pos1[bigram[0]],
                                unigram_counts_pos2[bigram[2]],
                                sum(bigram_counts.values()))
            results.loc[i] = [bigram[0], bigram[1], bigram[2], ratio, bigram_counts[bigram]]
            i += 1

    results = results.iloc[(-results['llr'].abs()).argsort()]  # sort dataframe by absolute value of llr
    results = results.reset_index(drop=True)  # update index

    return results


directory = 'demo-corpus/'
corpus = Corpus(directory)
relations = get_relations(corpus)
result = get_collocations(relations)
result.to_csv('collocations_syntax.txt', sep='\t')      # write to file
print('Finished!')
