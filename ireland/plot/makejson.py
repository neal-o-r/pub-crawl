import pandas as pd
import json

pubs = pd.read_csv("../path/pubs_path.csv")

points = {
    "type": "FeatureCollection",
    "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
}

features = []
for i, row in pubs.iterrows():
    d = {
        "type": "Feature",
        "properties": {
            "latitude": row.latitude,
            "longitude": row.longitude,
            "time": int(i + 1),
            "id": "route1",
            "name": str(row.trading_name)
        },
        "geometry": {"type": "Point", "coordinates": [row.longitude, row.latitude]},
    }

    features.append(d)

points["features"] = features

json.dump(points, open('ireland.json', 'w'), indent=4)
