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
            '一' : "jat1",
            '團' : "tyun4",
            '团': 'tyun4'
        }
        expected_pinyin_char_map = {
            #'一团': ["yi1", "tuan2"]
            '一' : "yi1",
            '团' : "tuan2",
            '團' : "tuan2",
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
            '上': 'shang4',
            '蒼': 'cang1',
            '苍': 'cang1'
        }
        self.assertEqual(expected_pinyin_word_map, pinyin_word_map)
        self.assertEqual(expected_pinyin_char_map, pinyin_char_map)
        
    def test_get_character_map(self):
        rc = pinyin_jyutping_sentence.romanization_conversion
        chinese = "聰明一世，蠢鈍一時"
        romanization = "cung1 ming4 jat1 sai3 ceon2 deon6 jat1 si4"
        actual_result = rc.get_character_map(chinese, romanization)
        expected_result = {'一': 'jat1',
                             '世': 'sai3',
                             '明': 'ming4',
                             '時': 'si4',
                             '聰': 'cung1',
                             '蠢': 'ceon2',
                             '鈍': 'deon6'}
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
        actual_result = rc.decode_pinyin(source, False)
        self.assertEqual(actual_result, expected_result)

    def test_decode_pinyin_tone_numbers(self):
        rc = pinyin_jyutping_sentence.romanization_conversion
        source = 'ni3'
        expected_result = 'ni3'
        actual_result = rc.decode_pinyin(source, True)
        self.assertEqual(actual_result, expected_result)        
        
    def test_decode_jyutping(self):
        rc = pinyin_jyutping_sentence.romanization_conversion
        source = 'nei5'
        expected_result = 'něi'
        actual_result = rc.decode_jyutping(source, False)
        self.assertEqual(actual_result, expected_result)        

    def test_decode_jyutping_tone_numbers(self):
        rc = pinyin_jyutping_sentence.romanization_conversion
        source = 'nei5'
        expected_result = 'nei5'
        actual_result = rc.decode_jyutping(source, True)
        self.assertEqual(actual_result, expected_result)         
        
class EndToEndTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(EndToEndTests, cls).setUpClass()
        cls.rc = pinyin_jyutping_sentence.romanization_conversion
        cls.rc.load_files()

        
    def test_process_sentence_pinyin(self):
        
        source = '忘拿一些东西了'
        expected_result = 'wàng ná yīxiē dōngxi le'
        actual_result = self.rc.process_sentence_pinyin(source)
        self.assertEqual(actual_result, expected_result)

    def test_process_sentence_pinyin_tone_numbers(self):
        
        source = '忘拿一些东西了'
        expected_result = 'wang4 na2 yi1xie1 dong1xi5 le5'
        actual_result = self.rc.process_sentence_pinyin(source, tone_numbers=True)
        self.assertEqual(actual_result, expected_result)        

    def test_process_sentence_pinyin_tone_numbers_spacing(self):
        
        source = '忘拿一些东西了'
        expected_result = 'wang4 na2 yi1 xie1 dong1 xi5 le5'
        actual_result = self.rc.process_sentence_pinyin(source, tone_numbers=True, spaces=True)
        self.assertEqual(actual_result, expected_result)                
        
    def test_process_sentence_jyutping(self):
    
        source = '有啲好貴'
        expected_result = 'jǎu dī hôu gwâi'
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
        expected_result = 'jau5 di1 hou3 gwai3'
        actual_result = self.rc.process_sentence_jyutping(source, tone_numbers=True)
        self.assertEqual(actual_result, expected_result)

    def test_complete_pinyin(self):
    
        expected_map = {
        '提高口语': 'tígāo kǒuyǔ',
        '什么': 'shénme',        
        '音乐': 'yīnyuè'
        }
        
        for source, expected_result in expected_map.items():
            actual_result = self.rc.process_sentence_pinyin(source)
            self.assertEqual(expected_result, actual_result)
        
        
    def test_complete_jyutping(self):
        expected_map = {
        '全身按摩': 'cyùnsān ônmō',
        '我出去攞野食': 'ngǒ cēothêoi ló jěsik',
        '你揸車來㗎':'něi zàa cēlòi gâa',
        '賣野食又唔係賺大錢': 'maai jěsik jau m hai zaandaaicín',
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