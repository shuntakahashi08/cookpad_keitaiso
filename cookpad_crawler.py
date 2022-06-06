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
#�����̌����L�[���[�h�����X�g�Ƃ��ĕۊǂ���

	
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
			#page���X�N���[������i�e�y�[�W�ɂ̓��V�s�̃^�C�g���ꗗ�����\���j
			html = urllib.request.urlopen('https://cookpad.com/search/{0}?page={1}'.format(searchWord_encode,strpage)).read() # html �擾
		
			root = lxml.html.fromstring(html.decode('utf-8',errors='replace'))
			strhtml = str(html.decode('utf-8','replace'))

			recipes = root.xpath("//span[@class='title font16']/a[@class='recipe-title font13 ']")
			#1�y�[�W�̃��V�s�^�C�g���ꗗ�̃����N���P�P���ǂ��ă��V�s�̒��g���擾����
			for recipe in recipes:
				#recipeNo=recipeNo+1
			
				bodyRes = urllib.request.urlopen('https://cookpad.com/'+recipe.get('href'))#���V�s�̃y�[�W���N���[�����O
				bodyHtml = bodyRes.read()
				#1�^�C�g�����̃��V�s���擾
				htmlTreeBody = lxml.html.fromstring(bodyHtml.decode('utf-8'))

				#���V�s�̃^�C�g�����擾
				titlepath = htmlTreeBody.xpath("//div[@id='recipe-title']")
				title =titlepath[0].text_content()
				title = keitaiso.wordAnalysis2(title)
				#print(title)
				ingredients = htmlTreeBody.xpath("//div[@class='ingredient_name']/span[@class='name']")#�@�{���y�[�W�̂Ȃ�����{���e�L�X�g�����X�N���C�s���O
				ingredient_text=''
				recipeVector=[]
			#	���V�s�̊e�s���P�P���o��
				for ingredient in ingredients:
				
					if ingredient.text_content()!=None:
						#yomiList,baseFormList = keitaiso.wordAnalysis(ingredient.text_content())
#						print(yomiList)
						ingredient_text += ' '+ingredient.text_content()
			
				indredient_words=keitaiso.tokenizer_customDic(ingredient_text)
				
				print('title:',title)
				ingred = ingredient_text.replace('�B','')
				print('recipe:',ingred,'\n')
								
				df = pd.DataFrame([[searchWord,ingredient_text,indredient_words,title]], columns=['label','text','words','others'])
				reciepe_df = reciepe_df.append(df)
	
	#�t�@�C���������Ȃ烌�R�[�h�ǉ��A�V�K�Ȃ�w�_�[�������o���Ă��烌�R�[�h�����o��
	#if os.path.isfile('cookpad_recipe.csv'):
	#	with codecs.open("cookpad_recipe.csv", "a", "ms932", "ignore") as cookpad_file:	
	#		reciepe_df.to_csv(cookpad_file, index=False, encoding="ms932", mode='a', header=False)
	#else:
	#	with codecs.open("cookpad_recipe.csv", "w", "ms932", "ignore") as cookpad_file:	
			#header=True�ŁA���o���������o��
	#		reciepe_df.to_csv(cookpad_file, index=False, encoding="ms932", mode='w', header=True)
		
	

except HTTPError as e:
	print(e)
except URLError as e:
	print("The server could not be found.")

finally:
	
	print("It Worked")
