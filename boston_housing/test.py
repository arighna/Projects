import numpy as np
import pandas as pd
import visuals as vs # Supplementary code
from sklearn.cross_validation import ShuffleSplit
import pylab as pl
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.metrics import r2_score
from sklearn.cross_validation import train_test_split
from sklearn import cross_validation
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import make_scorer
from sklearn.grid_search import GridSearchCV




data = pd.read_csv('housing.csv')
prices = data['MDEV']
features = data.drop('MDEV', axis = 1)

#print "Boston housing dataset has {} data points with {} variables each.".format(*data.shape)
#
#
#minimum_price = min(prices)
#maximum_price = max(prices)
#mean_price = np.mean(prices)
#median_price = np.median(prices)
#std_price = np.std(prices)

## Show the calculated statistics
#print "Statistics for Boston housing dataset:\n"
#print "Minimum price: ${:,.2f}".format(minimum_price)
#print "Maximum price: ${:,.2f}".format(maximum_price)
#print "Mean price: ${:,.2f}".format(mean_price)
#print "Median price ${:,.2f}".format(median_price)
#print "Standard deviation of prices: ${:,.2f}".format(std_price)

## plot the histogram of the prices
#prices_hist=sorted(prices)
#fit = stats.norm.pdf(prices_hist, mean_price, std_price)  #this is a fitting indeed
#pl.plot(prices_hist,fit,'-o')
#pl.hist(prices_hist,normed=True)

print features.keys()
rooms=features['RM']
lstat=features['LSTAT']
ptratio=features['PTRATIO']

#plt.scatter(rooms, prices,alpha=0.5)
#plt.scatter(lstat, prices,alpha=0.5)
#plt.scatter(ptratio, prices,alpha=0.5)


def performance_metric(y_true, y_predict):
    score = r2_score(y_true, y_predict)
    return score
# Calculate the performance of this model
score = performance_metric([3, -0.5, 2, 7, 4.2], [2.5, 0.0, 2.1, 7.8, 5.3])
print "Model has a coefficient of determination, R^2, of {:.3f}.".format(score)
    
X_train, X_test, y_train, y_test = train_test_split(features, prices, test_size=0.33, random_state=42)
#vs.ModelLearning(features, prices)
#vs.ModelComplexity(X_train, y_train)
def fit_model(X, y):
    cv_sets = cross_validation.ShuffleSplit(X.shape[0], n_iter = 10, test_size = 0.20, random_state = 0)
    regressor = DecisionTreeRegressor()
    params = {'max_depth': list(range(1,11))}
    scoring_fnc = make_scorer(performance_metric)
    grid = GridSearchCV(regressor, params, scoring = scoring_fnc, cv = cv_sets)
    grid = grid.fit(X, y)
    return grid.best_estimator_
    
reg = fit_model(X_train, y_train)


## Produce the value for 'max_depth'
print "Parameter 'max_depth' is {} for the optimal model.".format(reg.get_params()['max_depth'])

client_data = [[5, 34, 15], # Client 1
               [4, 55, 22], # Client 2
               [8, 7, 12]]  # Client 3

for i, price in enumerate(reg.predict(client_data)):
    print "Predicted selling price for Client {}'s home: ${:,.2f}".format(i+1, price)
    
#vs.PredictTrials(features, prices, fit_model, client_data)