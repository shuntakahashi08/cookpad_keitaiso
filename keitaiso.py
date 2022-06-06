# -*- utf-8 -*-

from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
def tokenizer(sentence):

	surfaceList=[]
	partList=[]

	t = Tokenizer()
	for token in t.tokenize(sentence):
	
		surfaceList.append(token.surface)
		partList.append(token.part_of_speech.split(',')[0])
	
	return surfaceList,partList
		
def tokenizer_base(sentence):

	strBaseForm=''
	t = Tokenizer()
	word_vector = []
	for token in t.tokenize(sentence):
#		if (token.part_of_speech.split(',')[0] =='名詞') or (token.part_of_speech.split(',')[0] =='動詞') or (token.part_of_speech.split(',')[0] =='形容詞'):
		if token.part_of_speech.split(',')[0] =='名詞':
			word_vector += [token.base_form]
#		strBaseForm = strBaseForm + ',' + token.base_form
	
	return word_vector

def tokenizer_customDic(sentence):

	word_vector = ''
	#tokenizerメソッドの初期化（コンストラクタ）にユーザー辞書を指定することができる
	#ユーザー辞書は、.csvのままでもよいし、コンパイル済の辞書でもよい
	#csvを使う場合は、拡張子を付けること。
	#t=Tokenizer("User_Dict1")
	#t=Tokenizer("User_Dict1.csv", udic_enc="CP932")
	t=Tokenizer()
	filter_char=[]
	filter_token=[CompoundNounFilter(),POSKeepFilter(['名詞'])]

	#上のでインスタンス生成
	a=Analyzer(filter_char,t,filter_token)
	for token in a.analyze(sentence):
	
		
		
		if token.part_of_speech.split(',')[1] in ['複合']:
			t=0
			complex_base_form=''
			for token2 in Analyzer().analyze(token.surface):
				if '＊' in token2.reading:
				
					break
				elif 'ホットケーキ' or 'パンケーキ' or '（' or '）' in token2.surface:
					break
				
				else:
					complex_base_form+=token2.base_form
				t+=1
					
			if t<3 and complex_base_form!='':
				word_vector += complex_base_form + ','
                
		else:
			if 'ホットケーキ' in token.base_form:
				continue
			else:
				word_vector += token.base_form+ ','
		#print(token.base_form)
	return word_vector[:-1]

def word2yomi(word):

	t = Tokenizer()
	yomi=''
	for token in t.tokenize(word):
	
		if token.reading =='*':
			yomi+=token.surface
		else:
			yomi+=token.reading
	
	return yomi


def wordAnalysis2(sentence):
#	print(sentence)
	surface=''
	
	t = Tokenizer()
	for token in t.tokenize(sentence):
		if token.reading!='*':
			surface=surface+token.surface
		
	return surface
	
if __name__ == '__main__':

	import pandas as pd
	import codecs
	csv_input = pd.read_csv('cookpad_recipe.csv', encoding='ms932', sep=',',skiprows=0)
	reciepe_words_df = pd.DataFrame([],columns=['label','text','words'])
	
	for label, text in zip(csv_input['label'].values.tolist(),csv_input['text'].values.tolist()):
		#print(text)
		word_vector=tokenizer_customDic(text)
		if word_vector!='':
			
			df = pd.DataFrame([[label,text,word_vector]], columns=['label','text','words'])
			reciepe_words_df = reciepe_words_df.append(df)
	
	with codecs.open("cookpad_recipe_words.csv", "w", "ms932", "ignore") as cookpad_file:	
		#header=Trueで、見出しを書き出す
		reciepe_words_df.to_csv(cookpad_file, index=False, encoding="ms932", mode='w', header=True)
		