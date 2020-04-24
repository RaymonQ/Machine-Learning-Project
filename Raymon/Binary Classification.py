import pandas as pd
# read data
path_project = "/Users/chengqian/Desktop/COMP9417-Group-Assignment/"
path_trainingData = path_project + '00_TaskHandout/training.csv'
path_testData = path_project + '00_TaskHandout/test.csv'

df = pd.read_csv(path_trainingData, sep=',')
df_test = pd.read_csv(path_testData, sep=',')

#TfIdf settings
from sklearn.feature_extraction.text import TfidfVectorizer as TfIdf
ngram_range = (1, 1)
min_df = 10
max_df = 1.
max_features = 300
sublinear_tf = True
tfidf_custom = TfIdf(ngram_range=ngram_range, max_df=max_df, min_df=min_df, max_features=max_features,
                     sublinear_tf=sublinear_tf)

#Create "relevance" label
def label_relevance (row):
   if row['topic'] == 'IRRELEVANT' :
      return '0'
   else:
      return '1'

#Add "relevance" label
df.apply (lambda row: label_relevance(row), axis=1)
df['relevance'] = df.apply (lambda row: label_relevance(row), axis=1)
df_test['relevance'] = df.apply (lambda row: label_relevance(row), axis=1)
X_train = tfidf_custom.fit_transform(df['article_words']).toarray()
X_test = tfidf_custom.fit_transform(df_test['article_words']).toarray()
y_train = df['relevance']
y_test = df_test['relevance']



# real test data
from sklearn.linear_model import LogisticRegression
logit_model = LogisticRegression()
# Fit model 
logit_model = logit_model.fit(X_train, y_train)

prediction = logit_model.predict(X_test)
# Confusion metrics
from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, prediction)
print(confusion_matrix)
# Results
from sklearn.metrics import classification_report
print(classification_report(y_test, prediction))


import numpy as np
np.count_nonzero(prediction=='0')



# test data generated from training data
#Split traing and test data
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X_train,y_train,test_size=0.20,random_state=0)
from sklearn.linear_model import LogisticRegression
logit_model = LogisticRegression()
# Fit model 
logit_model = logit_model.fit(X_train, y_train)

prediction = logit_model.predict(X_test)
# Confusion metrics
from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, prediction)
print(confusion_matrix)
# Results
from sklearn.metrics import classification_report
print(classification_report(y_test, prediction))

