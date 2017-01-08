import math 
from decimal import Decimal
import pandas as pd
import os

os.chdir(os.getcwd()+'\..\Data')
rating_file='training_ratings_for_kaggle_comp.csv'
## read the target file
with open(rating_file, 'r') as f:
    ratings=[line.split(',') for i,line in enumerate(f.readlines())]
ratings=pd.read_csv('training_ratings_for_kaggle_comp.csv')
ratings_df=pd.DataFrame(ratings).iloc[:10000,]          ## mention the size of the data to be considered and convert into a pandas dataframe
print 'data successfully read'
rating_users=list(set(ratings_df['user']))

print len(rating_users)



user_rating={}
## build rating_users
## keys are the users, then for each user there is one dictionary. Keys for 
## those are the movies he rated and values are the ratings
for user in rating_users:
    ## movie and rating for each user
    temp=ratings_df[ratings_df['user']==user]
    temp=temp[['movie','rating']].values.tolist()
#    temp=[[rating[1],rating[2]] for rating in ratings_training if rating[0]==str(user)]
    user_rating[str(user)]={}   
    for pair in temp:
        user_rating[str(user)][str(pair[0])]=float(pair[1])
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

        count=len(rating_a)
        rating_diffs=[((rating_a[c]-(sum(rating_a)/count))*(rating_b[c]-(sum(rating_b)/count)))/(abs(rating_a[c]-(sum(rating_a)/count))*abs(rating_b[c]-(sum(rating_b)/count))) for c in range(len(rating_a)) if (abs(rating_a[c]-(sum(rating_a)/count))*abs(rating_b[c]-(sum(rating_b)/count)))!=0]
        rating_diff=(sum(rating_diffs))/len(rating_a) if len(rating_a)!=0 else 0
    similarity[str(rating_users[i])][str(rating_users[j])]=rating_diff

print similarity


import networkx as nx
G=nx.Graph()
for node in similarity.keys():
    if node not in G.nodes():
        G.add_node(node)
        for new_node in similarity[node].keys():
            edge=(node,new_node)
            G.add_edge(*edge)
nx.draw(G)

