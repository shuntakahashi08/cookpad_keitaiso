import numpy as np
import gensim
from gensim import corpora, models,matutils
from collections import defaultdict
from operator import itemgetter
import pandas as pd
import codecs

def making_dataset(csv_name,dict_name,corpus_name):

	#コーパスリスト中の各要素の順番は、元ネタの.csvの行の順番と同じになっている
	#csv.field_size_limit(100000000)
	
	csv_input = pd.read_csv(csv_name, encoding='ms932', sep=',',skiprows=0)
				
	#ユニーク化したラベルリスとを作る
	unique_label = csv_input['label'].unique()
	print('unique',unique_label)
	label_dict={}
	for label_id,label in enumerate(unique_label):
		
		#辞書に、ラベルテキストをキーとしてvalueにlabel_idを入れる
		label_dict[label] = label_id
	print(label_dict)
	label_id_list=[]
	
	for label_text in csv_input['label'].values.tolist():
		
		labelId = label_dict[label_text]		
		label_id_list.append(labelId)
		
	
	array_label_id = np.array(label_id_list)
	print(array_label_id)
	
	dict_word=[]	
	dictionary = gensim.corpora.Dictionary.load_from_text(dict_name)
	print('dictionary:',dictionary)
	for k, v in sorted(dictionary.items()):
		
		dict_word.append(v)
		
	dict_word.insert(0,'label')
	dict_word.insert(1,' ')
	dataset_df = pd.DataFrame([],columns=dict_word)
	
	corpus = corpora.MmCorpus(corpus_name)
	feature_matrix=[]
	for label_id,unit_corpus,words_vector in zip(array_label_id,corpus,csv_input[['words']].values.tolist()):
		
		feature_matrix.append(list(matutils.corpus2dense([unit_corpus], num_terms=len(dictionary)).T[0]))
		word_vec=list(matutils.corpus2dense([unit_corpus], num_terms=len(dictionary)).T[0])
		word_vec.insert(0,label_id)
		word_vec.insert(1,words_vector)
		#writer.writerow(word_vec)
		
		df = pd.DataFrame([word_vec], columns=dict_word)
		dataset_df = dataset_df.append(df)
		
	#多次元リストでも一気にnpに変換できる
	np_features = np.array(feature_matrix)
	print(np_features.shape)
	
	#dataframeのばあい、codecエラーは、pandasのto_csvでは解決できないので、別途import codecsにて
	#以下のようにファイルを一旦開く
	with codecs.open("dataset.csv", "w", "ms932", "ignore") as dataset:	
		
			dataset_df.to_csv(dataset, index=False, encoding="ms932", mode='w', header=True)
		
	
	return np_features,array_label_id,dict_word,label_dict

	
if __name__ == '__main__':

	feature_matrix,array_label_id,dict_word=making_dataset('cookpad_recipe.csv','cookpad.dict','cookpad_corpus.mm')
	#print(feature_matrix)
	print(array_label_id)
	print(dict_word)
	
