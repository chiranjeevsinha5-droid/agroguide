# rainfall_predictor_model.py
import os
import pandas as pd
import joblib
import numpy as np
from datetime import datetime

BASE_DIR = r"C:\Users\dipak\OneDrive\Desktop\crop"
CLEAN_MONTHLY_DIR = os.path.join(BASE_DIR, "rainfall_monthly_clean")
MODELS_DIR = os.path.join(BASE_DIR, "models")

class RainfallPredictor:
    def __init__(self):
        pass

    def _load_prophet_model(self, state_name):
        model_path = os.path.join(MODELS_DIR, f"prophet_{state_name.lower()}.pkl")
        if os.path.exists(model_path):
            try:
                obj = joblib.load(model_path)
                return obj.get('model') if isinstance(obj, dict) else obj
            except Exception as e:
                print("Failed to load prophet model:", e)
        return None

    def _load_clean_monthly(self, state_name):
        csv_path = os.path.join(CLEAN_MONTHLY_DIR, f"{state_name}_monthly_clean.csv")
        if not os.path.exists(csv_path):
            return None
        df = pd.read_csv(csv_path)
        df['month_dt'] = pd.to_datetime(df['month'] + "-01")
        df = df.sort_values('month_dt')
        return df

    def _seasonal_average_forecast(self, df, target_year):
        df['month_num'] = pd.to_datetime(df['month'] + "-01").dt.month
        monthly_avg = df.groupby('month_num')['rain_sum'].mean()
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        preds = [float(monthly_avg.get(m, 0.0)) for m in range(1,13)]
        # shift labels to target_year
        labels = [f"{m} {target_year}" for m in months]
        return pd.DataFrame({'Month': labels, 'Predicted Rainfall (mm)': preds}).set_index('Month')

    def _prophet_forecast_for_year(self, m, hist_df, target_year):
        # hist_df has 'month_dt' and 'rain_sum'
        last_date = hist_df['month_dt'].max()
        # forecast up to end of target_year (month frequency)
        # compute months to forecast: from last_date (month) to Dec(target_year)
        start = last_date + pd.DateOffset(months=1)
        end = pd.Timestamp(f"{target_year}-12-01")
        if start > end:
            # target_year is earlier than next month -> still produce next 12 months but relabel
            periods = 12
            future = m.make_future_dataframe(periods=periods, freq='MS')
            forecast = m.predict(future)
        else:
            # number of months to roll
            months_needed = (end.year - start.year) * 12 + (end.month - start.month) + 1
            future = m.make_future_dataframe(periods=months_needed, freq='MS')
            forecast = m.predict(future)
        # forecast contains many months starting from history start; we need target_year months
        forecast['ds'] = pd.to_datetime(forecast['ds'])
        forecast['year'] = forecast['ds'].dt.year
        forecast['month_name'] = forecast['ds'].dt.strftime('%b')
        # select only rows where year == target_year and keep month order Jan->Dec
        target = forecast[forecast['year'] == int(target_year)].copy()
        # If no rows found (e.g., target_year beyond computed range), fallback to last 12 months predicted
        if target.empty:
            # get the last 12 forecasted months
            last12 = forecast.sort_values('ds').tail(12)
            labels = [f"{d.strftime('%b')} {d.year}" for d in last12['ds']]
            preds = last12['yhat'].clip(lower=0).values
            return pd.DataFrame({'Month': labels, 'Predicted Rainfall (mm)': preds}).set_index('Month')
        # otherwise, order by month
        target = target.sort_values('ds')
        labels = [f"{d.strftime('%b')} {d.year}" for d in target['ds']]
        preds = target['yhat'].clip(lower=0).values
        return pd.DataFrame({'Month': labels, 'Predicted Rainfall (mm)': preds}).set_index('Month')

    def predict(self, state, target_year=None):
        """
        state: e.g. "Uttar Pradesh" or "Uttar_Pradesh" (either)
        target_year: integer year (e.g., 2026). If None -> next 12 months from history end.
        returns pandas.DataFrame indexed by Month with 'Predicted Rainfall (mm)'
        """
        state_fname = state.replace(' ', '_')
        hist_df = self._load_clean_monthly(state_fname)
        if hist_df is None:
            print(f"No cleaned historical file for {state_fname}")
            return None

        if target_year is None:
            # default: next 12 months from history end
            target_year = (hist_df['month_dt'].max() + pd.DateOffset(months=1)).year

        # Try Prophet
        m = self._load_prophet_model(state_fname)
        if m is not None:
            try:
                forecast_df = self._prophet_forecast_for_year(m, hist_df, target_year)
                return forecast_df
            except Exception as e:
                print("Prophet forecast failed (falling back):", e)

        # Fallback
        return self._seasonal_average_forecast(hist_df, target_year)
