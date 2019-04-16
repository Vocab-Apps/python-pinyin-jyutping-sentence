import re
import jieba
import unittest
import os

class RomanizationConversion():
    
    pinyin_tone_map = {
        0: "aoeiuv\u00fc",
        1: "\u0101\u014d\u0113\u012b\u016b\u01d6\u01d6",
        2: "\u00e1\u00f3\u00e9\u00ed\u00fa\u01d8\u01d8",
        3: "\u01ce\u01d2\u011b\u01d0\u01d4\u01da\u01da",
        4: "\u00e0\u00f2\u00e8\u00ec\u00f9\u01dc\u01dc",
    }    

    jyutping_tone_map = {
        'e':     {1: 'ē',
                  2: 'é',
                  3: 'ê',
                  4: 'è',
                  5: 'ě',
                  6: 'e'},
        'a':     {1: 'ā',
                  2: 'á',
                  3: 'â',
                  4: 'à',
                  5: 'ǎ',
                  6: 'a'},
        'i':     {1: 'ī',
                  2: 'í',
                  3: 'î',
                  4: 'ì',
                  5: 'ǐ',
                  6: 'i'},
        'o':     {1: 'ō',
                  2: 'ó',
                  3: 'ô',
                  4: 'ò',
                  5: 'ǒ',
                  6: 'o'},
        'u':     {1: 'ū',
                  2: 'ú',
                  3: 'û',
                  4: 'ù',
                  5: 'ǔ',
                  6: 'u'}
        }
    
    def __init__(self):
        self.jyutping_word_map = {}
        self.pinyin_word_map = {}
        self.jyutping_char_map = {}
        self.pinyin_char_map = {}


    def decode_pinyin(self, s):
        s = s.lower()
        r = ""
        t = ""
        for c in s:
            if c >= 'a' and c <= 'z':
                t += c
            elif c == ':':
                assert t[-1] == 'u'
                t = t[:-1] + "\u00fc"
            else:
                if c >= '0' and c <= '5':
                    tone = int(c) % 5
                    if tone != 0:
                        m = re.search("[aoeiuv\u00fc]+", t)
                        if m is None:
                            t += c
                        elif len(m.group(0)) == 1:
                            t = t[:m.start(0)] + RomanizationConversion.pinyin_tone_map[tone][RomanizationConversion.pinyin_tone_map[0].index(m.group(0))] + t[m.end(0):]
                        else:
                            if 'a' in t:
                                t = t.replace("a", RomanizationConversion.pinyin_tone_map[tone][0])
                            elif 'o' in t:
                                t = t.replace("o", RomanizationConversion.pinyin_tone_map[tone][1])
                            elif 'e' in t:
                                t = t.replace("e", RomanizationConversion.pinyin_tone_map[tone][2])
                            elif t.endswith("ui"):
                                t = t.replace("i", RomanizationConversion.pinyin_tone_map[tone][3])
                            elif t.endswith("iu"):
                                t = t.replace("u", RomanizationConversion.pinyin_tone_map[tone][4])
                            else:
                                t += "!"
                r += t
                t = ""
        r += t
        return r
        
        
    def jyutping_tone_character(self, char, tone):
        return RomanizationConversion.jyutping_tone_map[char][tone]
        

    def decode_jyutping(self, syllable):
        # extract tone
        m = re.search("([a-z]+)([0-9])", syllable)
        if m == None:
            print("couldn't parse syllable [%s]" % syllable)
            return syllable
        sound = m.group(1)
        tone = int(m.group(2))
            
        # find the first vowel in the sound
        index=0
        for char in sound:
            if char in ('a','e','i','o','u'):
                break
            index += 1
        
        if index >= len(sound):
            return sound
        
        # the index of the first vowel is in "index"
        sound_characters = list(sound)
        sound_characters[index] = self.jyutping_tone_character(sound_characters[index], tone)
        updated_sound = "".join(sound_characters)
        
        return updated_sound        
        
    def get_character_map(self, chinese, romanization):
        result = {}
        if len(romanization) > 0:
            romanization_tokens = romanization.split(" ")
            chinese = ''.join( c for c in chinese if  c not in ',， ' )
            chinese_characters = list(chinese)
            if len(romanization_tokens) == len(chinese_characters):
                for pair in zip(chinese_characters, romanization_tokens):
                    (char, rom) = pair
                    result[char] = rom
            else:
                #print("length doesn't match: {} - {}".format(romanization_tokens, chinese_characters))
                pass
        return result

    def get_token_map(self, chinese, romanization):
        result = {}
        if len(romanization) > 0:
            # remove unwanted characters
            romanization = ''.join( c for c in romanization if  c not in ',，' )
            chinese = ''.join( c for c in chinese if  c not in ',， ' )
            romanization_tokens = romanization.split(" ")
            chinese_characters = list(chinese)
            if len(romanization_tokens) == len(chinese_characters):
                #print(romanization_tokens)
                #print(chinese_characters)
                chinese_word_list = list(jieba.cut(chinese))
                chinese_index = 0
                for chinese_word in chinese_word_list:
                    equivalent_romanization_syllables = romanization_tokens[chinese_index:chinese_index+len(chinese_word)]
                    #print(chinese_word, equivalent_romanization_syllables)
                    result[chinese_word] = equivalent_romanization_syllables
                    chinese_index += len(chinese_word)
            else:
                #print("length doesn't match: {} - {}".format(romanization_tokens, chinese_characters))
                pass
        return result
        
    def process_line(self, line, jyutping_word_map, pinyin_word_map, jyutping_char_map, pinyin_char_map):
        m = re.match('([^\s]+)\s([^\s]+)\s\[([^\]]*)\]\s\{([^\}]+)\}\s.*', line)
        if m == None:
            print(line)
        traditional_chinese = m.group(1)
        simplified_chinese = m.group(2)
        pinyin = m.group(3)
        jyutping = m.group(4)
        
        
        # process full words with tokens
        jyutping_token_map = self.get_token_map(traditional_chinese, jyutping)
        pinyin_token_map = self.get_token_map(simplified_chinese, pinyin)
        jyutping_word_map.update(jyutping_token_map)
        pinyin_word_map.update(pinyin_token_map)
        
        # process character by character
        line_jyutping_char_map = self.get_character_map(traditional_chinese, jyutping)
        line_pinyin_char_map = self.get_character_map(simplified_chinese, pinyin)
        jyutping_char_map.update(line_jyutping_char_map)
        pinyin_char_map.update(line_pinyin_char_map)
        
    def process_file(self, filename):
        print("opening file {}".format(filename))
        with open(filename, 'r', encoding="utf8") as filehandle:
            for line in filehandle:
                first_char = line[:1]
                if first_char != '#' and line != "and add boilerplate:\n":
                    self.process_line(line,
                                      self.jyutping_word_map, 
                                      self.pinyin_word_map, 
                                      self.jyutping_char_map, 
                                      self.pinyin_char_map)
                    
                    
        
    def load_files(self):
        module_dir = os.path.dirname(__file__)
        filename = os.path.join(module_dir, "cccanto-webdist-160115.txt")
        self.process_file(filename)
        filename = os.path.join(module_dir, "cccedict-canto-readings-150923.txt")
        self.process_file(filename)
        
    def get_romanization(self, chinese, word_map, char_map, processing_function):
        # 1. see if the word in its entirety is present in the word map
        if chinese in word_map:
            romanization_tokens = word_map[chinese]
            processed_syllables = [processing_function(syllable) for syllable in romanization_tokens]
            return "".join(processed_syllables)
        # 2. if the word is not found, proceed character by character using the character map
        chinese_characters = list(chinese)
        result = []
        for char in chinese_characters:
            if char in char_map:
                syllable = char_map[char]
                processed_syllable = processing_function(syllable)
            else:
                processed_syllable = char
            result.append(processed_syllable)
        return "".join(result)        

    def process_sentence(self, sentence, word_map, character_map, processing_function):
        seg_list = jieba.cut(sentence)
        word_list = list(seg_list)
        #print(word_list)
        processed_words = [self.get_romanization(word, word_map, character_map, processing_function) for word in word_list]
        return " ".join(processed_words)

    def process_sentence_pinyin(self, sentence):
        return self.process_sentence(sentence, self.pinyin_word_map, self.pinyin_char_map, self.decode_pinyin)
    
    def process_sentence_jyutping(self, sentence):
        return self.process_sentence(sentence, self.jyutping_word_map, self.jyutping_char_map, self.decode_jyutping)
        
romanization_conversion = RomanizationConversion()
romanization_conversion.load_files()
pinyin = romanization_conversion.process_sentence_pinyin
jyutping = romanization_conversion.process_sentence_jyutping
        
class FileLoadTests(unittest.TestCase):
    def test_process_line_1(self):
        rc = RomanizationConversion()
        jyutping_word_map = {}
        pinyin_word_map = {}
        jyutping_char_map = {}
        pinyin_char_map = {}
        rc.process_line("一團 一团 [yi1 tuan2] {jat1 tyun4} /a group /", jyutping_word_map, pinyin_word_map, jyutping_char_map, pinyin_char_map)
        #print(jyutping_word_map, pinyin_word_map, jyutping_char_map, pinyin_char_map)
        
        expected_jyutping_word_map = {
            '一團': ["jat1", "tyun4"]
        }
        expected_pinyin_word_map = {
            '一团': ["yi1", "tuan2"]
        }
        expected_jyutping_char_map = {
            # '一團': ["jat1", "tyun4"]
            '一' : "jat1",
            '團' : "tyun4"
        }
        expected_pinyin_char_map = {
            #'一团': ["yi1", "tuan2"]
            '一' : "yi1",
            '团' : "tuan2"
        }
        self.assertEqual(expected_jyutping_word_map, jyutping_word_map)
        self.assertEqual(expected_pinyin_word_map, pinyin_word_map)
        self.assertEqual(expected_jyutping_char_map, jyutping_char_map)
        self.assertEqual(expected_pinyin_char_map, pinyin_char_map)
        
    def test_process_line_2(self):
        rc = RomanizationConversion()
        jyutping_word_map = {}
        pinyin_word_map = {}
        jyutping_char_map = {}
        pinyin_char_map = {}
        rc.process_line("野火燒不盡，春風吹又生 野火烧不尽，春风吹又生 [ye3 huo3 shao1 bu4 jin4 , chun1 feng1 chui1 you4 sheng1] {je5 fo2 siu1 bat1 zeon6 ，ceon1 fung1 ceoi1 jau6 sang1}\n", 
        jyutping_word_map, pinyin_word_map, jyutping_char_map, pinyin_char_map)
        self.assertEqual(jyutping_char_map['又'], "jau6")
        self.assertEqual(jyutping_word_map['又'], ["jau6"])

        
    def test_get_character_map(self):
        rc = RomanizationConversion()
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
        rc = RomanizationConversion()
        chinese = '没有什么'
        romanization = 'mei2 you3 shen2 me5'
        expected_result = { '没有': ['mei2', 'you3'],
                            '什么': ['shen2', 'me5']}
        actual_result = rc.get_token_map(chinese, romanization)
        self.assertEqual(actual_result, expected_result)
        #print(actual_result, expected_result)
        
    def test_get_token_map_2(self):
        rc = RomanizationConversion()
        chinese = '野火燒不盡，春風吹又生'
        romanization = 'je5 fo2 siu1 bat1 zeon6 ，ceon1 fung1 ceoi1 jau6 sang1'
        actual_result = rc.get_token_map(chinese, romanization)
        #print(actual_result)
        self.assertEqual(actual_result['又'], ["jau6"])
        self.assertEqual(actual_result['生'], ["sang1"])
        
    def test_decode_pinyin(self):
        rc = RomanizationConversion()
        source = 'ni3'
        expected_result = 'nǐ'
        actual_result = rc.decode_pinyin(source)
        self.assertEqual(actual_result, expected_result)
        
    def test_decode_jyutping(self):
        rc = RomanizationConversion()
        source = 'nei5'
        expected_result = 'něi'
        actual_result = rc.decode_jyutping(source)
        self.assertEqual(actual_result, expected_result)        
        
class EndToEndTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(EndToEndTests, cls).setUpClass()
        cls.rc = RomanizationConversion()
        cls.rc.load_files()

        
    def test_process_sentence_pinyin(self):
        
        source = '忘拿一些东西了'
        expected_result = 'wàng ná yīxiē dōngxi le'
        actual_result = self.rc.process_sentence_pinyin(source)
        self.assertEqual(actual_result, expected_result)
        
    def test_process_sentence_jyutping(self):
    
        source = '有啲好貴'
        expected_result = 'jǎu dī hóu gwâi'
        actual_result = self.rc.process_sentence_jyutping(source)
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
        '賣野食又唔係賺大錢': 'maai jěsik jau m hai zaan daaicín',
        '你想做，就照做': 'něi sóeng zou ， zauzîu zou'
        }
        
        for source, expected_result in expected_map.items():
            actual_result = self.rc.process_sentence_jyutping(source)
            self.assertEqual(expected_result, actual_result)        
        
if __name__ == '__main__':
    unittest.main()        
        