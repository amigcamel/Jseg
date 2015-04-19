from Jieba import Jieba

jieba = Jieba()
print 'loading default dictionary...'
jieba._gen_trie()
print 'loading guarantee word list...'
jieba._load_guarantee_wlst()
