from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import keitaiso
import create_dataset
import gensim
from gensim import corpora, models,matutils

feature_matrix,array_label_id,dict_word,label_dict=create_dataset.making_dataset('cookpad_recipe_words.csv','cookpad.dict','cookpad_corpus.mm')

#教師ラベルと特徴量行列を訓練データとテストデータに75:25の割合で分離
X_train,X_test,Y_train,Y_test = train_test_split(feature_matrix,array_label_id,random_state=0)


training_accuracy=[]
test_accuracy=[]

#Kの値を1-24にセットする
neighbors_settings = range(1,25)

for n_neighbors in neighbors_settings:
	#KNNクラスをK=n_neighborsでインスタンス化
    clf=KNeighborsClassifier(n_neighbors=n_neighbors)
	#訓練データで学習
    clf.fit(X_train,Y_train)
	#訓練データによる当てはまり精度を計算
    training_accuracy.append(clf.score(X_train,Y_train))
	#テストデータによる予測精度を計算
    test_accuracy.append(clf.score(X_test, Y_test))

#x軸をKとして、訓練データ当てはまり精度、テストデータ予測精度をグラフ表示
plt.plot(neighbors_settings,training_accuracy,label="training accuracy")
plt.plot(neighbors_settings, test_accuracy, label="test accuracy")
plt.ylabel("Accuracy")
plt.xlabel("n_neighbors")
plt.legend()
plt.show()
