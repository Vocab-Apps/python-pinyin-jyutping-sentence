import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)

logger.debug('START loading pinyin_jyutping_sentence')
import pinyin_jyutping_sentence
logger.debug('DONE loading pinyin_jyutping_sentence')
