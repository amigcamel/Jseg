# Jseg
## A modified version of Jieba

All credit goes to [fxsjy/jieba](https://github.com/fxsjy/jieba").  
Find more on: https://github.com/fxsjy/jieba


### Synopsis

1. **Equipped with Emoticon detection**  
  Emoticons will not be segmented as sequences of meaningless punctuations.

2. **Data are trained with Sinica Corpus**  
  Results are more accurate when dealing with Traditional Chinese (F1-score = 0.91).

3. **Using Brill Tagger**  
  Training data are trained with Sinica Treebank, which raises the accuracy of POS tagging.

### Environment
+ Python2.7+
+ Python3.3+


### Installation

	pip install -U jseg


### Usage

	from jseg import Jieba
	j = Jieba()

### Add user defined dictionary

  	j.add_guaranteed_wordlist(lst)


Here's a sample text:


	sample = '期末要爆炸啦！ ◢▆▅▄▃崩╰(〒皿〒)╯潰▃▄▅▇◣'

Segmentation *with* POS (part-of-speech)

	j.seg(sample, pos=True)
