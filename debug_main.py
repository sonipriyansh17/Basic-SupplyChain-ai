"""
Debug version of main application
"""
print("Starting debug...")

try:
    from flask import Flask, jsonify, request
    print("✅ Flask imported successfully")
except Exception as e:
    print(f"❌ Flask import error: {e}")

try:
    from agents.supplier_agent import SupplierAgent
    print("✅ SupplierAgent imported successfully")
except Exception as e:
    print(f"❌ SupplierAgent import error: {e}")

try:
    from agents.inventory_agent import InventoryAgent
    print("✅ InventoryAgent imported successfully")
except Exception as e:
    print(f"❌ InventoryAgent import error: {e}")

try:
    from models.forecast_model import SimpleForecastModel
    print("✅ SimpleForecastModel imported successfully")
except Exception as e:
    print(f"❌ SimpleForecastModel import error: {e}")

print("Debug complete!")