#!/usr/bin/env python

"""
A feature extractor for chunking.
Copyright 2010,2011 Naoaki Okazaki.
"""

# Separator of field values.
separator = ' '

# Field names of the input data.
fields = 'w pos num cap ind month link punc first last pref3 pref4 suff3 suff4 len1 len2 len35 len6 y'

# Attribute templates.
templates = (
    (('w', -2), ),
    (('w', -1), ),
    (('w',  0), ),
    (('w',  1), ),
    (('w',  2), ),
    (('cap', 0), ),
    (('ind', 0), ),
    (('month', 0), ),
    (('link', 0), ),
    (('num', 0), ),
    (('punc', 0), ),
    (('first', 0), ),
    (('last', 0), ),
    (('pref3', 0), ),
    (('pref4', 0), ),
    (('suff3', 0), ),
    (('suff4', 0), ),
    (('len1', 0), ),
    (('len2', 0), ),
    (('len35', 0), ),
    (('len6', 0), ),
    (('w', -1), ('w',  0)),
    (('w',  0), ('w',  1)),
    (('pos', -2), ),
    (('pos', -1), ),
    (('pos',  0), ),
    (('pos',  1), ),
    (('pos',  2), ),
    (('pos', -2), ('pos', -1)),
    (('pos', -1), ('pos',  0)),
    (('pos',  0), ('pos',  1)),
    (('pos',  1), ('pos',  2)),
    (('pos', -2), ('pos', -1), ('pos',  0)),
    (('pos', -1), ('pos',  0), ('pos',  1)),
    (('pos',  0), ('pos',  1), ('pos',  2)),
    )


import crfutils

def feature_extractor(X):
    # Apply attribute templates to obtain features (in fact, attributes)
    crfutils.apply_templates(X, templates)
    if X:
    # Append BOS and EOS features manually
        X[0]['F'].append('__BOS__')     # BOS feature
        X[-1]['F'].append('__EOS__')    # EOS feature

if __name__ == '__main__':
    crfutils.main(feature_extractor, fields=fields, sep=separator)