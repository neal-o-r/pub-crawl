import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from concorde.tsp import TSPSolver

def read_data():

    pubs = pd.read_csv('pubs.csv')
    p = "Publican's Licence (7-Day Ordinary)"
    df = pd.read_csv('liquor-licences.csv').query(f'description == "{p}"')

    join = df.merge(pubs.drop_duplicates('name'),
        left_on='trading_name', right_on='name', how='left')

    dubs = join[(join.latitude.notnull()) & (join.county.str.startswith('Dublin'))]

    return dubs


def filter_on_dist(df):

    centre = np.array([53.347311, -6.259136])
    outer = np.array([53.390541, -6.348379])
    dist = np.linalg.norm(centre - outer)

    df["dist"] = (df[['latitude', 'longitude']] - outer).T.apply(np.linalg.norm)

    return df.query(f"dist < {dist}").reset_index()



if __name__ == "__main__":

    dubs = filter_on_dist(read_data())

    '''
    solver = TSPSolver.from_data(
        dubs.latitude,
        dubs.longitude,
        norm="GEO"
    )

    tour_data = solver.solve()

    dubs = dubs.iloc[tour_data.tour].reset_index()
    dubs[['type', 'color', 'url']] = 'pub', 'a80000', None

    dubs[['latitude', 'longitude', 'name',
        'type', 'color', 'url']].to_csv('optimal_dub_pubs.csv',index_label='id')
    '''
