# Agglomerative Hierarchical Clustering Centroids_method (specially made for text data)
# link for youtube video explaining algorithm: https://www.youtube.com/watch?v=VMyXc3SiEqs

from Agglomerative_Clustering import AC

# data should be in format: list of dictionaries which contain the words and their frequency(tf)
# for example, if we have 2 sentences: "one two one" & " one two three" then data should be:
Data = [{'one': 2, 'two': 1}, {'one': 1, 'two': 1, 'three': 1}]  # this makes distance finding a lot faster

# Running:
ac = AC(Data)  # initialize the model
ac.get_dist_plot()  # show the plot so you can decide the cutting point
clusters = ac.get_output(0.7)  # gets list of list, cluster[2] has the indexes of data for that cluster
print(clusters)
