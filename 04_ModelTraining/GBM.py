import pickle
from sklearn.ensemble import GradientBoostingClassifier as Gbc
from sklearn.metrics import accuracy_score

# specify your directory where the project is here
# path Yannick:
path_project = "/Users/yannickschnider/PycharmProjects/COMP9417-Group-Assignment/"

# importing objects from folder data in feature engineering
path_data = path_project + '03_FeatureEngineering/Data/'

with open(path_data + 'df_train.pickle', 'rb') as data:
    df_train = pickle.load(data)
with open(path_data + 'df_test.pickle', 'rb') as data:
    df_test = pickle.load(data)
with open(path_data + 'features_train.pickle', 'rb') as data:
    features_train = pickle.load(data)
with open(path_data + 'features_test.pickle', 'rb') as data:
    features_test = pickle.load(data)
with open(path_data + 'labels_train.pickle', 'rb') as data:
    labels_train = pickle.load(data)
with open(path_data + 'labels_test.pickle', 'rb') as data:
    labels_test = pickle.load(data)
with open(path_data + 'tfidf_custom.pickle', 'rb') as data:
    tfidf_custom = pickle.load(data)

# ADD CODE MODEL TRAINING HERE:

# see default parameters of GBM classifier
gbc_default = Gbc()
print(gbc_default.get_params())

# fit the model
gbc_default.fit(features_train, labels_train)

predicted_classes_train = gbc_default.predict(features_train)
predicted_classes_test = gbc_default.predict(features_test)

print('The accuracy of the default GBM classifier on the TRAIN set is: ' +
      str(round(accuracy_score(labels_train, predicted_classes_train)*100, 2)) + ' %.')
print('The accuracy of the default GBM classifier on the TEST set is: ' +
      str(round(accuracy_score(labels_test, predicted_classes_test)*100, 2)) + ' %.')

# The output for 1500 unigrams (took an awful lot of time) is:
# The accuracy of the default GBM classifier on the TRAIN set is: 50.76 %.
# The accuracy of the default GBM classifier on the TEST set is: 38.16 %.

