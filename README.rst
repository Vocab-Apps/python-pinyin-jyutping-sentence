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
    # the tone_numbers argument can be used to disable diacritics
    >>> pinyin_jyutping_sentence.pinyin("忘拿一些东西了", tone_numbers=True)
    'wang4 na2 yi1xie1 dong1xi5 le5'
    # the spaces argument adds a space between each syllable
    >>> pinyin_jyutping_sentence.pinyin("忘拿一些东西了", tone_numbers=True, spaces=True)
    'wang4 na2 yi1 xie1 dong1 xi5 le5'
    >>> pinyin_jyutping_sentence.jyutping("有啲好貴", tone_numbers=True)
    'jau5 di1 hou3 gwai3'
    
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

Google Sheets add-on
--------------------

This library is available in the form of a Google Sheets Add-on. You can read about it here: https://medium.com/@lucw/converting-chinese-characters-to-pinyin-or-jyutping-on-google-sheets-eb12cca669cb

How it works
------------

Uses the Jieba library (https://github.com/fxsjy/jieba) to tokenize the sentence. Then words are converted to Pinyin/Jyutping either as a whole, or character by character, using the CC-Canto dictionary (http://cantonese.org/about.html). The Jyutping diacritic conversion is not standard but originally described here: http://www.cantonese.sheik.co.uk/phorum/read.php?1,127274,129006


