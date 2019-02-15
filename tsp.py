from route import Route, Point
import random
from itertools import permutations
import matplotlib.pyplot as plt
import pandas as pd

n = 10


def rand_points(n):
    return [Point(random.randint(0, 100), random.randint(0, 100)) for i in range(n)]


def nonred_permutations(pts):
    head, *tail = pts
    return [[head] + list(p) for p in permutations(tail)]


def exhaustive(pts):
    return min((Route(i) for i in nonred_permutations(pts)), key=lambda x: x.length())


def greedy(pts, route):
    if not pts:
        return route

    # p = min(pts, key=lambda x: abs(route[-1] - x))
    p = min(zip(pts, times[inds[route[-1]]]), key=lambda x: x[1])[0]
    i = pts.index(p)
    return greedy(pts[:i] + pts[i + 1 :], route + [p])


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
    return [
        (i, i + length)
        for length in reversed(range(2, N))
        for i in reversed(range(N - length + 1))
    ]


def try_swaps(route_in, n=10):
    post_swap = swap_points(route_in)
    if (post_swap == route_in) or (n == 0):
        return post_swap
    else:
        print(n)
        return try_swaps(post_swap, n=n-1)


def swap_points(r):
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


if __name__ == "__main__":

    pubs = pd.read_csv("plot/dub_pubs.csv")
    pts = [Point(r.latitude, r.longitude) for i, r in pubs.iterrows()]
    opt = try_swaps(Route(pts))

    inds = [pts.index(o) for o in opt]
    pubs.iloc[inds][['latitude', 'longitude', 'trading_name']].to_csv("plot/opt_pubs.csv")


