# -*- coding:shift-jis -*-
# coding: cp932

from urllib.request import urlopen
import json
from urllib.error import HTTPError
from urllib.error import URLError
import urllib.request
import urllib.parse
import urllib
import lxml.html
import keitaiso
import os.path
import pandas as pd
import codecs
#import crawler

try:
#複数の検索キーワードをリストとして保管する

	
	searchWord_list=[]
	while True:		
		
		searchWord = input("Please input a keyword:")
		if searchWord =='q':	
			break
		else:
			searchWord_list.append(searchWord)
			
			
	
	reciepe_df = pd.DataFrame([],columns=['label','text','words','others'])
	
		
	for searchWord in searchWord_list:	
		searchWord_encode = urllib.parse.quote(searchWord)
		page=0
		while page <21:
			strhtml =''		
			page = page +1
		
			print(page)
			strpage = str(page)	
			#pageをスクロールする（各ページにはレシピのタイトル一覧だけ表示）
			html = urllib.request.urlopen('https://cookpad.com/search/{0}?page={1}'.format(searchWord_encode,strpage)).read() # html 取得
		
			root = lxml.html.fromstring(html.decode('utf-8',errors='replace'))
			strhtml = str(html.decode('utf-8','replace'))

			recipes = root.xpath("//span[@class='title font16']/a[@class='recipe-title font13 ']")
			#1ページのレシピタイトル一覧のリンクを１つ１つたどってレシピの中身を取得する
			for recipe in recipes:
				#recipeNo=recipeNo+1
			
				bodyRes = urllib.request.urlopen('https://cookpad.com/'+recipe.get('href'))#レシピのページをクローリング
				bodyHtml = bodyRes.read()
				#1タイトル文のレシピを取得
				htmlTreeBody = lxml.html.fromstring(bodyHtml.decode('utf-8'))

				#レシピのタイトルを取得
				titlepath = htmlTreeBody.xpath("//div[@id='recipe-title']")
				title =titlepath[0].text_content()
				title = keitaiso.wordAnalysis2(title)
				#print(title)
				ingredients = htmlTreeBody.xpath("//div[@class='ingredient_name']/span[@class='name']")#　本文ページのなかから本文テキストだけスクレイピング
				ingredient_text=''
				recipeVector=[]
			#	レシピの各行を１つ１つ取り出す
				for ingredient in ingredients:
				
					if ingredient.text_content()!=None:
						#yomiList,baseFormList = keitaiso.wordAnalysis(ingredient.text_content())
#						print(yomiList)
						ingredient_text += ' '+ingredient.text_content()
			
				indredient_words=keitaiso.tokenizer_customDic(ingredient_text)
				
				print('title:',title)
				ingred = ingredient_text.replace('。','')
				print('recipe:',ingred,'\n')
								
				df = pd.DataFrame([[searchWord,ingredient_text,indredient_words,title]], columns=['label','text','words','others'])
				reciepe_df = reciepe_df.append(df)
	
	#ファイルが既存ならレコード追加、新規ならヘダーを書き出してからレコード書き出す
	#if os.path.isfile('cookpad_recipe.csv'):
	#	with codecs.open("cookpad_recipe.csv", "a", "ms932", "ignore") as cookpad_file:	
	#		reciepe_df.to_csv(cookpad_file, index=False, encoding="ms932", mode='a', header=False)
	#else:
	#	with codecs.open("cookpad_recipe.csv", "w", "ms932", "ignore") as cookpad_file:	
			#header=Trueで、見出しを書き出す
	#		reciepe_df.to_csv(cookpad_file, index=False, encoding="ms932", mode='w', header=True)
		
	

except HTTPError as e:
	print(e)
except URLError as e:
	print("The server could not be found.")

finally:
	
	print("It Worked")
