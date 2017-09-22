"""Python setup settings."""
from setuptools import setup, find_packages

setup(
    name='jseg3',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'nltk==3.0.3'
    ],
    author='Aji Liu',
    author_email='amigcamel@gmail.com',
    description='''A modified version of Jieba''',
    package_data={
        'jseg': [
            'prob/*',
            'dict.txt',
            'emoall.txt',
            'brill_tagger.pkl'
        ]
    }
)
