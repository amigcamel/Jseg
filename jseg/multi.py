from jieba import Jieba
import logging
import multiprocessing
logger = logging.getLogger(__name__)
# logger = multiprocessing.get_logger()
# multiprocessing.log_to_stderr()
# logger.setLevel(logging.DEBUG)
try:
    import coloredlogs
    coloredlogs.install(level=logging.INFO)
except:
    pass


j = Jieba()


def _seg_wrapper(text):
    global j
    pid = multiprocessing.current_process().pid
    logger.debug('current pid: %s' % pid)
    return j.seg(text).raw


def seg(texts, processes=4):
    pool = multiprocessing.Pool(processes=processes)
    result = []
    for text in texts:
        result.append(pool.apply_async(_seg_wrapper, (text, )))
    pool.close()
    pool.join()
    result = [i.get() for i in result]
    return result
