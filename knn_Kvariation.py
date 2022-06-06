import matplotlib.pyplot as plt
import mglearn
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

#データをX,yに取り込む　X（特徴量） y(教師ラベル）
X,y = mglearn.datasets.make_forge()
print(len(y))
#複数の図を定義する。()の意味はスライド参照 axesに図表番号が入る
fig, axes = plt.subplots(1,3,figsize=(10,3))

#Kの値リスト、図表番号リスト(axes)を1つづつ取り出しては図を1つ作成する
for n_neighbors, ax in zip([20,24,26],axes):
	#K最近傍法のクラスをインスタンス化
	knn= KNeighborsClassifier(n_neighbors=n_neighbors)
	#学習
	clf=knn.fit(X,y)
	#境界線を引く
	mglearn.plots.plot_2d_separator(clf,X,fill=True, eps=0.5,ax=ax, alpha=.4)
	#散布図を描画、X[:,0]はx軸に相当する特徴量（Xの1列目を取り出している）　X[:,1]はy軸特徴量
	#y（教師ラベル）の違いによって散布図のプロット記号を変えている
	#ax= で図表番号を指定
	mglearn.discrete_scatter(X[:,0],X[:,1],y,ax=ax)
	ax.set_title("{} neighbor(s)".format(n_neighbors))
	ax.set_xlabel("feature 0")
	ax.set_ylabel("feature 1")
axes[0].legend(loc=3)

plt.show()