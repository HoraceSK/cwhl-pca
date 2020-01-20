# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 14:51:19 2019

@author: 一介貂蝉
"""
import numpy as np
import pandas as pd
import xlrd
import xlwt
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']
from sklearn import preprocessing

#转换明细账为原始数据阵

dir=r'./GLofChewang2017.xlsx'
gl=pd.read_excel(dir,sheet_name='管理费用GL')


gl_good1=gl.loc[:,['具体科目','金额']]
gl_good2=gl_good1.drop(labels=['具体科目','金额'],axis=1,inplace=False)


names=gl.loc[:,'具体科目'].drop_duplicates()
na_list=names.reset_index(drop=True)
na_list=list(na_list)
gl_good2=pd.DataFrame(gl_good2,columns=na_list)

for i in na_list:
    a=gl_good1[gl_good1['具体科目']==i]
    gl_good2.loc[a.index,i]=a.loc[:,'金额']
print('原始数据阵的形状和金额合计：',gl_good2.shape,gl_good2.sum().sum())

good=gl_good2.fillna(0)

#聚类分析，将原始数据阵转换为聚类数据阵

import scipy
from scipy import cluster
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import *

a=scipy.spatial.distance.pdist(good.T, metric='minkowski')
z=linkage(a,method='ward')
f=dendrogram(z)
f=pd.Series(f)
lf=f['leaves']

li=list(lf)
li1=li[0:7:1]
li2=li[7::1]
g1=good.iloc[:,li1]
g2=good.iloc[:,li2]
print('验证将原始数据阵拆分为未聚类的g1和聚类的g2之和与原始数据阵金额总和是否相等：',g1.sum().sum()+g2.sum().sum())
oth_na=list(g2.columns)
print('g2中的科目合并为科目others：',oth_na)
g2.loc[:,'others']=g2.sum(axis=1)
oth=g2.loc[:,'others']
oth=list(oth)

g1.loc[:,'others']=oth
print('将合并科目others再合并到g1，得到聚类整理之后的数据阵g1的金额合计:',g1.sum().sum())
print(g1.head(3))

#主成分分析，找到管理费用异常波动的原因

sgm=g1.cov()
print('协方差矩阵：',sgm.shape)
tzz,tzxl=np.linalg.eigh(sgm)
tzxl=pd.DataFrame(tzxl)
tzz=pd.Series(tzz)
tzzsort=tzz.sort_values(ascending=False).round(6)

gxl=tzzsort/tzzsort.sum()
gxl_cu=gxl.cumsum()
gxl_cu=pd.DataFrame(gxl_cu,columns=['gxl_cu'])
tzz_se=tzzsort[gxl_cu[gxl_cu['gxl_cu']<0.92].index]
print('累计方差贡献率:',(tzz_se.cumsum()/tzzsort.sum()).round(3))
print('符合条件的特征值:',tzz_se.round(3))

tzxl_se=tzxl.iloc[:,tzz_se.index]
na=list(g1.columns)
tzxl_se.index=na

bdyy=tzxl_se.abs().idxmax(axis=0)
bdyy=pd.DataFrame(bdyy)
print('变动原因',bdyy)

data1=pd.read_excel(r'./ExpenseofCWHL2017.xlsx')
data1.set_index(['月份'],inplace=True)
print('验证金额是否相等：',data1.sum().sum(),gl['金额'].sum(),good.sum().sum())
data1_oth=data1.loc[:,oth_na]
data1_oth_sum=pd.DataFrame(data1_oth.sum(axis=1),columns=['others'],index=data1_oth.index)

#将分析结果可视化展示

bdyy1=list(bdyy[0])
print('展示如下变量的折线图',bdyy1)

data1_bdyy1=data1.loc[:,bdyy1]
if 'others' in bdyy1:
    data1_bdyy1.loc[:,'others']=data1_oth_sum.loc[:,'others']
fi=data1_bdyy1

fi.plot.line(legend=True,table=True,figsize=(14,6),use_index=True,grid=True,sort_columns=True)
fi.plot.box(legend=True,figsize=(14,6),use_index=True,grid=True,sort_columns=True)
fi.plot.hist(legend=True,figsize=(14,6),use_index=True,grid=True,sort_columns=True)

#————————————————
#版权声明：本文为CSDN博主「一介貂蝉Phantaska」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
#原文链接：https://blog.csdn.net/weixin_44588870/article/details/89462568
