#coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import math

def floor(x):
        return math.floor(x)

#coding=utf-8
if __name__=='__main__':
	matplotlib.use('WX')
	path=os.getcwd()
	print(path)
	path+='\Data_movie_3.xls'
	
	table=pd.ExcelFile(path).parse('sheet1')
	table.index_col='年份'
	grouped_year=table['评分'].groupby(table['年份'])
	plt.figure(1)
	print(grouped_year.mean())
	plt.plot(grouped_year.mean(),'r^--')
	plt.title(u'各年份电影的平均评分')
	plt.show()

	plt.figure(2)
	decades=(table['年份']-1900)/10
	decades=decades.apply(math.floor)
	grouped_decades=table['评分'].groupby(decades)
	print(grouped_decades.describe())
	x=grouped_decades.count()
	list_explode=[0.02]*len(grouped_decades)
	explode=tuple(list_explode)
	labels=list(grouped_decades.count().index)
	plt.pie(grouped_decades.count(),explode=explode,labels=labels,autopct = '%3.1f%%')
	plt.axis('equal')
	plt.title(u'各个年代的电影数')
	plt.show()
