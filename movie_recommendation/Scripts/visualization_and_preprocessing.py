import os
import pandas as pd
print os.getcwd()
os.chdir(os.getcwd()+'\Data')
ratings=pd.read_csv('training_ratings_for_kaggle_comp.csv')
ratings_df=pd.DataFrame(ratings)
#print ratings_df.head(n=10)
#print ratings_df.describe()
#ratings_df['rating'].hist()

#for i in range(len(ratings_df.columns)):
#    print ratings_df.columns[i], len(set(ratings_df[ratings_df.columns[i]]))
#

rating_group_user=ratings_df.groupby('user').count()
#print rating_group_user.sort('movie',ascending=False).head()
#print rating_group_user['movie'].hist()
#print rating_group_user['movie'].describe()
rating_group_user=ratings_df.groupby('user').mean()
#print rating_group_user['rating'].hist()
#print rating_group_user['rating'].describe()


rating_group_movie=ratings_df.groupby('movie').count()
#print rating_group_movie.sort('user',ascending=False).head()
#print rating_group_movie.describe()
#print rating_group_movie['user'].hist()
rating_group_movie=ratings_df.groupby('movie').mean()
print rating_group_movie['rating'].hist()
print rating_group_movie['rating'].describe()
#ratings_df=ratings_df.sort_values(by='user')







import os
import pandas as pd
os.chdir(os.getcwd()+'\Data')
ratings=pd.read_csv('training_ratings_for_kaggle_comp.csv')
ratings_df=pd.DataFrame(ratings)

#rating_group_user=ratings_df.groupby('user').count()
##print rating_group_user.sort_values(by='movie',ascending=False).head()
#
##print ratings_df.head()
#
#quant_df = rating_group_user.quantile([0.01, 0.95])
#low=quant_df.loc[0.01,'movie']
#high=quant_df.loc[0.95,'movie']
#print low,high
#outliers_quant=rating_group_user[(rating_group_user['movie']<low) | (rating_group_user['movie']>high)]
#outliers_quant_low=rating_group_user[(rating_group_user['movie']<low)]
#outliers_std=rating_group_user[((rating_group_user['movie']-rating_group_user['movie'].mean())/rating_group_user['movie'].std())>3]
#
#print len(list(outliers_quant_low.index.get_values())), len(list(outliers_quant.index.get_values())),\
#len(list(outliers_std.index.get_values()))
#final_outlier=list(outliers_quant.index.get_values())
##final_outlier=final_outlier+list(outliers_std.index.get_values())
#print len(set(final_outlier))
#
#reduced_ratings=ratings_df[ratings_df['user'].isin(final_outlier)==False]
#
#print len(set(reduced_ratings['user']))
#print len(set(ratings_df['user']))
#
#rating_group_user=ratings_df.groupby('user').count()
#print rating_group_user['movie'].hist(bins=20)
#rating_group_user=reduced_ratings.groupby('user').count()
#print rating_group_user['movie'].hist(bins=10)

#print ratings_df.columns.tolist()
#
#rating_group_movie=ratings_df.groupby('movie').count()
#
#quant_df = rating_group_movie.quantile([0.05, 0.95])
#low=quant_df.loc[0.05,'user']
#high=quant_df.loc[0.95,'user']
#print low,high
#outliers_quant=rating_group_movie[(rating_group_movie['user']<low) | (rating_group_movie['user']>high)]
#outliers_quant=rating_group_movie[(rating_group_movie['user']<low)]
#outliers_std=rating_group_movie[((rating_group_movie['user']-rating_group_movie['user'].mean())/rating_group_movie['user'].std())>3]


#
#final_outlier=list(outliers_quant.index.get_values())
#print len(final_outlier)
#final_outlier=final_outlier+list(outliers_std.index.get_values())
#print len(final_outlier)
#print len(set(final_outlier))
#
#
#
#reduced_ratings=ratings_df[ratings_df['movie'].isin(final_outlier)==False]
#
#print len(set(reduced_ratings['movie']))
#print len(set(ratings_df['movie']))
#
#rating_group_movie=ratings_df.groupby('movie').count()
#print rating_group_movie['user'].hist()
#rating_group_movie=reduced_ratings.groupby('movie').count()
#print rating_group_movie['user'].hist()





###########################################################
## transformation
###########################################################
import math
import matplotlib.pyplot as plt
#
#rating_group_movie=ratings_df.groupby('movie').count()
#rating_group_movie_trans=map(math.log,map(float,list(rating_group_movie['user'])))
#print rating_group_movie_trans[1:5]
#xbins = [0, len(rating_group_movie_trans)]
#
#plt.hist(rating_group_movie_trans, bins=10)
##rating_group_movie['user'].hist()

rating=ratings_df['rating']
rating_trans=map(math.sqrt,map(float,list(rating)))
print rating_trans[1:5]
xbins = [0, len(rating_trans)]

plt.hist(rating_trans)
#rating_group_movie['user'].hist()
















