# PricePilot — Used Car Price Predictor

Ridge regression (alpha = 1.0) predicts a used car's resale price (Rs lakh) from age, mileage, engine size, brand tier, previous owners, fuel and transmission. Trained on 600 synthetic listings (seed 42).

- 5-fold CV: R² = 0.745, MAE = Rs 1.79 lakh (baseline Rs 3.62 lakh)
- Live demo: https://pricepilot.vercel.app (interactive, runs fully in the browser)
- `train.py` trains the model and exports `model.json`; `index.html` reproduces it exactly in JavaScript.

By Vikranth Reddy — B.Tech CSE (AI & ML), Woxsen University.
