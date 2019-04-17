from setuptools import setup

setup(name='pinyin_jyutping_sentence',
      version='0.1',
      description='Convert a Chinese sentence to Pinyin or Jyutping',
      url='https://github.com/lucwastiaux/python-pinyin-jyutping-sentence',
      author='Luc Wastiaux',
      author_email='lucw@airpost.net',
      classifiers=[
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing :: Linguistic',
      ],      
      license='GPL',
      packages=['pinyin_jyutping_sentence'],
      install_requires=[
          'jieba',
      ],      
      zip_safe=False,
      include_package_data=True)