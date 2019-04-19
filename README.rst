python-pinyin-jyutping-sentence
===============================

Python module which converts a Chinese sentence from Simplified to Mandarin/Pinyin and Traditional to Cantonese/Jyutping, outputting diacritics (accented characters). I designed this library to create Mandarin and Cantonese flashcards.

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

REST API
--------

You can use the REST API at the following URL:

.. code:: python

    http://api.mandarincantonese.com/jyutping/我哋盪失咗
    {"jyutping": "ngǒ déi dongsāt zó"}
    http://api.mandarincantonese.com/pinyin/办所有的事情
    {"pinyin": "bàn suǒyǒu de shìqíng"}

    # calling the API from python
    import requests
    import json

    url = "http://api.mandarincantonese.com/jyutping/我哋盪失咗"
    response = requests.get(url)
    print(json.loads(response.content)["jyutping"])    
    >>> ngǒ déi dongsāt zó

How it works
------------

Uses the Jieba library (https://github.com/fxsjy/jieba) to tokenize the sentence. Then words are converted to Pinyin/Jyutping either as a whole, or character by character, using the CC-Canto dictionary (http://cantonese.org/about.html). The Jyutping diacritic conversion is not standard but originally described here: http://www.cantonese.sheik.co.uk/phorum/read.php?1,127274,129006


