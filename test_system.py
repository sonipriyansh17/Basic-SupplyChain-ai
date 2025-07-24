"""
Test Script - Test all components of the supply chain system
"""
import requests
import json

BASE_URL = 'http://localhost:5000'
ERP_URL = 'http://localhost:5001'

def test_main_api():
    print("🧪 Testing Main API System")
    print("=" * 50)
    
    try:
        # Test health check
        response = requests.get(f'{BASE_URL}/api/health')
        if response.status_code == 200:
            print("✅ Health Check: PASSED")
        else:
            print("❌ Health Check: FAILED")
        
        # Test supplier evaluation
        response = requests.get(f'{BASE_URL}/api/suppliers?priority=quality')
        if response.status_code == 200:
            suppliers = response.json()
            print(f"✅ Supplier Evaluation: PASSED ({len(suppliers['ranked_suppliers'])} suppliers)")
        else:
            print("❌ Supplier Evaluation: FAILED")
        
        # Test inventory optimization
        inventory_data = {
            "item_id": "TEST_ITEM",
            "annual_demand": 10000,
            "ordering_cost": 50,
            "holding_cost": 2
        }
        response = requests.post(f'{BASE_URL}/api/inventory/optimize', json=inventory_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Inventory Optimization: PASSED (EOQ: {result['optimization_result']['optimal_order_quantity']})")
        else:
            print("❌ Inventory Optimization: FAILED")
        
        # Test forecasting
        response = requests.get(f'{BASE_URL}/api/forecast?periods=5')
        if response.status_code == 200:
            forecast = response.json()
            print(f"✅ Forecasting: PASSED ({len(forecast['forecast'])} days forecast)")
        else:
            print("❌ Forecasting: FAILED")
        
        # Test demo
        response = requests.get(f'{BASE_URL}/api/demo')
        if response.status_code == 200:
            print("✅ Demo Endpoint: PASSED")
        else:
            print("❌ Demo Endpoint: FAILED")
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Main API Server not running. Start with: python main.py")
    except Exception as e:
        print(f"❌ Test Error: {e}")

def test_erp_api():
    print("\n🧪 Testing ERP Mock API")
    print("=" * 50)
    
    try:
        # Test ERP health
        response = requests.get(f'{ERP_URL}/api/erp/health')
        if response.status_code == 200:
            print("✅ ERP Health Check: PASSED")
        else:
            print("❌ ERP Health Check: FAILED")
        
        # Test ERP endpoints
        endpoints = ['/api/erp/suppliers', '/api/erp/products', '/api/erp/inventory', '/api/erp/sales/7']
        for endpoint in endpoints:
            response = requests.get(f'{ERP_URL}{endpoint}')
            if response.status_code == 200:
                print(f"✅ {endpoint}: PASSED")
            else:
                print(f"❌ {endpoint}: FAILED")
                
    except requests.exceptions.ConnectionError:
        print("⚠️  ERP Mock API Server not running. Start with: python api/erp_mock.py")
    except Exception as e:
        print(f"❌ ERP Test Error: {e}")

def run_demo_scenario():
    print("\n🎯 Running Demo Scenario")
    print("=" * 50)
    
    try:
        # 1. Get supplier recommendations
        print("1. Supplier Evaluation (Quality Priority):")
        response = requests.get(f'{BASE_URL}/api/suppliers?priority=quality')
        if response.status_code == 200:
            suppliers = response.json()['ranked_suppliers']
            for supplier in suppliers[:2]:
                print(f"   🏆 {supplier['details']['name']}: {supplier['score']} points")
        
        # 2. Optimize inventory
        print("\n2. Inventory Optimization:")
        inventory_data = {
            "item_id": "WIDGET_A",
            "annual_demand": 15000,
            "ordering_cost": 75,
            "holding_cost": 3,
            "lead_time": 5,
            "daily_std_dev": 15
        }
        response = requests.post(f'{BASE_URL}/api/inventory/optimize', json=inventory_data)
        if response.status_code == 200:
            result = response.json()['optimization_result']
            print(f"   📦 Optimal Order Quantity: {result['optimal_order_quantity']} units")
            print(f"   🔄 Reorder Point: {result['reorder_point']} units")
            print(f"   💰 Annual Cost: ${result['total_annual_cost']}")
        
        # 3. Demand forecasting
        print("\n3. Demand Forecast (Next 5 Days):")
        response = requests.get(f'{BASE_URL}/api/forecast?periods=5&method=seasonal')
        if response.status_code == 200:
            forecast = response.json()['forecast']
            for day in forecast:
                print(f"   📅 {day['date']}: {day['predicted_demand']} units (±{day['confidence_upper']-day['predicted_demand']})")
        
        # 4. Check inventory status
        print("\n4. Inventory Status Check:")
        response = requests.get(f'{BASE_URL}/api/inventory/check?item_id=WIDGET_A&stock=200')
        if response.status_code == 200:
            status = response.json()['status']
            print(f"   {status}")
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Servers not running. Start both servers first!")
    except Exception as e:
        print(f"❌ Demo Error: {e}")

if __name__ == "__main__":
    print("🚀 AI Supply Chain Optimization System - Test Suite")
    print("=" * 60)
    
    # Run all tests
    test_main_api()
    test_erp_api()
    run_demo_scenario()
    
    print("\n📋 Quick Start Commands:")
    print("   Terminal 1: python main.py          # Start main API")
    print("   Terminal 2: python api/erp_mock.py  # Start ERP mock")
    print("   Terminal 3: python test_system.py   # Run tests")