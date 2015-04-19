import distutils.core

version = '0.1'

distutils.core.setup(
    name='Jseg',
    version=version,
    packages=['Jseg', 'POSTagger'],
    author='Aji Liu',
    author_email='i@jkey.lu',
    url='https://github.com/amigcamel/Jseg.git',
    # license='http://opensource.org/licenses/mit-license.php',
    description='A modified version of Jieba segmentator'
    )