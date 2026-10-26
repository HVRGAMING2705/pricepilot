import json, numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_predict, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

rng = np.random.default_rng(42)
n = 600
age = rng.uniform(0, 15, n)              # years
mileage = rng.uniform(5, 180, n)         # thousand km
engine = rng.uniform(0.8, 3.0, n)        # litres
brand = rng.integers(0, 3, n).astype(float)   # 0 budget, 1 mid, 2 premium
owners = rng.integers(1, 4, n).astype(float)
diesel = rng.integers(0, 2, n).astype(float)
automatic = rng.integers(0, 2, n).astype(float)
# Generative price in Rs lakh: premium brands start higher, value falls with
# age and mileage; bigger engines and automatics add value; extra owners cut it.
base = 4.0 + 6.5*brand + 2.0*engine + 1.2*automatic + 0.8*diesel
y_true = base * np.exp(-0.13*age) - 0.035*mileage - 0.9*(owners-1) + 0.4*engine*brand
y = np.clip(y_true + rng.normal(0, 1.2, n), 0.5, 80.0)
X = np.column_stack([age, mileage, engine, brand, owners, diesel, automatic])
names = ["age_years","mileage_1000km","engine_litres","brand_tier","owners","is_diesel","is_automatic"]
mu, sd = X.mean(0), X.std(0)
Xs = (X - mu) / sd
model = Ridge(alpha=1.0).fit(Xs, y)
kf = KFold(5, shuffle=True, random_state=42)
pred_cv = cross_val_predict(Ridge(alpha=1.0), Xs, y, cv=kf)
mae = float(mean_absolute_error(y, pred_cv))
rmse = float(np.sqrt(mean_squared_error(y, pred_cv)))
r2 = float(r2_score(y, pred_cv))
baseline_mae = float(mean_absolute_error(y, np.full_like(y, y.mean())))
print(f"CV MAE={mae:.2f} RMSE={rmse:.2f} R2={r2:.3f} baseline_MAE={baseline_mae:.2f}")
print("coef", model.coef_, "intercept", model.intercept_)
model_json = {"features": names, "means": mu.tolist(), "stds": sd.tolist(),
              "coef": model.coef_.tolist(), "intercept": float(model.intercept_),
              "metrics": {"cv_mae": mae, "cv_rmse": rmse, "cv_r2": r2, "baseline_mae": baseline_mae, "n": n}}
with open("model.json","w") as f: json.dump(model_json, f, indent=1)
def predict(v):
    z = (np.array(v)-mu)/sd
    return float(np.clip(model.intercept_ + z @ model.coef_, 0.5, 80.0))
samples = [[3,40,1.5,1,1,0,0],[8,120,1.2,0,2,1,0],[1,10,2.0,2,1,0,1],[12,160,1.0,0,3,1,0],[5,60,1.8,2,1,1,1]]
for s in samples: print(s, round(predict(s),2))
