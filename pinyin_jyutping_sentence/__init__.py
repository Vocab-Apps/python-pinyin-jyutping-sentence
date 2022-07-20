import re
import jieba
import logging
import os
import json

logger = logging.getLogger(__name__)

class ConversionData():
    DATA_CACHE_FILENAME = 'mandarin_cantonese_data.json'

    def __init__(self):
        self.jyutping_word_map = {}
        self.pinyin_word_map = {}
        self.jyutping_char_map = {}
        self.pinyin_char_map = {}

    def get_cache_file_path(self):
        module_dir = os.path.dirname(__file__)
        cache_file_path = os.path.join(module_dir, self.DATA_CACHE_FILENAME)
        return cache_file_path

    def cache_file_present(self):
        return os.path.isfile(self.get_cache_file_path())

    def serialize(self):
        data = {
            'jyutping_word_map': self.jyutping_word_map,
            'pinyin_word_map': self.pinyin_word_map,
            'jyutping_char_map': self.jyutping_char_map,
            'pinyin_char_map': self.pinyin_char_map
        }
        with open(self.get_cache_file_path(), 'w') as outfile:
            json.dump(data, outfile)

    def deserialize(self):
        with open(self.get_cache_file_path(), 'r') as input_file:
            data = json.load(input_file)  
            self.jyutping_word_map = data['jyutping_word_map']
            self.pinyin_word_map = data['pinyin_word_map']
            self.jyutping_char_map = data['jyutping_char_map']
            self.pinyin_char_map = data['pinyin_char_map']


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
        self.conversion_data = ConversionData()

    def decode_pinyin(self, s, tone_numbers, remove_tones):
        if remove_tones:
            return ''.join(i for i in s if not i.isdigit())
        if tone_numbers:
            return s
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
        

    def decode_jyutping(self, syllable, tone_numbers, remove_tones):
        if remove_tones:
            return ''.join(i for i in s if not i.isdigit())        
        if tone_numbers:
            return syllable
        # extract tone
        m = re.search("([a-z]+)([0-9])", syllable)
        if m == None:
            logger.info("couldn't parse syllable [%s]", syllable)
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
        
    # merge onto existing charmap
    def get_character_map(self, chinese, romanization, char_map):
        result = {}
        if len(romanization) > 0:
            romanization_tokens = romanization.split(" ")
            chinese = ''.join( c for c in chinese if  c not in ',， ' )
            chinese_characters = list(chinese)
            if len(romanization_tokens) == len(chinese_characters):
                for pair in zip(chinese_characters, romanization_tokens):
                    (char, rom) = pair
                    rom = rom.lower() # lowercase all romanizations
                    if char not in char_map:
                        # this character was never seen before, new entry
                        char_map[char] = {rom: 1}
                    else:
                        # this character has been seen before
                        if rom in char_map[char]:
                            # this romanization has been seen before
                            # increment by one
                            char_map[char][rom] += 1
                        else:
                            # new pronunciation for this character
                            char_map[char][rom] = 1
            else:
                #print("length doesn't match: {} - {}".format(romanization_tokens, chinese_characters))
                pass

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
            logger.info(line)
        traditional_chinese = m.group(1)
        simplified_chinese = m.group(2)
        pinyin = m.group(3)
        jyutping = m.group(4)
        
        
        # process full words with tokens
        # ==============================

        # jyutping, process both traditional and simplified
        # -------------------------------------------------

        jyutping_traditional_token_map = self.get_token_map(traditional_chinese, jyutping)
        jyutping_simplified_token_map = self.get_token_map(simplified_chinese, jyutping)
        jyutping_word_map.update(jyutping_traditional_token_map)
        jyutping_word_map.update(jyutping_simplified_token_map)

        # pinyin, process both traditional and simplified
        # -----------------------------------------------

        pinyin_simplified_token_map = self.get_token_map(simplified_chinese, pinyin)
        pinyin_traditional_token_map = self.get_token_map(traditional_chinese, pinyin)
        
        pinyin_word_map.update(pinyin_simplified_token_map)
        pinyin_word_map.update(pinyin_traditional_token_map)
        
        # process character by character
        # ==============================

        # jyutping
        # --------

        self.get_character_map(traditional_chinese, jyutping, jyutping_char_map)
        self.get_character_map(simplified_chinese, jyutping, jyutping_char_map)

        # pinyin
        # ------

        self.get_character_map(simplified_chinese, pinyin, pinyin_char_map)
        self.get_character_map(traditional_chinese, pinyin, pinyin_char_map)


    def process_cedict_line(self, line, pinyin_word_map, pinyin_char_map):
        m = re.match('([^\s]+)\s([^\s]+)\s\[([^\]]*)\]\s\/([^\/]+)\/.*', line)
        if m == None:
            logger.info(line)
        traditional_chinese = m.group(1)
        simplified_chinese = m.group(2)
        pinyin = m.group(3)
        definition = m.group(4)        
        
        # process full words with tokens
        # ==============================

        # pinyin, process both traditional and simplified
        # -----------------------------------------------

        pinyin_simplified_token_map = self.get_token_map(simplified_chinese, pinyin)
        pinyin_traditional_token_map = self.get_token_map(traditional_chinese, pinyin)
        
        pinyin_word_map.update(pinyin_simplified_token_map)
        pinyin_word_map.update(pinyin_traditional_token_map)
        
        # process character by character
        # ==============================

        # pinyin
        # ------

        self.get_character_map(simplified_chinese, pinyin, pinyin_char_map)
        self.get_character_map(traditional_chinese, pinyin, pinyin_char_map)

        
    def process_file(self, filename):
        logger.info("opening file %s", filename)
        with open(filename, 'r', encoding="utf8") as filehandle:
            for line in filehandle:
                first_char = line[:1]
                if first_char != '#' and line != "and add boilerplate:\n":
                    self.process_line(line,
                                      self.conversion_data.jyutping_word_map, 
                                      self.conversion_data.pinyin_word_map, 
                                      self.conversion_data.jyutping_char_map, 
                                      self.conversion_data.pinyin_char_map)
                    
    def process_cedict_file(self, filename):
        logger.info("opening file %s", filename)
        with open(filename, 'r', encoding="utf8") as filehandle:
            for line in filehandle:
                first_char = line[:1]
                if first_char != '#':
                    self.process_cedict_line(line,
                                            self.conversion_data.pinyin_word_map, 
                                            self.conversion_data.pinyin_char_map)
        
    def load_files(self):
        if self.conversion_data.cache_file_present():
            logger.debug('loading cached data')
            self.conversion_data.deserialize()
        else:
            module_dir = os.path.dirname(__file__)
            
            logger.debug('START loading jieba with dict.txt.big')
            jieba_big_dictionary_filename = os.path.join(module_dir, "dict.txt.big")
            jieba.set_dictionary(jieba_big_dictionary_filename)
            logger.debug('DONE loading jieba with dict.txt.big')
            
            filename = os.path.join(module_dir, "cccanto-webdist-160115.txt")
            logger.debug(f'START processing {filename}')
            self.process_file(filename)
            logger.debug(f'DONE processing {filename}')

            filename = os.path.join(module_dir, "cccedict-canto-readings-150923.txt")
            logger.debug(f'START processing {filename}')
            self.process_file(filename)
            logger.debug(f'DONE processing {filename}')
            # pinyin only
            filename = os.path.join(module_dir, "cedict_1_0_ts_utf-8_mdbg.txt")
            logger.debug(f'START processing {filename}')
            self.process_cedict_file(filename)
            logger.debug(f'DONE processing {filename}')

        
    def get_romanization(self, chinese, word_map, char_map, processing_function, tone_numbers, spaces, remove_tones):
        logger.debug(f'get_romanization: [{chinese}] tone_numbers: {tone_numbers} spaces: {spaces} remove_tones: {remove_tones}')
        spacing = ""
        if spaces == True:
            # add space between every character
            spacing = " "
        # 1. see if the word in its entirety is present in the word map (but only if it's not a single character)
        if len(chinese) > 1 and chinese in word_map:
            logger.debug(f'processing {chinese} as word')
            romanization_tokens = word_map[chinese]
            processed_syllables = [processing_function(syllable, tone_numbers, remove_tones) for syllable in romanization_tokens]
            result = spacing.join(processed_syllables)
            logger.debug(f'word processing result: {result}')
            return result
        # 2. if the word is not found, proceed character by character using the character map
        chinese_characters = list(chinese)
        logger.debug(f'processing character by character {chinese_characters}')
        result = []
        for char in chinese_characters:
            if char in char_map:
                romanizations = []
                for k, v in char_map[char].items():
                    romanizations.append({'rom': k, 'count': v})
                romanizations = sorted(romanizations, key=lambda entry: entry['count'], reverse=True)
                logger.debug(f'romanizations: {romanizations}')
                syllable = romanizations[0]['rom']
                processed_syllable = processing_function(syllable, tone_numbers, remove_tones)
            else:
                processed_syllable = char
            result.append(processed_syllable)
        return spacing.join(result)        

    def process_sentence(self, sentence, word_map, character_map, processing_function, tone_numbers, spaces, remove_tones):
        logger.debug(f'process_sentence [{sentence}]')
        seg_list = jieba.cut(sentence)
        word_list = list(seg_list)
        logger.debug(f'word_list: {word_list}')
        #print(word_list)
        processed_words = [self.get_romanization(word, word_map, character_map, processing_function, tone_numbers, spaces, remove_tones) for word in word_list]
        logger.debug(f'processed_words: {processed_words}')
        return " ".join(processed_words)

    def process_sentence_pinyin(self, sentence, tone_numbers=False, spaces=False, remove_tones=False):
        return self.process_sentence(sentence, self.conversion_data.pinyin_word_map, self.conversion_data.pinyin_char_map, self.decode_pinyin, tone_numbers, spaces, remove_tones)
    
    def process_sentence_jyutping(self, sentence, tone_numbers=False, spaces=False, remove_tones=False):
        return self.process_sentence(sentence, self.conversion_data.jyutping_word_map, self.conversion_data.jyutping_char_map, self.decode_jyutping, tone_numbers, spaces, remove_tones)
        
romanization_conversion = RomanizationConversion()
romanization_conversion.load_files()
pinyin = romanization_conversion.process_sentence_pinyin
jyutping = romanization_conversion.process_sentence_jyutping
        
