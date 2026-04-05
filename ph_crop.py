import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("C:\\Users\\sujal\\OneDrive\\Desktop\\ALL DATA\\PYTHON\\ML Projects\\data_for_ml\\CropDataset_Final_with_estimated_pH.csv")

# Features and label
x = df[["Latitude", "Longitude"]]
y = df["estimated_pH"]

# Select a row for prediction
row = df.iloc[50]
sample = [[row["Latitude"], row["Longitude"]]]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.05, random_state=42)

# --- Polynomial Regression ---
# Convert features to polynomial form (degree = 2 for now)
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Train model
model = LinearRegression()
model.fit(X_poly, y_train)

# Predict
sample_poly = poly.transform(sample)
y_pred = model.predict(sample_poly)

print("Predicted Nitrogen (Polynomial Regression):", y_pred[0])