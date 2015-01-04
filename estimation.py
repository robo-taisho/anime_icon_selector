#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import codecs
import tweetmecab
import username
from gensim import corpora,matutils
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn import svm


DICTIONARY_FILE_NAME = 'twitdic.txt'

dictionary = corpora.Dictionary.load_from_text(DICTIONARY_FILE_NAME)

data_train = []

def dense_calc(words):
    tmp = dictionary.doc2bow(words)
    dense = list(matutils.corpus2dense([tmp], num_terms=len(dictionary)).T[0])
    return dense

def dense_list_make(user_name):
    dense_list = []
    for i in range(0,len(user_name)):
        user_name_tmp = user_name[i]
        words = tweetmecab.main(user_name_tmp)
        dense_list.append(dense_calc(words))
    return dense_list



user_name = username.user_name
os.chdir('usertweet')
data_train = dense_list_make(user_name)

label_train = username.label_train

data_train_s, data_test_s, label_train_s, label_test_s,user_name_train,user_name_test = train_test_split(data_train, label_train,user_name, test_size=0.3)




#以下はestimatorの設定、かなりぐちゃっている
#結局、coefがあるのはSVCだけなのでSVCを採用

"""
estimator = RandomForestClassifier()
"""

#estimator = LinearSVC(C=1.0)
"""
estimator = svm.SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, degree=3,gamma=0.001, kernel="linear", max_iter=-1, probability=False,random_state=None, shrinking=True, tol=0.001, verbose=False)
"""

estimator = svm.SVC(C=1,kernel="linear",probability=True)

estimator.fit(data_train_s, label_train_s)


"""教師データでテストする用
label_tested = estimator.predict(data_train)
print(label_tested)
"""

#手動でテストしたいときはここの中身を使う

"""

data_test_s = ['robo_taisho','ageh4c']
user_name_test = data_test_s
data_test_s = dense_list_make(data_test_s)
label_test_s = [0,1]
#
"""


label_predict = estimator.predict(data_test_s)
label_predict2 = estimator.predict_proba(data_test_s)

#print data_test_s


os.chdir('../.')


coef = estimator.coef_


""" coefを出力し、単語ごとの重要度を調べる。配列はdictionaryの一番から対応している。
#print coef[0,1]
alist = []
f = open("output_coef.txt","w")


for i in range(0,7528):
    alist.append(coef[0,i])
    outp = alist[i]
    f.write(str(outp) + "\n")

#print alist

#coef.tofile("coef.text",sep=",", format="%s")


####data_testの内容（単語の出現数）をアウトプットしたいのだがうまく表示できず断念
#import pickle
#f = open("pickle.dump", "w")
#pickle.dump(data_test_s, f)
#f.close()

"""


print("==== coef出力")
print coef

print("==== テストデータとなったユーザー名")
print user_name_test

print("==== 予想ラベル")
print(label_predict)

print("==== 正解ラベル")
print(label_test_s)

print("==== 各ラベルごとの確率")
print(label_predict2)

print("==== 正誤マトリックス、左上は非アニメ、右上は誤ってアニメアイコンに分類したもの、左下は誤って非アニメアイコンに分類したもの、右下はアニメアイコン")
print confusion_matrix(label_test_s, label_predict)

print("==== 正答率")
print(estimator.score(data_test_s, label_test_s))

target_names = ['notanime', 'anime']
print (classification_report(label_test_s, label_predict, target_names=target_names))



"""以下はグリッドサーチ用だが、重すぎる上に特にサーチする必要ないので一旦凍結
#グリッドサーチ重すぎ！
#tuned_parameters = [{'n_estimators': [10, 30, 50, 70, 90, 110, 130, 150], 'max_features': ['auto', 'sqrt', 'log2', None]}]

tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                    'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]


#tuned_parameters = [{'kernel': ['linear'], 'C': [1]}]
    
clf = GridSearchCV(svm.SVC(C=1), tuned_parameters, n_jobs=-1)
clf.fit(data_train_s, label_train_s)
    
print("==== グリッドサーチ")
print("  ベストパラメタ")
print(clf.best_estimator_)


print("トレーニングデータでCVした時の平均スコア")
for params, mean_score, all_scores in clf.grid_scores_:
    print("{:.3f} (+/- {:.3f}) for {}".format(mean_score, all_scores.std() / 2, params))
    
y_true, y_pred = label_test_s, clf.predict(data_test_s)
print(classification_report(y_true, y_pred))
"""




