from setuptools import setup

# build instructions
#  python3 setup.py sdist
# python3 setup.py sdist upload

setup(name='pinyin_jyutping_sentence',
      version='0.6',
      description='Convert a Chinese sentence to Pinyin or Jyutping',
      long_description=open('README.rst', encoding='utf-8').read(),
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