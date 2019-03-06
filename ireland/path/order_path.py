import pandas as pd

def record_from_pubs(name):
    with open(name) as f:
        txt = f.read().split("\n")[2:-1]

    records = []
    for l in txt:
        lstrip = l.split(" ", 3)
        rstrip = lstrip[-1].split('"', 1)
        records.append((*lstrip[:-1], *rstrip))

    return records


def apply_reorder(df):
    for i in ["1", "2", "3", "4"]:
        order = pd.read_csv(f"verts.{i}", names=["order"], )
        df = df.iloc[order.order]
    return df

if __name__ == "__main__":
    df = pd.DataFrame(data=record_from_pubs("./all_pubs_clean.csv"),
            columns=["latitude", "longitude", "i", "trading_name", "address"])

    df["address"] = df.address.str[:-1]

