import fastf1
import pandas as pd
import numpy as np
import requests
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from xgboost import XGBRegressor

fastf1.Cache.enable_cache("f1_cache")

# load the 2024 Qatar session data
session_2024 = fastf1.get_session(2024, 24, "R")
session_2024.load()
laps_2024 = session_2024.laps[["Driver", "LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]].copy()
laps_2024.dropna(inplace=True)

# convert lap and sector times to seconds
for col in ["LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]:
    laps_2024[f"{col} (s)"] = laps_2024[col].dt.total_seconds()

# aggregate sector times by driver
sector_times_2024 = laps_2024.groupby("Driver").agg({
    "Sector1Time (s)": "mean",
    "Sector2Time (s)": "mean",
    "Sector3Time (s)": "mean"
}).reset_index()

sector_times_2024["TotalSectorTime (s)"] = (
    sector_times_2024["Sector1Time (s)"] +
    sector_times_2024["Sector2Time (s)"] +
    sector_times_2024["Sector3Time (s)"]
)

# clean air race pace from racepace.py
clean_air_race_pace = {
    "VER": 93.191067, "HAM": 94.020622, "LEC": 93.418667, "NOR": 93.428600, "ALO": 94.784333,
    "PIA": 93.232111, "RUS": 93.833378, "SAI": 94.497444, "STR": 95.318250, "HUL": 95.345455,
    "OCO": 95.682128
}

# quali data from Abu Dhabi GP
qualifying_2025 = pd.DataFrame({
    "Driver": ["RUS", "VER", "PIA", "NOR", "HAM", "LEC", "ALO", "HUL", "ALB", "SAI", "STR", "OCO", "GAS"],
    "QualifyingTime (s)": [
        82.645,  # RUS
        82.207,  # VER
        82.437,  # PIA
        82.408,  # NOR
        83.394,  # HAM
        82.730,  # LEC
        82.902,  # ALO
        83.450,  # HUL
        83.416,  # ALB
        83.042,  # SAI
        83.097,  # STR
        82.913,  # OCO
        83.468   # GAS
    ]
})

qualifying_2025["CleanAirRacePace (s)"] = qualifying_2025["Driver"].map(clean_air_race_pace)

# WeatherAPI.com integration
API_KEY = "4a734687533140f1b1a101427250712"  # Your WeatherAPI key
location = "Abu Dhabi"  # Yas Marina Circuit location
weather_url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=3&aqi=no&alerts=no"

try:
    response = requests.get(weather_url)
    response.raise_for_status()  # Raise an error for bad status codes
    weather_data = response.json()
    
    # Extract forecast for the race day (assuming race is tomorrow)
    forecast_data = weather_data["forecast"]["forecastday"][1]  # Next day
    
    # Get weather conditions for race time (usually 13:00 local time)
    # You might need to adjust the hour based on race time
    race_hour_condition = forecast_data["hour"][13]  # 1 PM
    
    # Extract relevant weather parameters
    temperature = race_hour_condition["temp_c"]
    rain_probability = race_hour_condition["chance_of_rain"] / 100  # Convert from percentage to decimal
    condition_text = race_hour_condition["condition"]["text"]
    
    print(f"📍 Weather forecast for Abu Dhabi GP:")
    print(f"🌡️  Temperature: {temperature}°C")
    print(f"🌧️  Rain probability: {rain_probability * 100:.0f}%")
    print(f"⛅ Condition: {condition_text}")
    
except requests.exceptions.RequestException as e:
    print(f"⚠️  Weather API error: {e}")
    print("⚠️  Using default weather values")
    temperature = 28  # Default Abu Dhabi temperature
    rain_probability = 0.05  # Low rain probability
    condition_text = "Sunny"

# adjust qualifying time based on weather conditions
if rain_probability >= 0.75:
    # Add wet performance factor if not already in data
    if "WetPerformanceFactor" not in qualifying_2025.columns:
        # Default wet performance factors (you might want to customize these)
        wet_performance_factors = {
            "VER": 1.02, "HAM": 1.01, "LEC": 1.03, "NOR": 1.02, "ALO": 1.04,
            "PIA": 1.025, "RUS": 1.03, "SAI": 1.04, "STR": 1.05, "HUL": 1.045,
            "OCO": 1.05, "GAS": 1.05, "ALB": 1.04
        }
        qualifying_2025["WetPerformanceFactor"] = qualifying_2025["Driver"].map(wet_performance_factors)
    
    qualifying_2025["QualifyingTime"] = qualifying_2025["QualifyingTime (s)"] * qualifying_2025["WetPerformanceFactor"]
else:
    qualifying_2025["QualifyingTime"] = qualifying_2025["QualifyingTime (s)"]

# add constructor's data
team_points = {
    "McLaren": 800, "Mercedes": 459, "Red Bull": 426, "Williams": 137, "Ferrari": 382,
    "Haas": 73, "Aston Martin": 80, "Kick Sauber": 68, "Racing Bulls": 92, "Alpine": 22
}

max_points = max(team_points.values())
team_performance_score = {team: points / max_points for team, points in team_points.items()}

driver_to_team = {
    "VER": "Red Bull", "NOR": "McLaren", "PIA": "McLaren", "LEC": "Ferrari", "RUS": "Mercedes",
    "HAM": "Ferrari", "GAS": "Alpine", "ALO": "Aston Martin", "TSU": "Racing Bulls",
    "SAI": "Williams", "HUL": "Kick Sauber", "OCO": "Alpine", "STR": "Aston Martin"
}

qualifying_2025["Team"] = qualifying_2025["Driver"].map(driver_to_team)
qualifying_2025["TeamPerformanceScore"] = qualifying_2025["Team"].map(team_performance_score)

# merge qualifying and sector times data
merged_data = qualifying_2025.merge(sector_times_2024[["Driver", "TotalSectorTime (s)"]], on="Driver", how="left")
merged_data["RainProbability"] = rain_probability
merged_data["Temperature"] = temperature
merged_data["WeatherCondition"] = condition_text
merged_data["QualifyingTime"] = merged_data["QualifyingTime"]

valid_drivers = merged_data["Driver"].isin(laps_2024["Driver"].unique())
merged_data = merged_data[valid_drivers]

# define features (X) and target (y)
X = merged_data[[
    "QualifyingTime", "RainProbability", "Temperature", "TeamPerformanceScore", 
    "CleanAirRacePace (s)"
]]
y = laps_2024.groupby("Driver")["LapTime (s)"].mean().reindex(merged_data["Driver"])

# impute missing values for features
imputer = SimpleImputer(strategy="median")
X_imputed = imputer.fit_transform(X)

# train-test split
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.1, random_state=39)

# train XGBoost model
model = XGBRegressor(n_estimators=300, learning_rate=0.9, max_depth=3, random_state=39, monotone_constraints='(1, 0, 0, -1, -1)')
model.fit(X_train, y_train)
merged_data["PredictedRaceTime (s)"] = model.predict(X_imputed)

# sort the results to find the predicted winner
final_results = merged_data.sort_values(by=["PredictedRaceTime (s)", "QualifyingTime"]).reset_index(drop=True)
print("\n📊 Final Predictions:")
print(final_results[["Driver", "PredictedRaceTime (s)"]])

# sort results and get top 3
podium = final_results.loc[:7, ["Driver", "PredictedRaceTime (s)"]]
print("\n🏆 Predicted in the Top 3 🏆")
print(f"🥇 P1: {podium.iloc[0]['Driver']}")
print(f"🥈 P2: {podium.iloc[1]['Driver']}")
print(f"🥉 P3: {podium.iloc[2]['Driver']}")

# Model evaluation
y_pred = model.predict(X_test)
print(f"\n📈 Model Error (MAE): {mean_absolute_error(y_test, y_pred):.2f} seconds")

# Plot feature importances
feature_importance = model.feature_importances_
features = X.columns

plt.figure(figsize=(8,5))
plt.barh(features, feature_importance, color='skyblue')
plt.xlabel("Importance")
plt.title("Feature Importance in Race Time Prediction")
plt.tight_layout()
plt.show()