#-*-coding:utf-8-*-
import re

metachr = '^$*+?{}[]\|()'

heads = u'''>ζↁ━இㅇ（┌／∑┐ψ〒ʕ└⊙＜√＝☜ㄟ〠Σ•ತ✧╰(*-/☮Oε┴‷〈ಸ爻<︿乁♡ｂˋ⁄ˇఠ◉ಠ○vｍ#◎⇎Ψmb◔♀ⶸლ\｡￣◢づ‧≧흫…╭o╮ჰ≡癶凸~ヽヾ'''
tails = u'''ↁﾉ「↑̖〠ิ▽♀⁄ˇ◣～⑤╮凵︿・|━）dʔಠ√ತ'+/°3ืಸ;?ξツఠｍ﹏◎"⇎｡≡╩╭oჴஇ☆┌з┐〒↗⊙☮☞•…*.┴:＼︴♡σ♂ｄ○●Z￣b≦♪╬╰癶>ｼ~＃〉３↘┛”；!✧)Ψ-ⶸ=＿ㅇψˊノ◔ლaづ╧흫m╯y凸'''
for i in metachr:
    heads = heads.replace(i, '\\'+i)
    tails = tails.replace(i, '\\'+i)


def ensure_unicode(string):
    if not isinstance(string, unicode):
        try:
            string = string.decode('utf-8')
        except:
            raise UnicodeError('Input should be UTF8 or UNICODE')
    return string

def clear_num(txt):
    num_pat = re.compile(u'''([0-9\-.:/]{2,})''')
    res = num_pat.sub('', txt)
    return res

def post_check(candlst):
    con = []
    for i in candlst:
        while True:
            i_mod = i.strip()
            i_mod = re.sub(u'\([一-龥]{1,}[\)]{0,1}', '', i_mod)
            i_mod = re.sub(u'（[一-龥]{1,}）', '', i_mod)
            if len(set(i_mod)) < 3:
                break
            else:
                if re.search(u'^m:[0-9a-zA-Z一-龥]', i_mod): # m:大大
                    break
                elif re.search(u'^~[0-9a-zA-Z一-龥]', i_mod): #~4次
                    break
                elif i_mod == i:
                    con.append(i_mod)
                    break
                else:
                   i = i_mod 
                   continue
    return con

def exclude_cht(txt):
    pat = re.compile(u'''(?!.*[.a-zA-Z][.a-zA-Z])([一-龥][一-龥]{2,})''')
    while True:
        res = pat.sub('', txt)
        if res == txt:
            return res
        else:
            txt = res
            exclude_cht(txt)

def find_emo(txt, source=False):
    txt = ensure_unicode(txt)
    txt_mod = clear_num(txt)
    txt_mod = exclude_cht(txt_mod)
    emo_pat = re.compile(u'''(?!.*[.a-zA-Z][.a-zA-Z])([%s].{3,})''' % heads)
    res = emo_pat.findall(txt_mod)
    res = post_check(res)
    res = [i for i in res if i in txt]
    if source == True:
        for x in res:
            txt = txt.replace(x, '<span>'+x+'</span>') 
        return (res,txt)
    return res

