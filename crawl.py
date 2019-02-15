import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json

from concorde.tsp import TSPSolver

GOOGLE_MAPS_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"


def read_data():

    p = "Publican's Licence (7-Day Ordinary)"
    df = pd.read_csv("liquor-licences.csv").query(f'description == "{p}"')

    df = df[~df.trading_name.isnull()]

    df["address_2"] = [
        a if not a.startswith("&") else "" for a in df["address_2"].astype(str)
    ]
    df["address_2"] = df["address_2"].str.replace("nan", "")

    df["Full_address"] = (
        df.filter(regex="^address").fillna("").apply(lambda x: ", ".join(x), axis=1)
    )

    df["Full_address"] = df.trading_name.fillna("") + ", " + df.Full_address
    df["Full_address"] = df.Full_address.str.rstrip("+") + ", " + df.county
    df["Full_address"] = df.Full_address.str.replace(" ,", "").str.lstrip(" ")

    dubs = df[df.county.str.startswith("Dublin")]

    return dubs


def get_lat_lon(address):

    params = {"address": address, "region": "ie", "key": ""}  # KEY HERE

    # Do the request and get the response data
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()

    # Use the first result
    if len(res["results"]) == 0:
        return {"lat": None, "lng": None, "address": None}

    result = res["results"][0]
    geodata = dict()
    geodata["lat"] = result["geometry"]["location"]["lat"]
    geodata["lng"] = result["geometry"]["location"]["lng"]
    geodata["address"] = result["formatted_address"]

    return geodata


def filter_on_dist(df):

    centre = np.array([53.347311, -6.259136])
    outer = np.array([53.378566, -6.355327])
    dist = np.linalg.norm(centre - outer)

    df["dist"] = (df[["latitude", "longitude"]] - outer).T.apply(np.linalg.norm)

    return df.query(f"dist < {dist}").reset_index()


def all_lat_lon(df):
    lat, lng, add = [], [], []
    for a in df.Full_address:
        d = get_lat_lon(a)
        lat.append(d["lat"])
        lng.append(d["lng"])
        add.append(d["address"])

    return lat, lng, add


def geocode():
    dubs = read_data()
    dubs["latitude"], dubs["longitude"], dubs["g_address"] = all_lat_lon(dubs)
    dubs.to_csv("all_dub_pubs.csv", index=False)
    return dubs


def tsp(df):

    solver = TSPSolver.from_data(df.latitude, df.longitude, norm="GEO")

    tour_data = solver.solve()
    return df.iloc[tour_data.tour].reset_index(), tour_data


if __name__ == "__main__":

    dubs = pd.read_csv("all_dub_pubs.csv")
    dubs = dubs[dubs.latitude.notnull()]

    dubs, tour = tsp(dubs)
    dubs[["latitude", "longitude", "trading_name"]].to_csv(
        "plot/dub_pubs.csv", index=False
    )
