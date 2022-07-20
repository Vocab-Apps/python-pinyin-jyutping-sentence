import logging
import pinyin_jyutping_sentence
import unittest

class FileLoadTests(unittest.TestCase):
    def test_process_line_1(self):
        rc = pinyin_jyutping_sentence.romanization_conversion
        jyutping_word_map = {}
        pinyin_word_map = {}
        jyutping_char_map = {}
        pinyin_char_map = {}
        rc.process_line("一團 一团 [yi1 tuan2] {jat1 tyun4} /a group /", jyutping_word_map, pinyin_word_map, jyutping_char_map, pinyin_char_map)
        #print(jyutping_word_map, pinyin_word_map, jyutping_char_map, pinyin_char_map)
        
        expected_jyutping_word_map = {
            '一團': ["jat1", "tyun4"],
            '一团': ['jat1', 'tyun4']
        }
        expected_pinyin_word_map = {
            '一团': ["yi1", "tuan2"],
            '一團': ['yi1', 'tuan2']
        }
        expected_jyutping_char_map = {
            # '一團': ["jat1", "tyun4"]
            '一' : {"jat1":2},
            '團' : {"tyun4":1},
            '团': {'tyun4':1}
        }
        expected_pinyin_char_map = {
            #'一团': ["yi1", "tuan2"]
            '一' : {"yi1":2},
            '团' : {"tuan2":1},
            '團' : {"tuan2":1},
        }
        self.assertEqual(expected_jyutping_word_map, jyutping_word_map)
        self.assertEqual(expected_pinyin_word_map, pinyin_word_map)
        self.assertEqual(expected_jyutping_char_map, jyutping_char_map)
        self.assertEqual(expected_pinyin_char_map, pinyin_char_map)
        

    def test_process_cedict_line_1(self):
        rc = pinyin_jyutping_sentence.romanization_conversion
        pinyin_word_map = {}
        pinyin_char_map = {}
        line = "上蒼 上苍 [shang4 cang1] /heaven/"
        rc.process_cedict_line(line, pinyin_word_map, pinyin_char_map)
        

        expected_pinyin_word_map = {
            '上蒼': ['shang4', 'cang1'],
            '上苍': ['shang4', 'cang1'],
        }
        expected_pinyin_char_map = {
            '上': {'shang4':2},
            '蒼': {'cang1':1},
            '苍': {'cang1':1}
        }
        self.assertEqual(expected_pinyin_word_map, pinyin_word_map)
        self.assertEqual(expected_pinyin_char_map, pinyin_char_map)
        
    def test_get_character_map(self):
        rc = pinyin_jyutping_sentence.romanization_conversion
        char_map = {}
        chinese = "聰明一世，蠢鈍一時"
        romanization = "cung1 ming4 jat1 sai3 ceon2 deon6 jat1 si4"
        rc.get_character_map(chinese, romanization, char_map)
        actual_result = char_map
        expected_result = {'一': {'jat1':2},
                             '世': {'sai3':1},
                             '明': {'ming4':1},
                             '時': {'si4':1},
                             '聰': {'cung1':1},
                             '蠢': {'ceon2':1},
                             '鈍': {'deon6':1}}
        self.assertEqual(expected_result, actual_result)
        
    def test_get_token_map_1(self):
        rc = pinyin_jyutping_sentence.romanization_conversion
        chinese = '没有什么'
        romanization = 'mei2 you3 shen2 me5'
        expected_result = { '没有': ['mei2', 'you3'],
                            '什么': ['shen2', 'me5']}
        actual_result = rc.get_token_map(chinese, romanization)
        self.assertEqual(actual_result, expected_result)
        #print(actual_result, expected_result)
        
        
    def test_decode_pinyin(self):
        rc = pinyin_jyutping_sentence.romanization_conversion
        source = 'ni3'
        expected_result = 'nǐ'
        actual_result = rc.decode_pinyin(source, False, False)
        self.assertEqual(actual_result, expected_result)

    def test_decode_pinyin_tone_numbers(self):
        rc = pinyin_jyutping_sentence.romanization_conversion
        source = 'ni3'
        expected_result = 'ni3'
        actual_result = rc.decode_pinyin(source, True, False)
        self.assertEqual(actual_result, expected_result)        

    def test_decode_pinyin_remove_tones(self):
        rc = pinyin_jyutping_sentence.romanization_conversion
        source = 'ni3'
        expected_result = 'ni'
        actual_result = rc.decode_pinyin(source, True, True)
        self.assertEqual(actual_result, expected_result)             
        
    def test_decode_jyutping(self):
        rc = pinyin_jyutping_sentence.romanization_conversion
        source = 'nei5'
        expected_result = 'něi'
        actual_result = rc.decode_jyutping(source, False, False)
        self.assertEqual(actual_result, expected_result)        

    def test_decode_jyutping_tone_numbers(self):
        rc = pinyin_jyutping_sentence.romanization_conversion
        source = 'nei5'
        expected_result = 'nei5'
        actual_result = rc.decode_jyutping(source, True, False)
        self.assertEqual(actual_result, expected_result)  
        
class EndToEndTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(EndToEndTests, cls).setUpClass()
        cls.rc = pinyin_jyutping_sentence.romanization_conversion
        cls.rc.load_files()

        
    def test_process_sentence_pinyin(self):
        # pytest test_conversion.py::EndToEndTests::test_process_sentence_pinyin -s -rPP
        
        source = '忘拿一些东西了'
        expected_result = 'wàng ná yīxiē dōngxi le'
        actual_result = self.rc.process_sentence_pinyin(source)
        self.assertEqual(actual_result, expected_result)

    def test_process_sentence_pinyin_tone_numbers(self):
        
        source = '忘拿一些东西了'
        expected_result = 'wang4 na2 yi1xie1 dong1xi5 le5'
        actual_result = self.rc.process_sentence_pinyin(source, tone_numbers=True)
        self.assertEqual(actual_result, expected_result)

    def test_process_sentence_pinyin_remove_tones(self):
        
        source = '忘拿一些东西了'
        expected_result = 'wang na yixie dongxi le'
        actual_result = self.rc.process_sentence_pinyin(source, remove_tones=True)
        self.assertEqual(actual_result, expected_result)

    def test_process_sentence_pinyin_tone_numbers_spacing(self):
        
        source = '忘拿一些东西了'
        expected_result = 'wang4 na2 yi1 xie1 dong1 xi5 le5'
        actual_result = self.rc.process_sentence_pinyin(source, tone_numbers=True, spaces=True)
        self.assertEqual(actual_result, expected_result)                
        
    def test_process_sentence_jyutping(self):
    
        source = '有啲好貴'
        expected_result = 'jǎu dī hóu gwâi'
        actual_result = self.rc.process_sentence_jyutping(source)
        self.assertEqual(actual_result, expected_result)

    def test_process_sentence_jyutping_spaces(self):
    
        # '全身按摩': 'cyùnsān ônmō',
        source = '全身按摩'
        expected_result = 'cyùn sān ôn mō'
        actual_result = self.rc.process_sentence_jyutping(source, spaces=True)
        self.assertEqual(actual_result, expected_result)        
        
    def test_process_sentence_jyutping_tone_numbers(self):
    
        source = '有啲好貴'
        expected_result = 'jau5 di1 hou2 gwai3'
        actual_result = self.rc.process_sentence_jyutping(source, tone_numbers=True)
        self.assertEqual(actual_result, expected_result)

    def test_complete_pinyin(self):
    
        expected_map = {
        '提高口语': 'tígāo kǒuyǔ',
        '什么': 'shénme',        
        '音乐': 'yīnyuè',
        '胡同': 'hútòng',
        # should work after character-pinyin frequency update
        '瓶盖': 'pínggài',
        '宝贝儿': 'bǎobèir',
        '在哪儿呢？': 'zài nǎr ne ？',

        # still broken
        # '电子乐': 'diànzǐ yuè',

        # set of characters which were missing at some point
        '闫': 'yán',
        # not sure how to handle alternate pronunciation
        #'晟': 'chéng',
        '卞': 'biàn',
        '垚': 'yáo',
        '濛': 'méng',
        '玥': 'yuè',
        # not found in any dictionaries
        #'㛤': 'lí',
        '潀': 'cóng',
        '谌': 'chén',
        '赟': 'yūn',
        '崚': 'léng',
        '骐': 'qí',
        # cedict doesn't agree with this pinyin
        #'珩': 'háng',
        '崧': 'sōng',
        '汭': 'ruì',
        '邬': 'wū',
        '镤': 'pú',
        '靳': 'jìn',

        # still broken
        #'將': 'jiāng',
        '痠': 'suān',
        '谁': 'shéi',
        '吗': 'ma',
        '呢': 'ne',

        }
        
        for source, expected_result in expected_map.items():
            actual_result = self.rc.process_sentence_pinyin(source)
            self.assertEqual(expected_result, actual_result)
        
        
    def test_complete_jyutping(self):
        expected_map = {
        '全身按摩': 'cyùnsān ônmō',
        '我出去攞野食': 'ngǒ cēothêoi ló jěsik',
        # seems the char frequency change broke this example
        #'你揸車來㗎':'něi zàa cēlòi gâa',
        '賣野食又唔係賺大錢': 'maai jěsik jau m hai zaan daaicín',
        '你想做，就照做': 'něi sóeng zou ， zauzîu zou'
        }
        
        for source, expected_result in expected_map.items():
            actual_result = self.rc.process_sentence_jyutping(source)
            self.assertEqual(expected_result, actual_result)        

    def test_traditional_mandarin(self):
        expected_map = {
        '請問，你叫什麼名字？': 'qǐngwèn ， nǐ jiào shénme míngzì ？',
        '上課': 'shàngkè',
        '糾結': 'jiūjié',
        }
        
        for source, expected_result in expected_map.items():
            actual_result = self.rc.process_sentence_pinyin(source)
            self.assertEqual(expected_result, actual_result)        

        
    def test_problematic_pinin(self):
        # how to debug a single character:
        # python
        # import pinyin_jyutping_sentence
        # pinyin_jyutping_sentence.romanization_conversion.pinyin_char_map['了']
        expected_map = {
            '好': 'hao3',
            '我很好': 'wo3 hen3 hao3',
        }
        
        for source, expected_result in expected_map.items():
            actual_result = self.rc.process_sentence_pinyin(source, tone_numbers=True)
            self.assertEqual(expected_result, actual_result)
