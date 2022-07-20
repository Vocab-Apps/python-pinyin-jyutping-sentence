from setuptools import setup
from setuptools.command.install import install

# build instructions
#  python3 setup.py sdist
# python3 setup.py sdist upload


def post_installation():
    import pinyin_jyutping_sentence
    pinyin_jyutping_sentence.romanization_conversion.conversion_data.serialize()


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        post_installation()

setup(name='pinyin_jyutping_sentence',
      version='1.2',
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
      cmdclass={
          'install': PostInstallCommand
      },      
      zip_safe=False,
      include_package_data=True)