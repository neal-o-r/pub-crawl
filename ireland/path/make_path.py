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


def do_swaps(df):
    for i in [1,2,3,4]:
        order = pd.read_csv(f"verts.{i}", names=["order"])
        df = df.reindex(order.order)
    return df

df = pd.DataFrame(data=pubs_to_records("./all_pubs_clean.csv"),
        columns=["lat", "lng", "i", "trading_name", "address"])

df["address"] = df.address.str[:-1]

df = do_swaps(df)
