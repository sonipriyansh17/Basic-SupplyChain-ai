"""
Main Application - Integrates all agents and provides API endpoints
"""
print("🚀 Initializing AI Supply Chain System...")

# Import statements with error handling
try:
    from flask import Flask, jsonify, request
    print("✅ Flask imported successfully")
except Exception as e:
    print(f"❌ Flask import error: {e}")
    exit(1)

try:
    from agents.supplier_agent import SupplierAgent
    print("✅ SupplierAgent imported successfully")
except Exception as e:
    print(f"❌ SupplierAgent import error: {e}")
    exit(1)

try:
    from agents.inventory_agent import InventoryAgent
    print("✅ InventoryAgent imported successfully")
except Exception as e:
    print(f"❌ InventoryAgent import error: {e}")
    exit(1)

try:
    from models.forecast_model import SimpleForecastModel
    print("✅ SimpleForecastModel imported successfully")
except Exception as e:
    print(f"❌ SimpleForecastModel import error: {e}")
    exit(1)

# Initialize Flask app
app = Flask(__name__)
print("✅ Flask app created")

# Initialize agents
supplier_agent = SupplierAgent()
inventory_agent = InventoryAgent()
forecast_model = SimpleForecastModel()
print("✅ All agents initialized")

# Load forecast data
try:
    success = forecast_model.load_data('data/sample_data.csv')
    if success:
        print("✅ Forecast data loaded successfully")
    else:
        print("⚠️  Warning: Could not load forecast data")
except Exception as e:
    print(f"⚠️  Warning: Forecast data loading issue: {e}")

# API Routes
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "AI Supply Chain Optimization System",
        "status": "running",
        "version": "1.0.0",
        "endpoints": [
            "/api/health",
            "/api/suppliers",
            "/api/inventory/optimize",
            "/api/forecast"
        ]
    })

@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    try:
        priority = request.args.get('priority', 'balanced')
        ranked_suppliers = supplier_agent.evaluate_suppliers(priority)
        
        return jsonify({
            "priority": priority,
            "ranked_suppliers": [
                {
                    "id": supplier_id,
                    "score": data['score'],
                    "details": data['details']
                }
                for supplier_id, data in ranked_suppliers
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/inventory/optimize', methods=['POST'])
def optimize_inventory():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        required_fields = ['item_id', 'annual_demand', 'ordering_cost', 'holding_cost']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        result = inventory_agent.optimize_inventory(
            item_id=data['item_id'],
            annual_demand=data['annual_demand'],
            ordering_cost=data['ordering_cost'],
            holding_cost_per_unit=data['holding_cost'],
            lead_time_days=data.get('lead_time', 7),
            daily_std_dev=data.get('daily_std_dev', 5)
        )
        
        return jsonify({
            "status": "success",
            "optimization_result": result
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    try:
        method = request.args.get('method', 'moving_average')
        periods = request.args.get('periods', default=30, type=int)
        periods = min(periods, 90)  # Limit to 90 days
        
        if method == 'seasonal' and forecast_model.data is not None:
            forecast = forecast_model.seasonal_forecast(periods)
        else:
            forecast = forecast_model.moving_average_forecast(periods=periods)
        
        trend = forecast_model.get_trend_analysis()
        
        return jsonify({
            "method": method,
            "periods": periods,
            "forecast": [
                {
                    "date": date,
                    "predicted_demand": forecast_val,
                    "confidence_lower": lower,
                    "confidence_upper": upper
                }
                for date, forecast_val, lower, upper in 
                zip(forecast['dates'], forecast['forecast'], 
                    forecast['confidence_lower'], forecast['confidence_upper'])
            ],
            "trend_analysis": trend
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "system": "AI Supply Chain Optimization",
        "timestamp": "now"
    })

# This is crucial - it tells Python what to do when run directly
if __name__ == '__main__':
    print("=" * 60)
    print("🚀 AI Supply Chain Optimization System Starting...")
    print("=" * 60)
    print("✅ System Components:")
    print("   - Supplier Agent: Active")
    print("   - Inventory Agent: Active")
    print("   - Forecast Model: Active")
    print("\n🌐 Available API Endpoints:")
    print("   GET  /                     - System info")
    print("   GET  /api/health           - Health check")
    print("   GET  /api/suppliers        - Supplier evaluation")
    print("   POST /api/inventory/optimize - Inventory optimization")
    print("   GET  /api/forecast         - Demand forecasting")
    print("\n🔧 Starting server on http://127.0.0.1:5000")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start the Flask server
    try:
        app.run(host='127.0.0.1', port=5000, debug=True)
    except Exception as e:
        print(f"❌ Server failed to start: {e}")