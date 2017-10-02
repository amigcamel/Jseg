# -*-coding:utf-8-*-
from os.path import abspath, dirname, join
import urllib2
import re
import time
import json

CUR_PATH = dirname(abspath(__file__))


def craw_emo(save=True):
    base = 'http://facemood.grtimed.com/index.php?view=facemood&tid=%d'
    pat = re.compile(u'''flashvars="str=(.*?)"''')
    emos = []

    cnt1 = 1
    while cnt1 < 200:
        print cnt1
        url = base % cnt1
        raw = urllib2.urlopen(url).read().decode('utf-8')
        res = pat.findall(raw)
        if res == []:
            cnt1 += 1
        else:
            emos += res
            cnt2 = 2
            while True:
                url2 = url + '&page=%d' % cnt2
                print url2
                raw2 = urllib2.urlopen(url2).read().decode('utf-8')
                res2 = pat.findall(raw2)
                if res2 == []:
                    break
                else:
                    emos += res2
                    cnt2 += 1
                    time.sleep(0.5)
            cnt1 += 1
            time.sleep(0.5)
            print '%d emos collected' % len(emos)
    emos = list(set(emos))
    if save:
        with open('emodata.json', 'w') as jf:
            json.dump(emos, jf)
        print 'emoticons saved!'
    else:
        return emos


def load_emo():
    with open(join(CUR_PATH, 'emoall.txt'), encoding="utf-8") as f:
            "") as f:
        emos = f.read().decode('utf-8')
    emos = emos.split('\n')
    emos = [i for i in emos if i != '\n']
    # with open(join(CUR_PATH, 'emodata.json')) as jf1, \
    #      open(join(CUR_PATH, 'emo2.json')) as jf2, \
    #      open(join(CUR_PATH, 'emo3.json')) as jf3, \
    #      open(join(CUR_PATH, 'emo4.json')) as jf4:
    #     emos1 = json.load(jf1)
    #     emos2 = json.load(jf2)
    #     emos3 = json.load(jf3)
    #     emos4 = json.load(jf4)
    # emos = emos1 + emos2 + emos3
    emo_ext = [u'= =', u'=.=', u'=_=', u'>///<', u'> <', u'orz',
               u'^ ^', u'XD', u'(′･_･`)', u'-_-||', u'>"<', u'T.T']
    emos += emo_ext
    emos = list(set(emos))
    emos = [i.strip() for i in emos]
    return emos


def ensure_unicode(string):
    if not isinstance(string, unicode):
        try:
            string = string.decode('utf-8')
        except:
            raise UnicodeError('Input should be UTF8 or UNICODE')
    return string

emos = load_emo()


def find_emo(txt, source=False):
    global emos
    txt = ensure_unicode(txt)
    res = [i for i in emos if i in txt]
    if source is True:
        for x in res:
            txt = txt.replace(x, '<span>' + x + '</span>')
        return (res, txt)
    return res

# source
# http://facemood.grtimed.com/ (顏文字卡)   --> emodata.json
# http://news.gamme.com.tw/55689 (宅宅新聞) --> emo2.json
# http://www.ptt.cc/bbs/cksh77th17/M.1158075878.A.9D2.html (PTT) --> emo3.json
# http://j831124g2009.pixnet.net/blog/post/17973045-素材│日本顏文字（可愛）(*☉౪⊙*)
# (痞客邦) --> emo4.json

# problems
# 兩行以上的emoticons怎麼辦？
#　　　　 ▲           ▲             ▲
# ﹏﹏(ㄏ￣▽￣)ㄏ  q(〒□〒)p    ㄟ(￣▽￣ㄟ)﹏﹏  通通變成阿飄
