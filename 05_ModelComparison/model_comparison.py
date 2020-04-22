import pickle
import pandas as pd
from sklearn.metrics import accuracy_score


def create_table(models, model_names):
    table = pd.DataFrame()
    table['Name'] = model_names
    training_accuracies = []
    test_accuracies = []
    for model in models:
        pred_train = model.predict(features_train)
        pred_test = model.predict(features_test)
        accuracy_train = round(accuracy_score(labels_train, pred_train)*100, 2)
        accuracy_test = round(accuracy_score(labels_test, pred_test)*100, 2)
        training_accuracies.append(accuracy_train)
        test_accuracies.append(accuracy_test)
    table['Accuracy Training'] = training_accuracies
    table['Accuracy Test'] = test_accuracies
    return table


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
with open(path_data + 'NN.pickle', 'rb') as data:
    nn = pickle.load(data)
with open(path_data + 'SVM.pickle', 'rb') as data:
    svm = pickle.load(data)
with open(path_data2 + 'labels_train.pickle', 'rb') as data:
    labels_train = pickle.load(data)
with open(path_data2 + 'labels_test.pickle', 'rb') as data:
    labels_test = pickle.load(data)
with open(path_data2 + 'features_train.pickle', 'rb') as data:
    features_train = pickle.load(data)
with open(path_data2 + 'features_test.pickle', 'rb') as data:
    features_test = pickle.load(data)

classifiers = [gbm, knn, mnb, rf, svm, nn]
classifiers_name = ['GradientBoost', 'NearestNeighbour', 'MultinomBayes', 'RandomForest', 'SupportVector',
                    'Multiperceptron']

df_table = create_table(classifiers, classifiers_name)
df_table_sorted = df_table.sort_values(by='Accuracy Test', ascending=False)
print(df_table_sorted)

# saving the table
with open('df_table_sorted.pickle', 'wb') as output:
    pickle.dump(df_table_sorted, output)

# Output for 2000 features:
#                Name  Accuracy Training  Accuracy Test
# 5   Multiperceptron              94.96          77.15
# 0     GradientBoost              98.64          77.04
# 1  NearestNeighbour              82.79          76.73
# 4     SupportVector              90.63          76.52
# 3      RandomForest              98.58          74.32
# 2     MultinomBayes              79.30          72.43

#  Output for 1000 features
#                Name  Accuracy Training  Accuracy Test
# 5   Multiperceptron              92.97          76.83
# 4     SupportVector              88.75          76.21
# 1  NearestNeighbour              82.76          76.10
# 0     GradientBoost              98.58          75.16
# 3      RandomForest              98.56          74.63
# 2     MultinomBayes              78.83          74.00
