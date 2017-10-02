# -*-coding:utf-8-*-
from os.path import abspath, dirname, join

CUR_PATH = dirname(abspath(__file__))


def load_emo():
    with open(join(CUR_PATH, 'emoall.txt'), encoding="utf-8") as f:
        emos = f.read()
    emos = emos.split('\n')
    emos = [i for i in emos if i != '\n']
    emo_ext = [u'= =', u'=.=', u'=_=', u'>///<', u'> <', u'orz', u'^ ^', u'XD', u'(′･_･`)', u'-_-||', u'>"<', u'T.T']
    emos += emo_ext
    emos = list(set(emos))
    emos = [i.strip() for i in emos]
    return emos


def find_emo(txt):
    emos = load_emo()
    res = [i for i in emos if i in txt]
    return res
