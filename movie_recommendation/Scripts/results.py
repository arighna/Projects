###############################################################################
##########################      read the data  ################################
###############################################################################

import os
path=os.getcwd()+'\..\Data'
os.chdir(path)
#print os.listdir(os.getcwd())
with open('performance.csv', 'r') as f:
    results=[line.split(',') for i,line in enumerate(f.readlines())]



###############################################################################
###################     fetch and process the results  #######################
###############################################################################

results_edited=[]   ### processed result
for i in range(len(results)-8):                                             ## the first 8 rows contain the headers
    results_edited.append([0]*50)                                           ## total 50 cols. 1st is the name of the distance; 7 fields for each 'K'; K,user_rating,time for user_rating, movie_rating, time for movie_rating, avg_rating, time for avg_rating
    results_edited[i][0]=results[i+8][0]                                    ## name of the distance
    for j in range(7):                                                      ## loop through each 'K'. 
        results_edited[i][7*j+1]=results[i+8][7*j+1][2:]                    ## fetch K and process it because there is '"[' attached to the it in the beginning
        results_edited[i][(7*j+2):(7*j+7)]=results[i+8][(7*j+2):(7*j+7)]    ## fetch the 5 values as is
        results_edited[i][7*j+7]=results[i+8][7*j+7][:-2]                   ## fetch the last value and process it because there is ']"' attached to the it in the end
    results_edited[i][49]=results_edited[i][49][:-1]                        ## the last loop (k=50) of each distance for the has an extra '\n'
print results_edited[0]




###############################################################################
###################  plots for k ##############################
###############################################################################

import matplotlib.pyplot as plt
x=[1,3,5,10,15,25,50]
fig = plt.figure()


### plot the user based filtering rating prediction accuracy #######
for i in range(len(results_edited)):
    y=[results_edited[i][j] for j in [2,9,16,23,30,37,44]]                  ### for user based filtering 2,9,16,23,30,37,44 cols of results_edited contain error rate for k=1,3,5,10,15,25,50
    plt.plot(x,y,label=results_edited[i][0])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),                 ### (0.5, -0.2); '-' keeps it below the fig
          fancybox=True, shadow=True, ncol=2)
plt.title('Error Rate vs number of nearest neighbors for predicted ratings \
of user based collaborative filtering',y=-0.6)                              ### y=-0.6; '-' keeps it below the fig
plt.xlabel('Number of nearest neighbors')
plt.ylabel('Error Rate')
plt.show()

#### plot the movie based filtering rating prediction accuracy #######
for i in range(len(results_edited)):
    y=[results_edited[i][j+2] for j in [2,9,16,23,30,37,44]]                ### for movie based filtering indexes of 2 places right from 2,9,16,23,30,37,44 cols of results_edited contain error rate for k=1,3,5,10,15,25,50
    plt.plot(x,y,label=results_edited[i][0])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, shadow=True, ncol=2)
plt.title('Error Rate vs number of nearest neighbors for predicted ratings \
of movie based collaborative filtering',y=-0.6)
plt.xlabel('Number of nearest neighbors')
plt.ylabel('Error Rate')
plt.show()

### plot the average of user and movie based filtering rating prediction accuracy #######
for i in range(len(results_edited)):
    y=[results_edited[i][j+4] for j in [2,9,16,23,30,37,44]]                ### for avg filtering indexes of 4 places right from 2,9,16,23,30,37,44 cols of results_edited contain error rate for k=1,3,5,10,15,25,50
    plt.plot(x,y,label=results_edited[i][0])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, shadow=True, ncol=2)
plt.title('Error Rate vs number of nearest neighbors for average ratings \
of user based and movie based collaborative filtering',y=-0.6)
plt.xlabel('Number of nearest neighbors')
plt.ylabel('Error Rate')
plt.show()





###############################################################################
###################  plots for time             ##############################
###############################################################################


import matplotlib.pyplot as plt
x=[1,3,5,10,15,25,50]
fig = plt.figure()


### plot the user based filtering rating prediction accuracy #######
for i in range(len(results_edited)):
    y=[results_edited[i][j] for j in [3,10,17,24,31,38,45]]                  ### for user based filtering 2,9,16,23,30,37,44 cols of results_edited contain error rate for k=1,3,5,10,15,25,50
    plt.plot(x,y,label=results_edited[i][0])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),                 ### (0.5, -0.2); '-' keeps it below the fig
          fancybox=True, shadow=True, ncol=2)
plt.title('Time consumed vs number of nearest neighbors \n for predicted ratings \
of user based collaborative filtering',y=-0.7)                              ### y=-0.6; '-' keeps it below the fig
plt.xlabel('Number of nearest neighbors')
plt.ylabel('Time consumed')
plt.show()

#### plot the movie based filtering rating prediction accuracy #######
for i in range(len(results_edited)):
    y=[results_edited[i][j+2] for j in [3,10,17,24,31,38,45]]                ### for movie based filtering indexes of 2 places right from 2,9,16,23,30,37,44 cols of results_edited contain error rate for k=1,3,5,10,15,25,50
    plt.plot(x,y,label=results_edited[i][0])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, shadow=True, ncol=2)
plt.title('Time consumed vs number of nearest neighbors \n for predicted ratings \
of movie based collaborative filtering',y=-0.7)
plt.xlabel('Number of nearest neighbors')
plt.ylabel('Time consumed')
plt.show()

### plot the average of user and movie based filtering rating prediction accuracy #######
for i in range(len(results_edited)):
    y=[results_edited[i][j+4] for j in [3,10,17,24,31,38,45]]                ### for avg filtering indexes of 4 places right from 2,9,16,23,30,37,44 cols of results_edited contain error rate for k=1,3,5,10,15,25,50
    plt.plot(x,y,label=results_edited[i][0])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2),
          fancybox=True, shadow=True, ncol=2)
plt.title('Time consumed vs number of nearest neighbors \n for average ratings \
of user based and movie based collaborative filtering',y=-0.7)
plt.xlabel('Number of nearest neighbors')
plt.ylabel('Time consumed')
plt.show()