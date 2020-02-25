class Reverse_DSU:

    def __init__(self, initial_size):
        self.children = []
        self.initial_size = initial_size  # from 0 to (initial_size -1) are original ones
        for i in range(initial_size):
            self.children.append([-1, -1])

    def union(self, ind1, ind2):
        self.children.append([ind1, ind2])

    def get_all_children(self, source):  # semi-BFS
        ans = []
        queue = [source]
        while queue:
            now = queue.pop(0)
            ch1, ch2 = self.children[now]
            if ch1 == -1 and ch2 == -1:
                ans.append(now)
            if ch1 != -1:
                queue.append(ch1)
            if ch2 != -1:
                queue.append(ch2)
        return ans
