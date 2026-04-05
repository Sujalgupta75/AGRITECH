import pandas as pd
from catboost import CatBoostRegressor

# Load the saved model
model = CatBoostRegressor()
model.load_model("crop_price_model.cbm")

print("✅ Model loaded successfully!")

# Load dataset
df = pd.read_csv("Agriculture_price_dataset.csv")

def predict_price(state, district, mandi, commodity):
    # Filter dataset to fetch min/max price
    filtered = df[
        (df["STATE"] == state) &
        (df["District Name"] == district) &
        (df["Market Name"] == mandi) &
        (df["Commodity"] == commodity)
    ]

    if filtered.empty:
        return None, None, None  # No match found

    # Take the latest matching row
    row = filtered.iloc[-1]

    min_p = row["Min_Price"]
    max_p = row["Max_Price"]

    # Prepare input for prediction
    sample = pd.DataFrame({
        'STATE': [state],
        'District Name': [district],
        'Market Name': [mandi],
        'Commodity': [commodity],
        'Min_Price': [min_p],
        'Max_Price': [max_p]
    })

    pred = model.predict(sample)[0]
    return pred, min_p, max_p


# User input loop
while True:
    print("\nEnter data for prediction (type 'exit' to stop):")
    state = input("State: ")
    if state.lower() == 'exit':
        break

    district = input("District: ")
    mandi = input("Mandi Name: ")
    commodity = input("Commodity: ")

    pred, min_p, max_p = predict_price(state, district, mandi, commodity)

    if pred is None:
        print("\n❌ No matching data found in dataset. Try again.")
        continue

    print("\n✅ Data Fetched Automatically:")
    print(f"Min Price: {min_p}")
    print(f"Max Price: {max_p}")

    print(f"\n✅ Predicted Model Price: {pred:.2f} Rs")
