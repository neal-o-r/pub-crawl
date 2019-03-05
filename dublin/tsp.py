from route import Route, Point
import random
from itertools import permutations
import matplotlib.pyplot as plt


def rand_points(n):
    # make random points
    return [Point(random.randint(0, 100), random.randint(0, 100)) for i in range(n)]


def nonred_permutations(pts):
    # all non-redundant permutations
    # e.g. [1,2,3] and [3,1,2] are redundant, they define the same path
    head, *tail = pts
    return [[head] + list(p) for p in permutations(tail)]


def exhaustive(pts):
    # check all non-red permutations and select min
    return min((Route(i) for i in nonred_permutations(pts)), key=lambda x: x.length())


def greedy(pts, path=[]):
    # TODO: make this accept a Route object
    # recursively find greedy path
    if not pts:
        return path

    # if the path is empty, put the last value into path
    if not len(path):
        path.append(pts.pop())

    p = min(pts, key=lambda x: abs(path[-1] - x))
    i = pts.index(p)
    return greedy(pts[:i] + pts[i + 1 :], path + [p])


def plot_path(route):
    for i in range(len(route)):
        plt.plot(route[i].real, route[i].imag, "ok", zorder=10)
        plt.plot(
            (route[i].real, route[i - 1].real),
            (route[i].imag, route[i - 1].imag),
            c="0.8",
            alpha=0.8,
        )
    plt.axis("off")
    plt.show()


def subsegments(N):
    # given a number, generate all indices of
    # subsegments of a path len <= N
    return [
        (i, i + length)
        for length in reversed(range(2, N))
        for i in reversed(range(N - length + 1))
    ]


def try_swaps(route_in):
    # recursively do swaps until there
    # aren't any left that decrease length
    # i.e. until there are no crosses left
    post_swap = swap_points(route_in)
    if (post_swap == route_in):
        return post_swap
    else:
        return try_swaps(post_swap)


def swap_points(r):
    # go through all subsegments
    # and try reversing it, if the length
    # decreases keep the swap
    min_l = r.length()
    p = r.path[:]
    for s in subsegments(len(r)):
        i, j = s
        j = j % len(p)
        p[i:j] = reversed(p[i:j])
        if Route(p).length() < min_l:
            r = Route(p)
            min_l = r.length()
        else:
            p = r.path[:]

    return r


def tsp(pts):
    return try_swaps(Route(greedy(pts)))

if __name__ == "__main__":

    pts = rand_points(100)
    optimised_route = tsp(pts)

    plot_path(optimised_route)

