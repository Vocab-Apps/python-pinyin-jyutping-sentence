import pinyin_jyutping_sentence

def build_file_cache():
    pinyin_jyutping_sentence.romanization_conversion.conversion_data.serialize()

if __name__ == '__main__':
    build_file_cache()