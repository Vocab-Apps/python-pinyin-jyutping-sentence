python-pinyin-jyutping-sentence
===============================

Python module which converts a Chinese sentence from Simplified to Mandarin/Pinyin and Traditional to Cantonese/Jyutping, outputting diacritics (accented characters)

Install
-------

.. code:: bash

    $ pip install pinyin_jyutping_sentence

Usage
-----

.. code:: python

    >>> import pinyin_jyutping_sentence
    >>> pinyin_jyutping_sentence.pinyin("提高口语")
    'tígāo kǒuyǔ'
    >>> pinyin_jyutping_sentence.jyutping("我出去攞野食")
    'ngǒ cēothêoi ló jěsik'

How it works
------------

Uses the Jieba library (https://github.com/fxsjy/jieba) to tokenize the sentence. Then words are converted to Pinyin/Jyutping either as a whole, or character by character, using the CC-Canto dictionary (http://cantonese.org/about.html). The Jyutping diacritic convertion is not standard but original described here: http://www.cantonese.sheik.co.uk/phorum/read.php?1,127274,129006


