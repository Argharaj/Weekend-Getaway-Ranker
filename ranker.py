import pandas as pd


file_path = "data/Top Indian Places to Visit.csv"
city_name = input("Enter Source City: ")

df = pd.read_csv(file_path)

if "Unnamed: 0" in df.columns:
    df.drop("Unnamed: 0", axis=1, inplace=True)

df["City"] = df["City"].astype(str)

city_data = df[df["City"].str.lower() == city_name.lower()]

if len(city_data) == 0:
    print("No places found for this city")
else:
    
    if city_data["Google review rating"].isnull().any():
        avg_rating = city_data["Google review rating"].mean()
        city_data["Google review rating"].fillna(avg_rating, inplace=True)

    if city_data["Number of google review in lakhs"].isnull().any():
        city_data["Number of google review in lakhs"].fillna(0, inplace=True)

    if city_data["time needed to visit in hrs"].isnull().any():
        med_time = city_data["time needed to visit in hrs"].median()
        city_data["time needed to visit in hrs"].fillna(med_time, inplace=True)

    max_rating = city_data["Google review rating"].max()
    city_data["rating_score"] = city_data["Google review rating"] / max_rating

    max_pop = city_data["Number of google review in lakhs"].max()
    if max_pop == 0:
        city_data["popularity_score"] = 0
    else:
        city_data["popularity_score"] = (
            city_data["Number of google review in lakhs"] / max_pop
        )

    max_time = city_data["time needed to visit in hrs"].max()
    city_data["time_score"] = 1 - (
        city_data["time needed to visit in hrs"] / max_time
    )

    city_data["final_score"] = (
        city_data["rating_score"] * 0.5
        + city_data["popularity_score"] * 0.3
        + city_data["time_score"] * 0.2
    )

    city_data = city_data.sort_values("final_score", ascending=False)

    print("\nTop Weekend Places in", city_name, "\n")

    print(
        city_data[
            [
                "Name",
                "State",
                "Google review rating",
                "Number of google review in lakhs",
                "time needed to visit in hrs",
            ]
        ]
        .head(5)
        .to_string(index=False)
    )
