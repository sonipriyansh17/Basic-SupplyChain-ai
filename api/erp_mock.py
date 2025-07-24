"""
ERP Mock API - Simulates ERP system data endpoints
"""
from flask import Flask, jsonify
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

class ERPMockAPI:
    def __init__(self):
        self.suppliers = {
            "SUP001": {"name": "Global Parts Co.", "status": "active", "rating": 4.5},
            "SUP002": {"name": "Premium Suppliers Inc.", "status": "active", "rating": 4.8},
            "SUP003": {"name": "Budget Components Ltd.", "status": "active", "rating": 3.9}
        }
        
        self.products = {
            "PROD001": {"name": "Widget A", "category": "Electronics", "unit_cost": 25.50},
            "PROD002": {"name": "Gadget B", "category": "Hardware", "unit_cost": 18.75},
            "PROD003": {"name": "Tool C", "category": "Tools", "unit_cost": 32.00}
        }
        
        self.inventory = {
            "PROD001": {"current_stock": 500, "reserved": 50, "available": 450},
            "PROD002": {"current_stock": 300, "reserved": 30, "available": 270},
            "PROD003": {"current_stock": 150, "reserved": 15, "available": 135}
        }
    
    def get_sales_data(self, days=30):
        """Generate mock sales data"""
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') 
                for i in range(days-1, -1, -1)]
        
        # Generate realistic sales data with some variation
        base_sales = 100
        sales_data = []
        
        for date in dates:
            # Add some randomness and weekend pattern
            day_of_week = datetime.strptime(date, '%Y-%m-%d').weekday()
            weekend_factor = 0.7 if day_of_week >= 5 else 1.0
            daily_sales = int(base_sales * weekend_factor * (0.8 + 0.4 * (hash(date) % 100) / 100))
            sales_data.append({"date": date, "sales": daily_sales})
        
        return sales_data

# Initialize ERP mock
erp = ERPMockAPI()

@app.route('/api/erp/suppliers', methods=['GET'])
def get_suppliers():
    return jsonify(erp.suppliers)

@app.route('/api/erp/products', methods=['GET'])
def get_products():
    return jsonify(erp.products)

@app.route('/api/erp/inventory', methods=['GET'])
def get_inventory():
    return jsonify(erp.inventory)

@app.route('/api/erp/sales/<int:days>', methods=['GET'])
def get_sales_data(days=30):
    sales_data = erp.get_sales_data(min(days, 90))  # Limit to 90 days max
    return jsonify(sales_data)

@app.route('/api/erp/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

# Test endpoints
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "ERP Mock API is running",
        "endpoints": [
            "/api/erp/suppliers",
            "/api/erp/products", 
            "/api/erp/inventory",
            "/api/erp/sales/{days}",
            "/api/erp/health"
        ]
    })

if __name__ == '__main__':
    print("🚀 Starting ERP Mock API Server...")
    print("Available endpoints:")
    print("  http://localhost:5001/api/erp/suppliers")
    print("  http://localhost:5001/api/erp/products")
    print("  http://localhost:5001/api/erp/inventory")
    print("  http://localhost:5001/api/erp/sales/30")
    print("  http://localhost:5001/api/erp/health")
    app.run(host='0.0.0.0', port=5001, debug=True)