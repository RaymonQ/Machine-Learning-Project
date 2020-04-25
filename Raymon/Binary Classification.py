import pickle

import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV, ShuffleSplit
from sklearn.linear_model import LogisticRegression
import time

from sklearn.feature_extraction.text import TfidfVectorizer as TfIdf

from sklearn.metrics import confusion_matrix, classification_report

# Decide if to implement grid search or not
fit_grid_search = 0

# Specify Path Project
#path_project = "/Users/TalWe/.vscode/COMP9417 Group Assignment/COMP9417-Group-Assignment/"
path_project = "/Users/yannickschnider/PycharmProjects/COMP9417-Group-Assignment/"

# read data
df = pd.read_csv(path_project + "00_TaskHandout/training.csv", sep=',')
df_test = pd.read_csv(path_project + "00_TaskHandout/test.csv", sep=',')

#TfIdf settings
ngram_range = (1, 1)
min_df = 10
max_df = 1.
max_features = 2000
sublinear_tf = True
stop_words = None
tfidf_custom = TfIdf(ngram_range=ngram_range, max_df=max_df, min_df=min_df, max_features=max_features,
                     sublinear_tf=sublinear_tf, stop_words = stop_words)

topic_codes = {
    'IRRELEVANT': 0,
    'ARTS CULTURE ENTERTAINMENT': 1,
    'BIOGRAPHIES PERSONALITIES PEOPLE': 1,
    'DEFENCE': 1,
    'DOMESTIC MARKETS': 1,
    'FOREX MARKETS': 1,
    'HEALTH': 1,
    'MONEY MARKETS': 1,
    'SCIENCE AND TECHNOLOGY': 1,
    'SHARE LISTINGS': 1,
    'SPORTS': 1,   
}

df['relevance'] = df['topic']
df = df.replace({'relevance':topic_codes})

df_test['relevance'] = df_test['topic']
df_test = df_test.replace({'relevance':topic_codes})

# Fit TFIDF to Train Features, only apply transform to Test input
features_train = tfidf_custom.fit_transform(df['article_words']).toarray()
X_test_final = tfidf_custom.transform(df_test['article_words']).toarray()
labels_train = df['relevance']
y_test_final = df_test['relevance']


# IMPLEMENT CROSS VALIDATION FOR TUNING LOGISTIC REGRESSION HYPERPARAMETERS
if fit_grid_search:
    # parameter grid based on output random search
    multiclass = ['ovr']
    n_jobs = [-1]
    max_iter = [100,200,300,500]

    param_grid = [
        {'penalty': ['l2'], 'multi_class': multiclass, 'solver': ['newton-cg','sag','lbfgs'], 'n_jobs': n_jobs, 'max_iter': max_iter},
        {'penalty': ['elasticnet'], 'multi_class': multiclass, 'solver': ['saga'], 'n_jobs': n_jobs, 'max_iter': max_iter},
        {'penalty': ['l1'], 'multi_class': multiclass, 'solver': ['liblinear','saga'], 'n_jobs': n_jobs, 'max_iter': max_iter}
    ]

    # Create a base model
    logit_model = LogisticRegression()

    # splits in CV with random state
    cv_sets = ShuffleSplit(n_splits=5, test_size=.2, random_state=0)

    # Instantiate the grid search model
    start_time = time.process_time()
    grid_search = GridSearchCV(estimator=logit_model,
                               param_grid=param_grid,
                               scoring='accuracy',
                               cv=cv_sets,
                               verbose=0)

    # Fit the grid search to the data
    grid_search.fit(features_train, labels_train)
    end_time = time.process_time() - start_time

logit_best_grid = grid_search.best_estimator_
predicted_classes_train = logit_best_grid.predict(features_train)
predicted_classes_test = logit_best_grid.predict(X_test_final)


'''# Train Validation Split on Training Data to apply Cross Validation to

for i in range(10):
    X_train, X_test, y_train, y_test = train_test_split(features_train, labels_train, test_size=0.20, random_state=None)

    # Validation test data
    logit_model = LogisticRegression()

    # Fit model 
    logit_model = logit_model.fit(X_train, y_train)
    prediction = logit_model.predict(X_test)
    
    # Confusion metrics
    cnf_matrix = confusion_matrix(y_test, prediction)
    print(cnf_matrix)
    
    # Results
    
    print(classification_report(y_test, prediction))
'''

# Real test data
# parameters chosen from Cross Validation
logit_model = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
          intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=-1,
          penalty='l2', random_state=None, solver='sag', tol=0.0001,
          verbose=0, warm_start=False)

# Fit model 
logit_model = logit_model.fit(features_train, labels_train)
prediction = logit_model.predict(X_test_final)

# Confusion metrics
cnf_matrix = confusion_matrix(y_test_final, prediction)
print(cnf_matrix)

# Results
print(classification_report(y_test_final, prediction))

# Filter Test Data to only include articles that were prediction relevant by logistic model function
df_test['prediction'] = prediction
df_test_predicted_relevant = df_test[df_test['prediction'] == 1]

# Remove relevance and prediction columns (as they're redundant for next part of classification)
df_test_predicted_relevant = df_test_predicted_relevant.drop(columns=["relevance", "prediction"])

print(df_test_predicted_relevant.head())

# Save Logistic Regression model in Pickle file
with open('df_test_predicted_relevant.pickle', 'wb') as output:
    pickle.dump(df_test_predicted_relevant, output)
