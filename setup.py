import distutils.core

version = '0.1'

distutils.core.setup(
    name='jseg',
    version=version,
    packages=['jseg'],
    author='Aji Liu',
    author_email='amigcamel@gmail.com',
    url='https://github.com/amigcamel/Jseg.git',
    # license='http://opensource.org/licenses/mit-license.php',
    description='A modified version of Jieba segmentator',
    package_data={'jseg': ['prob/*', 'dict.txt', 'emoall.txt', 'sinica_treebank_brill_aubt.pickle', 'ptt_encyc.txt']}
)
