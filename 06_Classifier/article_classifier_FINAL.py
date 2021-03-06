import pickle
import pandas as pd
from sklearn.metrics import accuracy_score


def sort_probs(probs, cat):
    return probs.sort_values(by=cat, ascending=False)[[cat, 'topic_code']]


def classify_articles(model, model_names, model_number, features_train, features_test, labels_train, labels_test, stats,
                      topx, dataset):
    # fitting/training the model on the proved training data
    model.fit(features_train, labels_train)
    probab_test = model.predict_proba(features_test)
    df_proba = pd.DataFrame(labels_test)
    predicted_classes_test = model.predict(features_test)
    print('\nClassifier: ' + model_names[model_number] + ' accuracy: ' +
          str(round(accuracy_score(labels_test, predicted_classes_test)*100, 2)) + ' %.\n')
    print('Performance on ' + dataset + '.\n')

    for i in range(probab_test.shape[1]):
        column = "p" + str(i)
        df_proba[column] = probab_test[:, i]

    codes_categories = {'ARTS CULTURE ENTERTAINMENT': 0,
                        'BIOGRAPHIES PERSONALITIES PEOPLE': 1,
                        'DEFENCE': 2,
                        'DOMESTIC MARKETS': 3,
                        'FOREX MARKETS': 4,
                        'HEALTH': 5,
                        'MONEY MARKETS': 6,
                        'SCIENCE AND TECHNOLOGY': 7,
                        'SHARE LISTINGS': 8,
                        'SPORTS': 9,
                        'IRRELEVANT': 10}

    inv_code_categories = {v: k for k, v in codes_categories.items()}

    overall_hits = 0
    for i in range(probab_test.shape[1]):
        column = "p" + str(i)
        top10 = sort_probs(df_proba, column).head(topx)
        hits = top10['topic_code'] == i
        overall_hits += hits.astype(int).sum()
        if stats:
            print(top10)
            print('\nCategory ' + inv_code_categories[i] + ': ' + str(hits.astype(int).sum()) + '/' + str(topx) +
                  '.\n\n')

    print('OVERALL RESULT: ' + str(overall_hits) + '/' + str(int(probab_test.shape[1])*topx) + ".")
    if stats:
        print('(Performance on ' + dataset + '.)\n')

    return df_proba


# specify your directory where the project is here
# path Yannick:
path_project = "/Users/yannickschnider/PycharmProjects/COMP9417-Group-Assignment/"

# importing objects from folder data in feature engineering
path_data = path_project + '04_ModelTraining/Models/'
path_data2 = path_project + '03_FeatureEngineering/Data/'

with open(path_data + 'GBM.pickle', 'rb') as data:
    gbm = pickle.load(data)
with open(path_data + 'KNN.pickle', 'rb') as data:
    knn = pickle.load(data)
with open(path_data + 'MNB.pickle', 'rb') as data:
    mnb = pickle.load(data)
with open(path_data + 'RF.pickle', 'rb') as data:
    rf = pickle.load(data)
with open(path_data + 'SVM.pickle', 'rb') as data:
    svm = pickle.load(data)
with open(path_data + 'NN.pickle', 'rb') as data:
    nn = pickle.load(data)
with open(path_data2 + 'df_test.pickle', 'rb') as data:
    df_test = pickle.load(data)
with open(path_data2 + 'df_train.pickle', 'rb') as data:
    df_train = pickle.load(data)
with open(path_data2 + 'df_test_unfiltered.pickle', 'rb') as data:
    df_test_unfiltered = pickle.load(data)
with open(path_data2 + 'df_train_unfiltered.pickle', 'rb') as data:
    df_train_unfiltered = pickle.load(data)
with open(path_data2 + 'tfidf_custom.pickle', 'rb') as data:
    tfidf_custom = pickle.load(data)


# 1 == NN, 0 == SVM
modelselection = 0
show_filtered_results = 0
show_unfiltered_results = 0
show_unfiltered_results_with_cat_Irrelevant = 1
# show the stats for each categorie for true
show_stats = 1
# show the topX of each category
topX = 10

if modelselection:
    classifiers = [nn]
    classifiers_name = ['Multiperceptron']

else:
    classifiers = [svm]
    classifiers_name = ['SupportVector']

if show_filtered_results:
    # FILTERED DATA
    # FINAL test data set w/o irrelevant articles trained with FINAL training set w/o the irrelevant articles

    # fitting the tfidf transform on the whole train data
    features_train_filtered = tfidf_custom.fit_transform(df_train['article_words']).toarray()
    # applying the tfidf transform
    features_test_filtered = tfidf_custom.transform(df_test['article_words']).toarray()
    labels_train_filtered = df_train['topic_code']
    labels_test_filtered = df_test['topic_code']

    num = 0
    for classifier in classifiers:
        classify_articles(classifier, classifiers_name, num, features_train_filtered, features_test_filtered,
                          labels_train_filtered, labels_test_filtered, show_stats, topX,
                          'FINAL TEST data set WITHOUT irrelevant articles')
        num += 1

if show_unfiltered_results:
    # UNFILTERED DATA
    # FINAL test data set WITH irrelevant articles trained with FINAL training set w/o the irrelevant articles

    # fitting the tfidf transform on the whole train data
    features_train_filtered = tfidf_custom.fit_transform(df_train['article_words']).toarray()
    # applying the tfidf transform
    features_test_unfiltered = tfidf_custom.transform(df_test_unfiltered['article_words']).toarray()

    labels_train_filtered = df_train['topic_code']
    labels_test_unfiltered = df_test_unfiltered['topic_code']

    num = 0
    for classifier in classifiers:
        classify_articles(classifier, classifiers_name, num, features_train_filtered, features_test_unfiltered,
                          labels_train_filtered, labels_test_unfiltered, show_stats, topX,
                          'FINAL TEST data set WITH irrelevant articles')
        num += 1

if show_unfiltered_results_with_cat_Irrelevant:
    # FINAL test data set WITH irrelevant articles trained with FINAL training set WITH the irrelevant articles

    # fitting the tfidf transform on the whole UNFILTERED train data
    features_train_unfiltered = tfidf_custom.fit_transform(df_train_unfiltered['article_words']).toarray()
    # applying the tfidf transform
    features_test_unfiltered = tfidf_custom.transform(df_test_unfiltered['article_words']).toarray()
    labels_train_unfiltered = df_train_unfiltered['topic_code']
    labels_test_unfiltered = df_test_unfiltered['topic_code']

    num = 0
    for classifier in classifiers:
        classify_articles(classifier, classifiers_name, num, features_train_unfiltered, features_test_unfiltered,
                          labels_train_unfiltered, labels_test_unfiltered, show_stats, topX,
                          'FINAL TEST data set WITH TRAINED irrelevant articles')
        num += 1


