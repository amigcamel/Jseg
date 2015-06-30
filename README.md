# Jseg
##A modified version of [Jieba](https://github.com/fxsjy/jieba")

### Synopsis

1. **Equipped with Emoticon detection**  
  Emoticons will not be segmented as sequences of meaningless punctuations.

2. **Data are trained with Sinica Corpus**  
  Results are more accurate when dealing with Traditional Chinese (F1-score = 0.91).

3. **Using Brill Tagger**  
  Training data are trained with Sinica Treebank, which raises the accuracy of POS tagging. 

### Installation

	(sudo) pip install git+https://github.com/amigcamel/Jseg.git



###Usage

	from jseg.jieba import Jieba
	jieba = Jieba()

Here's a sample text:


	sample = '期末要爆炸啦！ ◢▆▅▄▃崩╰(〒皿〒)╯潰▃▄▅▇◣'

Segmentation


	result = jieba.seg(sample)

Print out:

	print result.text()

And the result:


	期末/Ng 要/Dbab 爆炸/VH11 啦/Tc ！/PUNCTUATION ◢▆▅▄▃崩╰(〒皿〒)╯潰▃▄▅▇◣/EMOTICON 


You can print out the result with colored POS tagging:

	print result.text(mode='color')

Print out without POS tagging:

	print result.nopos()

Result:

	期末 要 爆炸 啦 ！ ◢▆▅▄▃崩╰(〒皿〒)╯潰▃▄▅▇◣ 

If you want the result to be in a list, set ```mode``` to ```list```:

	result.nopos(mode='list')


###Add user defined dictionary

	jieba.add_guaranteed_wordlist(lst)

`lst` should bebe a list of unicodes, e.g., ['蟹老闆', '張他口', '劉阿吉']
