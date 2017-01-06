import math 
from decimal import Decimal
import pandas as pd
import os


###############################################################################
#class for calculating all kinds of distance metrics except Pearson Correlation   ################################
## but this distance is not divided by the length of the vectors. It's performed in the place where it was called from
###############################################################################

class Similarity():
    def euclidean_distance(self,x,y):
        return math.sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))
    def standardized_euclidean_distance(self,x,y):
        x=[i/(float(sum(x))/len(x)) for i in x]
        y=[i/(float(sum(y))/len(y)) for i in y]      
        return math.sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))
    def normalized_euclidean_distance(self,x,y):
        x=[i/float(max(x)) for i in x]
        y=[i/float(max(y)) for i in y]      
        return math.sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))
    def manhattan_distance(self,x,y):
        return sum(abs(a-b) for a,b in zip(x,y))
    def minkowski_distance(self,x,y,p_value=3):
        return self.nth_root(sum(pow(abs(a-b),p_value) for a,b in zip(x, y)), p_value)
    def nth_root(self,value, n_root):
        root_value = 1/float(n_root)
        return round (Decimal(value) ** Decimal(root_value),3)
        

###############################################################################
##########################  read the data from \..\Data\  directory   ################################
###############################################################################

def data_read():
    os.chdir(os.getcwd()+'\..\Data')
    rating_file='training_ratings_for_kaggle_comp.csv'
    ## read the target file
    with open(rating_file, 'r') as f:
        ratings=[line.split(',') for i,line in enumerate(f.readlines())]
    ratings=pd.read_csv('training_ratings_for_kaggle_comp.csv')
    ratings_df=pd.DataFrame(ratings).iloc[:50000,]          ## mention the size of the data to be considered and convert into a pandas dataframe
    print 'data successfully read'
    return ratings_df


###############################################################################
####  split the data into training and testing with a 4:1 ratio   ################################
###############################################################################

def training_testing(ratings_df):
    users=list(set(ratings_df['user']))
    training=pd.DataFrame()
    testing=pd.DataFrame()
    ## making sure that none of the user is missing in the training. It's difficult to recommend a movie to a user if the history of his movie selection is not known
    for user in users:
        df=ratings_df[ratings_df['user']==user].sample(frac=1,random_state=42)
        train=df.sample(frac=0.8,random_state=200)
        test=df.drop(train.index)
        training=training.append(train)
        testing=testing.append(test)
    print len(training), len(testing)
    ## filter a subset of the whole data set
    ratings_training=training
    # fetch the users who have rated movies
    rating_users=list(set(ratings_training['user']))
    print 'training and testing split'
    return ratings_training, testing, rating_users
    
### create the object of the distance class which can be used later
dist=Similarity()


###############################################################################
#### build the similarity matrix for users  ################################
###############################################################################

def user_ratings(ratings_training, rating_users,metric):
    ## dictionary with users as keys, then movies as keys of each user and rating as corrsponding values
    user_rating={}
    ## build rating_users
    ## keys are the users, then for each user there is one dictionary. Keys for 
    ## those are the movies he rated and values are the ratings
    for user in rating_users:
        ## movie and rating for each user
        temp=ratings_training[ratings_training['user']==user]
        temp=temp[['movie','rating']].values.tolist()
    #    temp=[[rating[1],rating[2]] for rating in ratings_training if rating[0]==str(user)]
        user_rating[str(user)]={}   
        for pair in temp:
            user_rating[str(user)][str(pair[0])]=float(pair[1])
    #print user_rating.keys()

    ## build the similarity matrix for users
    ## keys are the users, values are dictionary again. keys are users and values
    ## are similarities
    import math
    similarity={}
    for i in range(len(rating_users)):
        similarity[str(rating_users[i])]={}
        for j in range(len(rating_users)):
            rating_diff=0
            count=1
            rating_a=[]
            rating_b=[]
            for movie in user_rating[str(rating_users[i])].keys():
                if user_rating[str(rating_users[j])].has_key(movie):
                    rating_a.append(float(user_rating[str(rating_users[i])][movie]))
                    rating_b.append(float(user_rating[str(rating_users[j])][movie]))
    #                rating_diff+=(float(user_rating[str(rating_users[j])][movie])-\
    #                float(user_rating[str(rating_users[i])][movie]))**2
    #                rating_diff+=( -float(user_rating[str(rating_users[i])][movie]))**2
    #                count+=1
    #        rating_diffs=[(rating_a[c]-rating_b[c])**2 for c in range(len(rating_a))]
    #        rating_diff=math.sqrt(sum(rating_diffs))/len(rating_a) if len(rating_a)!=0 else 0
            if metric in ['euclidean_distance','standardized_euclidean_distance','normalized_euclidean_distance',\
            'manhattan_distance','minkowski_distance']:
                rating_diffs=getattr(dist,metric)(rating_a,rating_b)
                rating_diff=rating_diffs/len(rating_a) if len(rating_a)!=0 else 0
            else:       ## for pearson correlation
                count=len(rating_a)
                rating_diffs=[((rating_a[c]-(sum(rating_a)/count))*(rating_b[c]-(sum(rating_b)/count)))/(abs(rating_a[c]-(sum(rating_a)/count))*abs(rating_b[c]-(sum(rating_b)/count))) for c in range(len(rating_a)) if (abs(rating_a[c]-(sum(rating_a)/count))*abs(rating_b[c]-(sum(rating_b)/count)))!=0]
                rating_diff=(sum(rating_diffs))/len(rating_a) if len(rating_a)!=0 else 0
            similarity[str(rating_users[i])][str(rating_users[j])]=rating_diff
    print 'done building the user similarity for ' + metric
    return similarity, user_rating

###############################################################################
#### predict the rating of a movie by a user based on user filtering ################################
###############################################################################

def user_based_rating(similarity, user_rating, myuser,mymovie,k):
    non_zero={k:v for k,v in similarity[myuser].items() if abs(v)>0}
    movie_filtered={k:v for k,v in non_zero.items() if user_rating[k].has_key(mymovie)}
    sorted_non_zero=sorted(movie_filtered, key=lambda k:movie_filtered[k])
    neigh_num=min(k,len(sorted_non_zero))
    if neigh_num==0:
        return 0
#    neighbors[myuser]=sorted_non_zero[:neigh_num]
    new_rating=0
    for i in range(neigh_num):
        new_rating+=float(user_rating[sorted_non_zero[i]][mymovie])
    return (new_rating/float(neigh_num))


###############################################################################
#### build the similarity matrix for movies  ################################
###############################################################################

def movie_ratings(ratings_training, metric):
    rating_movies=list(set(ratings_training['movie']))
    movie_rating={}
    ### build movie_rating
    for movie in rating_movies:
        ## user and rating for each movie
        temp=ratings_training[ratings_training['movie']==movie]
        temp=temp[['user','rating']].values.tolist()
    #    temp=[[rating[0],rating[2]] for rating in ratings_training if rating[1]==str(movie)]
        movie_rating[str(movie)]={}   
        for pair in temp:
            movie_rating[str(movie)][str(pair[0])]=float(pair[1])

    ## build the similarity matrix
    import math
    similarity_movies={}
    for i in range(len(rating_movies)):
        similarity_movies[str(rating_movies[i])]={}
        for j in range(len(rating_movies)):
            rating_a=[]
            rating_b=[]
            for user in movie_rating[str(rating_movies[i])].keys():
                if movie_rating[str(rating_movies[j])].has_key(user):
                    rating_a.append(float(movie_rating[str(rating_movies[j])][user]))
                    rating_b.append(float(movie_rating[str(rating_movies[i])][user]))
    #        rating_diffs=[(rating_a[c]-rating_b[c])**2 for c in range(len(rating_a))]
    #        rating_diff=math.sqrt(sum(rating_diffs))/len(rating_a) if len(rating_a)!=0 else 0
            count=len(rating_a)
            if metric in ['euclidean_distance','standardized_euclidean_distance','normalized_euclidean_distance',\
            'manhattan_distance','minkowski_distance']:
                rating_diffs=getattr(dist,metric)(rating_a,rating_b)
                rating_diff=rating_diffs/len(rating_a) if len(rating_a)!=0 else 0
            else:       ## for pearson correlation
                rating_diffs=[((rating_a[c]-(sum(rating_a)/count))*(rating_b[c]-(sum(rating_b)/count)))/(abs(rating_a[c]-(sum(rating_a)/count))*abs(rating_b[c]-(sum(rating_b)/count))) for c in range(len(rating_a)) if (abs(rating_a[c]-(sum(rating_a)/count))*abs(rating_b[c]-(sum(rating_b)/count)))!=0]
                rating_diff=(sum(rating_diffs))/len(rating_a) if len(rating_a)!=0 else 0
            similarity_movies[str(rating_movies[i])][str(rating_movies[j])]=rating_diff
    print 'done building the movie similarity'
    return similarity_movies, movie_rating


###############################################################################
#### predict the rating of a movie by a user based on movie filtering ################################
###############################################################################

def movie_based_rating(similarity_movies, movie_rating, myuser,mymovie,k):
    non_zero_movies={k:v for k,v in similarity_movies[mymovie].items() if abs(v)>0}
    filtered_movies={k:v for k,v in non_zero_movies.items() if movie_rating[k].has_key(myuser)}
    sorted_non_zero_movies=sorted(filtered_movies, key=lambda k:filtered_movies[k])
    neigh_num=min(k,len(sorted_non_zero_movies))
    if neigh_num==0:
        return 0
#    neighbors[mymovie]=sorted_non_zero_movies[:neigh_num]
    new_rating=0
    for i in range(neigh_num):
        new_rating+=float(movie_rating[sorted_non_zero_movies[i]][myuser])
    return (new_rating/float(neigh_num))

###############################################################################
#### perform the ratings for different model parameters ################################
###############################################################################

def perform(similarity, user_rating, similarity_movies, movie_rating, testing):
    training_movies=similarity_movies.keys()
    import time
    import math
    performance=[]
    
    for k in [1,3,5,10,15,25,50]:
    #    ratings_testing=ratings[i*1000:(i+1)*1000]
        t1=time.time()
        ratings_testing=testing
        result=[]
        time_user=0
        time_movie=0
        for testing_index in range(len(ratings_testing)):
            myuser=str(ratings_testing.iloc[testing_index,0])
            mymovie=str(ratings_testing.iloc[testing_index,1])
            if mymovie in training_movies:
                t2=time.time()
                rating_movie_based=movie_based_rating(similarity_movies, movie_rating, myuser,mymovie,k)
                t3=time.time()
                rating_user_based=user_based_rating(similarity, user_rating, myuser,mymovie,k)
                t4=time.time()            
                avg_rating=(rating_movie_based+rating_user_based)/2.0
                result.append([ratings_testing.iloc[testing_index,2],rating_movie_based,rating_user_based,avg_rating])
                time_user=time_user+(t3-t2)
                time_movie=time_movie+(t4-t3)
        total_time=time.time()-t1
        #print sum(float(myresult[0]) for myresult in result)/len(result), \
        #        sum(myresult[1] for myresult in result)/len(result)
        #print result
        squared_error_user,squared_error_movie,squared_error_average=0,0,0
        for rating in result:
            squared_error_user+=(float(rating[0])-float(rating[1]))**2
            squared_error_movie+=(float(rating[0])-float(rating[2]))**2
            squared_error_average+=(float(rating[0])-float(rating[3]))**2
        squared_error_user,squared_error_movie,squared_error_average=math.sqrt(squared_error_user)/len(result),math.sqrt(squared_error_movie)/len(result),math.sqrt(squared_error_average)/len(result)
#        print k, squared_error_user, time_user, squared_error_movie, \
        time_movie, squared_error_average, total_time
        performance.append([k, squared_error_user, time_user, squared_error_movie, time_movie, squared_error_average, total_time])
    return performance
## find similarity matrix for users
## pick a combination of user and movie, 
## filter the users which have rated that movie
## find the users with min similarity
## similarity*rating avg for the filtered users


### list of distance metric
metric_list=['pearson','minkowski_distance','euclidean_distance','standardized_euclidean_distance','normalized_euclidean_distance',\
            'manhattan_distance']
all_performances=['metric','k', 'squared_error_user', 'time_user', 'squared_error_movie', 'time_movie', 'squared_error_average', 'total_time']

ratings_df=data_read()
ratings_training, testing, rating_users=training_testing(ratings_df)

for mymetric in metric_list:
    similarity, user_rating = user_ratings(ratings_training, rating_users,mymetric)
    similarity_movies, movie_rating = movie_ratings(ratings_training, mymetric)
    all_performances.append([mymetric]+perform(similarity, user_rating, similarity_movies, movie_rating,testing))
    print [mymetric]+perform(similarity, user_rating, similarity_movies, movie_rating,testing)
    
print all_performances

import csv
with open('performance.csv','wb') as f:
    writer=csv.writer(f)
    writer.writerows(all_performances) 