# -*- coding: utf-8 -*-
"""AI for unknown protocol (未知協定).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xRNmD2JWIWFFc-bSPaEtRuMSeFDLQYoh
"""

! pip install pcapng

! pip install scapy

from scapy.all import *

traffic = rdpcap('/Users/user/Documents/資策會＿讀取檔案/44818_eth0_00001_20210325095818 (2).pcapng')

print (traffic)

unique_ip_address = []

for packet in traffic:
    src = packet[IP].src
    dst = packet[IP].dst
    
    unique_ip_address.append(src)
    unique_ip_address.append(dst)
    
print(set(unique_ip_address))

#unique IP Addresses 已取得所有封包

traffic[0]

traffic[0][IP].src

IP

traffic[0].payload

traffic[0].payload.len

traffic[2].payload.len

traffic[2].payload.id

traffic[2].payload.proto

traffic[0][IP].payload

print (traffic[0][IP].payload.load)
len(traffic[0][IP].payload.load)

len(traffic[2][IP].payload.load)

testBytes = traffic[2][IP].payload.load
byteArray = []
for i in  testBytes :
    byteArray.append(i)
    #byteArray[i] = testBytes[i]
print (byteArray)

len(traffic[197][IP].payload.load)
traffic[197][IP].len

len(traffic[0][IP].payload.load)

len(traffic[4][IP].payload.load)

traffic[4][IP].payload.load

traffic[4][IP].payload.load[0]

"""# 整理資料"""

rows = []

for i in traffic:
    
    testBytes = i[IP].payload.load
    byteArray = []
    for iii in  testBytes :
        byteArray.append(iii)
    
    len_ = i.payload.len
    LEN = len(i[IP].payload.load)
    byteArray = byteArray
    id_ = i.payload.id
    frag = i.payload.frag
    ttl = i.payload.ttl
    proto = i.payload.proto
    src =  i.payload.src
    dst =  i.payload.dst
    window = i.payload.window

    
    rows.append((len_,LEN,byteArray, id_,frag, ttl,proto, src,dst, window))
#print(rows)

#for i in rows:
    #print(i)

import pandas as pd

df = pd.DataFrame(rows, columns = ['len', 'LEN' ,'byteArray', 'id','frag','ttl','proto','src','dst', 'window'])

df['label'] = 0
pd.set_option('display.width', 10000)

#新增byte array 長度的array
len_list = []
for i in df['byteArray']:
    len_list.append(len(i))
print ("ALL LEN::::::: ",set(len_list))

#####
df_54 = df[df['LEN'] == 54] ##只拿54的
print("-----------")
print(df_54)

df_54.columns

len(list(range(54)))

for j in range(54):
    listj = []
    for  i in df_54['byteArray']:
        
        listj.append(i[j])
    df_54[str(j)] = listj
df_54

#捏出假資料
import numpy as np

df_fake = df_54.copy()

np.random.seed(6)

ran_1 = np.random.randint(0,255,2593)
ran_2 = np.random.randint(0,255,2593)

ran_3 = np.random.randint(0,255,2593)
ran_5 = np.random.randint(0,255,2593)
ran_7 = np.random.randint(0,255,2593)
ran_9 = np.random.randint(0,255,2593)
ran_11 = np.random.randint(0,255,2593)
ran_13 = np.random.randint(0,255,2593)

df_fake['1'] = ran_1
df_fake['3'] = ran_3
df_fake['5'] = ran_5
df_fake['7'] = ran_7
df_fake['9'] = ran_9
df_fake['11'] = ran_11
df_fake['13'] = ran_13

df_fake['label'] = 1

df_fake

frames = [df_54,df_fake]
result = pd.concat(frames)
result

#用統計方法 , 去看標準差
df_54.describe()

# 看位置跟位置之間的相關性 用相關係數
df_54.corr()

from sklearn.model_selection import  train_test_split

#切資料
X = result.drop(['label','src', 'dst', 'byteArray'], axis= 1)
y = result['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


#訓練兩份 一份input, 一份是答案
print(X_train.shape)
print(y_train.shape)

#測試兩份 一份input, 一份是答案
print(X_test.shape)
print(y_test.shape)


#測試的資料, 不能先看過, 會像是考古題
#機器會把他背起來

X_train.columns

from sklearn.tree import  DecisionTreeClassifier

#呼叫物件
dtree = DecisionTreeClassifier()

#訓練模型, 調參數
dtree.fit(X_train, y_train)

#進行預測
predictions = dtree.predict(X_test)

#衡量模型表現
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, predictions))

#視覺化
from sklearn import tree
text_representation = tree.export_text(dtree)
print(text_representation)

list(zip(X_train.columns, dtree.feature_importances_))

from sklearn.svm import SVC

#呼叫物件
model_svc = SVC()

#訓練模型, 調參數
model_svc.fit(X_train, y_train)

#進行預測
predictions = model_svc.predict(X_test)

#報錯原因, 只有一個類別

from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, predictions))

