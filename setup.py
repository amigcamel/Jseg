"""Python setup settings."""
from setuptools import setup, find_packages

setup(
    name='jseg',
    version='0.0.4',
    packages=find_packages(),
    install_requires=[
        'nltk==3.0.3',
        'six==1.11.0',
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
