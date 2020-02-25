import math
import matplotlib.pyplot as plt
from Reverse_DSU import Reverse_DSU


class AC:
    def __init__(self, data):
        """
        :param data: get data in format list of dictionaries
        """
        self.data_init = data  # list of dicts
        # if 3 & 5 merge, we erase them from valid and append a new data including both with new index in valid
        self.valid_init = {}
        for i in range(len(self.data_init)):  # init valid
            self.valid_init[i] = 1
        self.distances_init = []
        # init distances:  ([5][3] will contain the dist, not [3][5] (two times faster, half memory))
        for i in range(len(self.data_init)):
            dists = []
            for j in range(0, i):
                dists.append(self.find_distance(self.data_init[i], self.data_init[j]))
            self.distances_init.append(dists)
        self.itr_min_dists = []

    def get_dist_plot(self):
        """
        :return: shows the plot for minimum distance merging in every iteration of the algorithm
        """
        data = self.data_init.copy()
        valid = self.valid_init.copy()
        distances = self.distances_init.copy()

        # the algorithm:
        for itr in range(len(self.data_init) - 1):
            if itr % 50 == 0:
                print("get_dist_plot:   saw " + str(itr))
            min_dist = 1e9
            min_ind1 = -1
            min_ind2 = -1
            for ind1 in valid.keys():
                for ind2 in valid.keys():
                    if ind1 <= ind2:
                        continue
                    if distances[ind1][ind2] < min_dist:
                        min_dist = distances[ind1][ind2]
                        min_ind1 = ind1
                        min_ind2 = ind2
            self.itr_min_dists.append(min_dist)
            del valid[min_ind1]
            del valid[min_ind2]
            new_data = self.merge(data[min_ind1], data[min_ind2])
            new_dists = []
            for ind in range(len(data)):
                new_dist = 1e9 if ind not in valid else self.find_distance(data[ind], new_data)
                new_dists.append(new_dist)
            data.append(new_data)
            valid[len(data) - 1] = 1
            distances.append(new_dists)
        # see visuals to chose from where to cut off in get_output (find knee):
        x = []
        for i in range(0, len(self.data_init) - 1):
            x.append(i)
        plt.plot(x, self.itr_min_dists, 'ro', markersize=1)
        plt.show()

    def get_output(self, max_dist):
        """
        :param max_dist: chose from which minimum distance they shouldn't merge anymore
        :return: returns a list of list, each row contains the index of the input data
        which belongs to that cluster, example: returnedData[2] is a list which has [3, 5, 8]
        it means the input data with indexes [3, 5, 8] have made a cluster
        """
        r_dsu = Reverse_DSU(len(self.data_init))  # initial DSU model
        data = self.data_init.copy()
        valid = self.valid_init.copy()
        distances = self.distances_init.copy()

        # the algorithm:
        for itr in range(len(self.data_init) - 1):
            if itr % 50 == 0:
                print("get_output:   saw " + str(itr))
            min_dist = 1e9
            min_ind1 = -1
            min_ind2 = -1
            for ind1 in valid.keys():
                for ind2 in valid.keys():
                    if ind1 <= ind2:
                        continue
                    if distances[ind1][ind2] < min_dist:
                        min_dist = distances[ind1][ind2]
                        min_ind1 = ind1
                        min_ind2 = ind2
            if min_dist > max_dist:
                print("Number of Clusters Found: " + str(len(self.data_init) - itr))
                break
            self.itr_min_dists.append(min_dist)
            del valid[min_ind1]
            del valid[min_ind2]
            new_data = self.merge(data[min_ind1], data[min_ind2])
            new_dists = []
            for ind in range(len(data)):
                new_dist = 1e9 if ind not in valid else self.find_distance(data[ind], new_data)
                new_dists.append(new_dist)
            r_dsu.union(min_ind1, min_ind2)
            data.append(new_data)
            valid[len(data) - 1] = 1
            distances.append(new_dists)
        # now get the list of dataPoints for each Cluster:
        clusters = []
        for key in valid.keys():
            clusters.append(r_dsu.get_all_children(key))

        return clusters

    def find_distance(self, dp1, dp2, dist_method='CosineSimilarity'):
        if dist_method == 'CosineSimilarity':
            sum_products = 0
            len_dp1 = len_dp2 = 0
            for name, cnt in dp1.items():
                len_dp1 += cnt * cnt
                if name in dp2:
                    sum_products += cnt * dp2[name]
            for name, cnt in dp2.items():
                len_dp2 += cnt * cnt
            ans = sum_products / (math.sqrt(len_dp1) * math.sqrt(len_dp2))
            return 1 - ans
        if dist_method == 'Jaccard':
            over_lap = union = 0.0
            for name, cnt in dp1.items():
                if name in dp2:
                    over_lap += min(cnt, dp2[name])
                    union += max(cnt, dp2[name])
                else:
                    union += cnt
            for name, cnt in dp2.items():
                if name not in dp1:
                    union += cnt
            return 1 - (over_lap / union)

    def merge(self, data1, data2):
        ans = data1.copy()
        for name, cnt in data2.items():
            if name not in ans:
                ans[name] = cnt
            else:
                ans[name] += cnt
        return ans
