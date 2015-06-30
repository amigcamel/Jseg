# Jseg
##A modified version of [Jieba](https://github.com/fxsjy/jieba")

### Synopsis

1. **Equipped with Emoticon detection**  
  Emoticons will not be segmented as sequences of meaningless punctuations.

2. **Data are trained with Sinica Corpus**  
  Results are more accurate when dealing with Traditional Chinese (F1-score = 0.91).

3. **Using Brill Tagger**  
  Training data are trained with Sinica Treebank, which raises the accuracy of POS tagging. 
  
### Environment
Python 3.4.3


### Installation

	pip install https://github.com/amigcamel/Jseg/archive/jseg3.zip



###Usage

	from jseg.jieba import Jieba
	j = Jieba()

Here's a sample text:


	sample = '期末要爆炸啦！ ◢▆▅▄▃崩╰(〒皿〒)╯潰▃▄▅▇◣'

Segmentation *with* part-of-speech

	result = j.seg(sample, pos=True)
	
Segmentation *without* part-of-speech

	result = j.seg(sample, pos=False)

###Add user defined dictionary

	j.add_guaranteed_wordlist(lst)
