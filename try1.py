import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
import joblib
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np



df = pd.read_csv("Agriculture_price_dataset.csv")

df.dropna(subset=['STATE', 'District Name', 'Market Name', 'Commodity', 
                  'Min_Price', 'Max_Price', 'Modal_Price'], inplace=True)
# Build pipeline

X = df[['STATE', 'District Name', 'Market Name', 'Commodity','Min_Price','Max_Price']]
y = df['Modal_Price']

cat_features = [0, 1, 2, 3]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


model = CatBoostRegressor(
    iterations=800,
    depth=8,
    learning_rate=0.05,
    loss_function='RMSE',
    random_seed=42,
    verbose=100
)

model.fit(X_train, y_train, cat_features=cat_features)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100


from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_pred)

print("MAE:", mae)
print("MAPE (%):", mape)
print("R2 Score (Accuracy):", r2)

# -------------------------------------------
# 6. Feature Importance
# -------------------------------------------
importances = model.get_feature_importance()
feature_names = X.columns

for name, score in zip(feature_names, importances):
    print(f"{name}: {score}")



model.save_model("crop_price_model.cbm")
print("\n✅ Model saved successfully as crop_price_model.cbm")