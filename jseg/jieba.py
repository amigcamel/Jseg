# -*- coding: utf-8 -*-
from __future__ import division
from math import log
from os.path import dirname, abspath, join
from string import punctuation
from emodet import find_emo
import json
import re
import pickle


import logging
logger = logging.getLogger(__name__)
try:
    import coloredlogs
    coloredlogs.install(level=logging.INFO)
except:
    pass

CUR_PATH = dirname(abspath(__file__))
with open(join(CUR_PATH, 'brill_tagger.pkl'), 'rb') as f:
    BrillTagger = pickle.load(f)


class Hmm:

    def __init__(self):
        self._min_float = -3.14e100
        self._prev_status = {
            'B': ('E', 'S'),
            'M': ('M', 'B'),
            'S': ('S', 'E'),
            'E': ('B', 'M')
        }

        self._prob = dict()
        probs = ['initP', 'tranP', 'emisP']
        for prob in probs:
            with open(join(CUR_PATH, 'prob', prob + '.json')) as jf:
                self._prob[prob] = json.load(jf)

    def _viterbi(self, obs, states, start_p, trans_p, emit_p):
        _v = [{}]  # tabular
        path = {}
        for y in states:  # init
            _v[0][y] = start_p[y] + emit_p[y].get(obs[0], self._min_float)
            path[y] = [y]
        for t in range(1, len(obs)):
            _v.append({})
            newpath = {}
            for y in states:
                em_p = emit_p[y].get(obs[t], self._min_float)
                (prob, state) = max(
                    [(_v[t - 1][y0] + trans_p[y0].get(y, self._min_float) + em_p, y0) for y0 in self._prev_status[y]])
                _v[t][y] = prob
                newpath[y] = path[state] + [y]
            path = newpath

        (prob, state) = max([(_v[len(obs) - 1][y], y) for y in ('E', 'S')])

        return (prob, path[state])

    def hmm_seg(self, sentence):
        con = []
        prob, pos_list = self._viterbi(sentence, ('B', 'M', 'E', 'S'), self._prob[
                                       'initP'], self._prob['tranP'], self._prob['emisP'])
        begin, next = 0, 0
        for i, char in enumerate(sentence):
            pos = pos_list[i]
            if pos == 'B':
                begin = i
            elif pos == 'E':
                con.append(sentence[begin:i + 1])
                next = i + 1
            elif pos == 'S':
                con.append(char)
                next = i + 1
        if next < len(sentence):
            con.append(sentence[next:])
        return con


class Jieba(Hmm):

    def __init__(self, load_ptt_dict=False):
        Hmm.__init__(self)
        self._freq = {}
        self._trie = {}
        self._min_freq = None
        self._gw, self._gwr = {}, {}
        self._gw_num = 0

        self._gen_trie()

        if load_ptt_dict:
            logger.debug('loading ptt dictionary')
            with open(join(CUR_PATH, "ptt_encyc.txt")) as tf:
                raw = tf.read()
                guarantee_wlst = filter(None, raw.split('\n'))
            self.add_guaranteed_wordlist(guarantee_wlst)

    def _load_dic(self):
        logger.debug('loading default dictionary')
        with open(join(CUR_PATH, "dict.txt")) as tf:
            raw = tf.read()
            dic = re.split('\r{0,1}\n', raw)
            dic = filter(None, dic)
            # 字典只得有中文

        return dic

    def add_guaranteed_wordlist(self, lst=None):
        '''
        Custom dictoinary should be a list of unicodes, e.g., [u'蟹老闆', u'張他口', u'愛米粒', u'劉阿吉']
        '''

        gw_num = self._gw_num
        if gw_num == 0:
            gw_num = 1
        for num, word in enumerate(lst, gw_num):
            self._gw_num = num
            self._gw[word] = '_gw' + str(num) + '@'
            self._gwr['_gw' + str(num) + '@'] = word

    def _gen_trie(self):
        dic = self._load_dic()
        total = 0.0
        for item in dic:
            word, freq = item.split(' ')
            freq = float(freq)
            self._freq[word] = freq
            total += freq
            p = self._trie
            for char in word:
                if char not in p:
                    p[char] = {}
                p = p[char]
            p[''] = ''  # ending flag

        self._freq = dict([(w, log(float(c) / total)) for w, c in self._freq.items()])
        self._min_freq = min(self._freq.values())

    def _get_dag(self, sentence):
        senlen = len(sentence)
        i, j = 0, 0
        p = self._trie
        dag = {}
        while i < senlen:
            c = sentence[j]
            if c in p:
                p = p[c]
                if '' in p:
                    if i not in dag:
                        dag[i] = []
                    dag[i].append(j)
                j += 1
                if j >= senlen:
                    i += 1
                    j = i
                    p = self._trie
            else:
                p = self._trie
                i += 1
                j = i
        for i in range(len(sentence)):
            if i not in dag:
                dag[i] = [i]
        return dag

    def _calc_route(self, sentence, dag, idx):
        route = {}
        senlen = len(sentence)
        route[senlen] = (0.0, '')
        for idx in range(senlen - 1, -1, -1):
            candidates = [(self._freq.get(
                sentence[idx:x + 1], self._min_freq) + route[x + 1][0], x) for x in dag[idx]]
            route[idx] = max(candidates)
        return route

    def _seg(self, sentence):  # cut DAG or hmm seg
        dag = self._get_dag(sentence)
        route = self._calc_route(sentence, dag, 0)
        dag_con = []
        x = 0
        buf = u''
        _n = len(sentence)
        while x < _n:
            y = route[x][1] + 1
            l_word = sentence[x:y]
            if y - x == 1:
                buf += l_word
            else:
                if len(buf) > 0:
                    if len(buf) == 1:
                        dag_con.append(buf)
                        buf = u''
                    else:
                        if buf not in self._freq:
                            regognized = self.hmm_seg(buf)
                            for t in regognized:
                                dag_con.append(t)
                        else:
                            for elem in buf:
                                dag_con.append(elem)
                        buf = u''
                dag_con.append(l_word)
            x = y

        if len(buf) > 0:
            if len(buf) == 1:
                dag_con.append(buf)
            else:
                if buf not in self._freq:
                    regognized = self.hmm_seg(buf)
                    for t in regognized:
                        dag_con.append(t)
                else:
                    for elem in buf:
                        dag_con.append(elem)
        return dag_con

    def seg(self, sentence, pos=True):

        # find emoticons
        emos = find_emo(sentence)
        emocan, emocan_r = {}, {}

        for num, emo in enumerate(emos):
            emocan[emo] = '_emo' + str(num) + '@'
            emocan_r['_emo' + str(num) + '@'] = emo

        for emo in emocan.keys():
            sentence = sentence.replace(emo, emocan[emo])

        # guarantee wlst
        # for gw in self._gw.keys():
        gws = self._gw.keys()
        gws = sorted(gws, key=lambda x: len(x), reverse=True)  # 長詞優先
        for gw in gws:
            if gw in sentence:
                sentence = sentence.replace(gw, self._gw[gw])

        re_han = re.compile(r"(http://.*?\s|_gw\d+?@|_emo\d+?@|[ㄅ-ㄩ一-龥]+)", re.U)
        # re_ch = re.compile(ur"[ㄅ-ㄩ\u4E00-\u9FA5]+")
        # re_alphnumeric = re.compile(ur'([a-zA-Z0-9]+)')
        re_eng = re.compile(r'[a-zA-Z]+')
        re_neu = re.compile(r'[0-9]+')
        re_url = re.compile(r'(http://.*?)[\s\n\r\n]')
        re_skip = re.compile(r"(\r{0,1}\n|\s)", re.U)

        puns = punctuation
        puns += ''.join([chr(ord(i) + 65248)
                         for i in puns])  # full-width punctuations
        puns += u'、。「」…“”'  # 要在加上一些常用標點符號
        br = u'\r{0,1}\n|\s'
        # metachr = u'^$*+?{}[]\|()'
        re_pun = re.compile(u'(%s|[%s])' % (br, puns))

        blocks = re_han.split(sentence)

        con = []
        for blk in blocks:
            if blk.startswith('_gw'):
                word = self._gwr[blk]
                logger.debug('find in dict: %s' % word)
                con.append((word, None))

            elif blk.startswith('_emo'):
                word = emocan_r[blk]
                con.append((word, 'EMOTICON'))
            elif re_url.match(blk):
                con.append((re_url.match(blk).group(1), 'URL'))
            # elif re_eng.match(blk):
                # con.append((blk, 'FW'))
            elif re_han.match(blk):
                for word in self._seg(blk):
                    con.append((word, None))
            else:
                tmp = re_pun.split(blk)
                for x in tmp:
                    if x != ' ' and x != '':
                        if re_skip.match(x):
                            con.append(('\n', 'LINEBREAK'))
                        else:
                            con.append((x, None))
        if pos:
            con_w = [i[0] for i in con]
            con_p1 = [i[1] for i in con]
            res = BrillTagger.tag(con_w)

            res_con = []
            for word_fin, pos_fin in res:
                if pos_fin == '-None-':
                    if re_pun.match(word_fin):
                        pos_fin = 'PUNCTUATION'
                    elif re_eng.match(word_fin):
                        pos_fin = 'FW'
                    elif re_neu.match(word_fin):
                        pos_fin = 'Neu'
                res_con.append((word_fin, pos_fin))

            word_seg = [i[0] for i in res_con]
            con_p2 = [i[1] for i in res_con]

            pos_con = []
            for pos_p1, pos_p2 in zip(con_p1, con_p2):
                if pos_p1 is None:
                    pos_out = pos_p2
                else:
                    pos_out = pos_p1
                pos_con.append(pos_out)

            output = zip(word_seg, pos_con)
            output_mod = []
            for word, pos in output:
                output_mod.append((word, pos))
            output_obj = Segres(output_mod)
            return output_obj
        else:
            con = [i[0] for i in con]
            return con


class Segres(object):

    def __init__(self, object):
        self.raw = object
        self.text = self.text()
        self.nopos = self.nopos()

    def text(self, mode='plain'):
        output = ''
        for word, pos in self.raw:
            if pos != 'LINEBREAK':
                if mode == 'plain':
                    output += '%s/%s' % (word, pos)
                elif mode == 'color':
                    output += '%s/\x1b[33m%s\x1b[0m' % (word, pos)
                elif mode == 'html':
                    output += '%s<span>/%s</span>' % (word, pos)
                else:
                    raise ValueError('Mode name error: %s' % mode)
                output += ' '
            else:
                output += word
        return output

    def nopos(self, mode='string'):
        '''
        Return segmentation results without POS tags.

        mode:
        1. string: return results with "str"
        2. list: return results with "list"
        '''
        output = [word for word, pos in self.raw]
        if mode == 'string':
            output = ' '.join(output)
            output = output.replace(' \n ', '\n')
        elif mode == 'list':
            pass
        else:
            raise ValueError('Mode name error: %s' % mode)
        return output


# TODO
# add construction detection
# 標點符號分割？
# backslash 可能有問題
