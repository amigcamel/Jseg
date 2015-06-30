from setuptools import setup, find_packages


setup(
    name='jseg3',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'nltk==3.0.3'
    ],
    author='Aji Liu',
    author_email='amigcamel@gmail.com',
    description='''A modified version of Jieba''',
)
