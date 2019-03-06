import pandas as pd

def pubs_to_records(name):
    with open(name) as f:
        txt = f.read().split('\n')[2:-1]

    records = []
    for l in txt:
        lsplit = l.split(" ", 3)
        rsplit = lsplit[-1].split('"', 1)
        records.append((*lsplit[:-1], *rsplit))

    return records


df = pd.DataFrame(data=pubs_to_records("./all_pubs_clean.csv"),
        columns=["lat", "lng", "i", "trading_name", "address"])

df["address"] = df.address.str[:-1]


order = pd.read_csv("./verts.4", names=["order"])


