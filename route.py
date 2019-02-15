
Point = complex

class Route(object):

        def __init__(self, path):
                self.path = list(path)

        def length(self):
                return sum(abs(self.path[i - 1] - self.path[i])
                                for i in range(len(self.path)))
        def time(self):
                return sum(times[inds[self.path[i-1]]][inds[self.path[i]]]
                                for i in range(len(self.path)))

        def __len__(self):
                return len(self.path)

        def __getitem__(self, key):
                return self.path[key]

        def __repr__(self):
                return str(self.path)

        def __str__(self):
                return self.path

        def __eq__(self, other):
                if not isinstance(self, other.__class__):
                        return False

                if not self.path[0] in other.path:
                        return False

                i = other.path.index(self.path[0])
                rotate = other.path[i:] + other.path[:i]
                return (self.path == rotate or
                        self.path == [rotate[0]] + rotate[1:][::-1])
