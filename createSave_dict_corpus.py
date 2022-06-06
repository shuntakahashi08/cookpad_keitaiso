#csvのテキストを読み込んで、辞書とコーパスを生成する。
#辞書には、語彙別にユニークなidが自動的に付けられる
#コーパスもこのidで生成される
#いずれも、フォルダーに保存される。これらは、何回でもloadできる
#ユーザー辞書をつかった形態素解析は非常に時間がかかるので、
#保存するのは大変有効
import keitaiso
import gensim
from gensim import corpora, models
from collections import defaultdict
import pandas as pd

csv_input = pd.read_csv('cookpad_recipe_words.csv', encoding='ms932', sep=',',skiprows=0)
recipe_text_list=[]

for index, row in csv_input.iterrows():
    recipe_text_list.append(row['words'].split(','))


print(recipe_text_list)
# ------------------辞書生成---------------------------------------
#行列news_list_keitaiso（行が文書1単位）から辞書を生成（単語をユニーク化し、各単語に自動的にidを振る）
#機械学習では単語そのものでなく、idでコード化した語彙によって学習を行うため
dictionary = gensim.corpora.Dictionary(recipe_text_list)
print(dictionary)
#no_below=2で二回以下しか出現したい単語は無視します
#no_above=0.3で全部の文章の30パーセント以上に出現したワードは一般的すぎるワードとして無視します
#dictionary.filter_extremes(no_below=5, no_above=0.3)
dictionary.save_as_text('cookpad.dict')

# ----------------bag of word 生成および特徴量(TF, TF-iDF）生成
#上記辞書を参照しながら、形態素解析済の記事を文書単位毎にidを付与し、出現頻度を計算する
#corpusは、レシピテキスト1行分を要素とするリスト形式

corpus = [dictionary.doc2bow(recipe_morph) for recipe_morph in recipe_text_list]
#print(corpus)
gensim.corpora.MmCorpus.serialize('cookpad_corpus.mm', corpus)  



