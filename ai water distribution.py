import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Sample dataset
data = {
    "Temperature": [30, 32, 35, 28, 25, 33, 31],
    "Population": [1000, 1200, 1500, 900, 800, 1300, 1100],
    "Water_Demand": [500, 600, 750, 450, 400, 680, 550]
}

df = pd.DataFrame(data)

X = df[["Temperature", "Population"]]
y = df["Water_Demand"]

model = LinearRegression()
model.fit(X, y)

print("AI Water Demand Prediction System")
temp = float(input("Enter Temperature: "))
pop = float(input("Enter Population: "))
# Optional: Add input validation
if temp < 0 or pop < 0:
    print("Error: Temperature and Population must be non-negative")
else:
    prediction = model.predict([[temp, pop]])
    print("Predicted Water Demand:", round(prediction[0], 2), "liters")
