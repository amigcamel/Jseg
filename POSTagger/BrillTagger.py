from os.path import dirname , abspath, join
import pickle,nltk

CURPATH = dirname(abspath(__file__))

tagger = pickle.load(open(join(CURPATH, 'sinica_treebank_brill_aubt/sinica_treebank_brill_aubt.pickle')))
