<h1>Jseg</h1>
<h2>A modified version of <a href="https://github.com/fxsjy/jieba">Jieba</a> segmentator</h2>

<h3>Synopsis</h3>
<ul>
  <li><strong>Equipped with Emoticon detection</strong></li>
      <p>Emoticons will not be segmented as sequences of meaningless punctuations.</p>
  <li><strong>Data are trained with Sinica Corpus</strong></li>
      <p>Results are more accurate when dealing with Traditional Chinese (F1-score = 0.91).</p>
  <li><strong>Using <a href="https://github.com/a33kuo/postagger_zh">Brill Tagger</strong></a></li>
      <p>Training data are trained with Sinica Treebank, which raises the accuracy of POS tagging. </p>
</ul>

<h3>Usage</h3>
```
from Jseg import jieba

```
Here's a sample text:
```
sample = '''台灣大學語言學研究所LOPE實驗室超強
            Taco門神超罩
            Amber 和 Emily 是雙胞胎
            Yvonne 不是小老鼠
            期末要爆炸啦！ ◢▆▅▄▃崩╰(〒皿〒)╯潰▃▄▅▇◣
         '''
```
Segmentation
```
result = jieba.seg(sample)
```
Print out:
```
print result.text()
```
And the result:
```
台灣/Nca 大學/Ncb 語言學/Nad 研究所/Ncb LOPE/FW 實驗室/Ncb 超強/VH11 
Taco/FW 門神/Nad 超罩/VH14 
Amber/FW 和/Caa Emily/FW 是/V_11 雙胞胎/DM 
Yvonne/FW 不/Dc 是/V_11 小老鼠/Nab 
期末/Ng 要/Dbab 爆炸/VH11 啦/Tc ！/PUNCTUATION ◢▆▅▄▃崩╰(〒皿〒)╯潰▃▄▅▇◣/EMOTICON 
```
You can print out the result with colored POS tagging:
```
print result.text(mode='color')
```
Print out without POS tagging:
```
print result.nopos()
```
Result:
```
台灣 大學 語言學 研究所 LOPE 實驗室 超強
Taco 門神 超罩
Amber 和 Emily 是 雙胞胎
Yvonne 不 是 小老鼠
期末 要 爆炸 啦 ！ ◢▆▅▄▃崩╰(〒皿〒)╯潰▃▄▅▇◣ 
```
