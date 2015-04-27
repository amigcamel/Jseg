# -*-coding:utf-8-*-
from jieba import Jieba
import multi
import time
import logging
logger = logging.getLogger(__name__)


text = '''網友瘋傳高市新興分局發給各單位協助慈濟骨髓捐贈者戶籍查訪「交辦單」，但不是說「警務大瘦身、大砍20項業務嗎？」引發基層員警議論紛紛；新興分局表示，交辦時間是17日，在警政署20日宣布簡化警察協辦業務前，未來對於類似服務需求將會視個案狀況審慎處理。
警政署20日公布20項簡化協辦業務，讓警察回歸專業，網路即瘋傳一張高市新興分局指派各警勤區員警，到骨髓捐贈者的戶籍地查訪、通告「交辦單」；網友們還在交辦單上打上「署長一直在減別人的爛攤子、高雄卻也是一直撿爛攤子」嘲諷引發群起議論。
不少網友留言：「這種急難救助，不是應該衛生單位訪查嗎？怎會是基層員警？」，也有人認為這太誇張，說「慈濟是收費的，不是免費幫人看病，這不是為民服務，根本是幫慈濟跑腿」；連慈濟義工都看不下，直言「這是我們慈濟人工作，不應交辦給警察，還用他們的警勤時間，做我們的事。」
新興分局指出，慈濟骨髓幹細胞中心請各縣警察局代為協尋已配對成功、但失去聯繫的骨髓幹細胞志願捐贈者，屬急難救助業務一環，盼結合警政分布系統，在最短時間內找尋該志願者，轉送通知信函，速與慈濟骨髓幹細胞中心聯絡，以辦理捐贈移植手續。
新興分局表示，尊重基層同仁想法及建議，對此類服務將儘量婉拒，但如遇到有緊急、非迅速找到配對捐贈者無法救命者，考慮人道精神，仍依個案來協助；絕不給基層員警造成任何工作負荷。'''

texts = [text] * 1000

j = Jieba()


def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        logger.info('%r %f sec' % (method.__name__, te-ts))
        return result

    return timed


@timeit
def single_test():
    con = []
    for text in texts:
        con.append(j.seg(text))


@timeit
def multi_test():
    multi.seg(texts, 8)


if __name__ == '__main__':
    single_test()
    multi_test()
