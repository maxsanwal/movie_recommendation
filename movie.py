import csv
from math import sqrt

movies = {}
ratinglist = {}
def loadmovies(path1='ml-latest-small/movies.csv', path2='ml-latest-small/ratings.csv'):
	with open(path1) as csvfile:
		readcsv = csv.reader(csvfile, delimiter=',')
		for rows in readcsv:
			id = rows[0]
			movies[id]=rows[1]

	with open(path2) as csvfile:
		readcsv = csv.reader(csvfile, delimiter=',')
		next(readcsv)
		for rows in readcsv:
			user = rows[0]
			movieid = rows[1]
			rate = rows[2]

			ratinglist.setdefault(user, {})
			ratinglist[user][movies[movieid]] = float(rate)
	return ratinglist

loadedmovies = loadmovies()

def sim_pearson(prefs,p1,p2):
	# Get the list of mutually rated items
	si={}
	for item in prefs[p1]:
		if item in prefs[p2]: 
			si[item]=1
		# Find the number of elements
	n=len(si)
	# if they are no ratings in common, return 0
	if n==0: 
		return 0
	# Add up all the preferences
	sum1=sum([prefs[p1][it] for it in si])
	sum2=sum([prefs[p2][it] for it in si])
	# Sum up the squares
	sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
	sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
	# Sum up the products
	pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
	# Calculate Pearson score
	num=pSum-(sum1*sum2/n)
	den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den==0: 
		return 0
	r=num/den
	return r

def rankratings(ratings, person, n=100,similarity = sim_pearson):
	rank = [(similarity(ratings,person,others),others) for others in ratings if others!=person]
	rank.sort()
	rank.reverse()
	return rank[0:n]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
	totals={}
	simSums={}
	for other in prefs:
		# don't compare me to myself
		if other==person: continue
		sim=similarity(prefs,person,other)
		# ignore scores of zero or lower
		if sim<=0: continue
		for item in prefs[other]:
			# only score movies I haven't seen yet
			if item not in prefs[person] or prefs[person][item]==0:
				# Similarity * Score
				totals.setdefault(item,0)
				totals[item]+=prefs[other][item]*sim
				# Sum of similarities
				simSums.setdefault(item,0)
				simSums[item]+=sim
	# Create the normalized list
	rankings=[(total/simSums[item],item) for item,total in totals.items( )]
	# Return the sorted list
	rankings.sort( )
	rankings.reverse( )
	return rankings
h = rankratings(loadedmovies, '250')
g = getRecommendations(loadedmovies,'150')
print g





