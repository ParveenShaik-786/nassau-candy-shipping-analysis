import pandas as pd


def load_data(file_path):
    # Load CSV
    df = pd.read_csv(file_path)

    # Convert dates
    df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    dayfirst=True,
    errors="coerce"
    )

    df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    dayfirst=True,
    errors="coerce"
   )

    # Remove rows where dates could not be parsed
    df = df.dropna(subset=["Order Date", "Ship Date"])
    # Remove duplicates
    df = df.drop_duplicates()

    # Lead Time
    df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days

    # Remove negative lead times
    df = df[df["Lead Time"] >= 0]

    return df