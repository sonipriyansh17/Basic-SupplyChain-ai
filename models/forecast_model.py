"""
Forecast Model - Simple demand forecasting using moving averages
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class SimpleForecastModel:
    def __init__(self):
        self.data = None
    
    def load_data(self, csv_file):
        """Load historical demand data"""
        try:
            self.data = pd.read_csv(csv_file)
            self.data['date'] = pd.to_datetime(self.data['date'])
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def moving_average_forecast(self, window=7, periods=30):
        """
        Simple moving average forecast
        window: number of days to average
        periods: number of future periods to forecast
        """
        if self.data is None:
            return None
        
        # Get the last 'window' days of data
        recent_data = self.data['demand'].tail(window).values
        avg_demand = np.mean(recent_data)
        
        # Generate forecast dates
        last_date = self.data['date'].max()
        forecast_dates = [(last_date + timedelta(days=i+1)).strftime('%Y-%m-%d') 
                         for i in range(periods)]
        
        # Create forecast (same average for all periods)
        forecast = {
            'dates': forecast_dates,
            'forecast': [round(avg_demand) for _ in range(periods)],
            'confidence_lower': [round(avg_demand * 0.8) for _ in range(periods)],
            'confidence_upper': [round(avg_demand * 1.2) for _ in range(periods)]
        }
        
        return forecast
    
    def seasonal_forecast(self, periods=30):
        """
        Simple seasonal forecast based on day of week patterns
        """
        if self.data is None:
            return None
        
        # Calculate average demand by day of week
        self.data['day_of_week'] = self.data['date'].dt.dayofweek
        daily_avg = self.data.groupby('day_of_week')['demand'].mean()
        
        # Generate forecast
        last_date = self.data['date'].max()
        forecast_dates = []
        forecast_values = []
        
        for i in range(periods):
            next_date = last_date + timedelta(days=i+1)
            day_of_week = next_date.weekday()
            avg_demand = daily_avg[day_of_week]
            
            forecast_dates.append(next_date.strftime('%Y-%m-%d'))
            forecast_values.append(round(avg_demand))
        
        return {
            'dates': forecast_dates,
            'forecast': forecast_values,
            'confidence_lower': [round(val * 0.8) for val in forecast_values],
            'confidence_upper': [round(val * 1.2) for val in forecast_values]
        }
    
    def get_trend_analysis(self):
        """Simple trend analysis"""
        if self.data is None or len(self.data) < 2:
            return "Insufficient data"
        
        # Calculate trend using linear regression
        y = self.data['demand'].values
        x = np.arange(len(y))
        
        # Simple slope calculation
        slope = (y[-1] - y[0]) / len(y) if len(y) > 0 else 0
        
        if slope > 0:
            trend = "📈 Increasing"
        elif slope < 0:
            trend = "📉 Decreasing"
        else:
            trend = "➡️  Stable"
        
        return {
            'trend': trend,
            'slope': round(slope, 2),
            'avg_demand': round(np.mean(y), 2)
        }

# Test the model
if __name__ == "__main__":
    model = SimpleForecastModel()
    
    print("=== Demand Forecasting Demo ===")
    
    # Load sample data
    if model.load_data('data/sample_data.csv'):
        print("✅ Data loaded successfully")
        
        # Moving average forecast
        ma_forecast = model.moving_average_forecast(window=7, periods=5)
        print(f"\nMoving Average Forecast (next 5 days):")
        for i, (date, forecast) in enumerate(zip(ma_forecast['dates'], ma_forecast['forecast'])):
            print(f"  {date}: {forecast} units")
        
        # Trend analysis
        trend = model.get_trend_analysis()
        print(f"\nTrend Analysis: {trend['trend']}")
        print(f"Average Demand: {trend['avg_demand']} units/day")
    else:
        print("❌ Failed to load data")