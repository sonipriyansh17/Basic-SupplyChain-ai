"""
Inventory Agent - Optimizes inventory levels and reorder points
"""
import math

class InventoryAgent:
    def __init__(self):
        self.inventory_levels = {}
        self.safety_stock_multiplier = 1.65  # 95% service level
    
    def eoq_calculate(self, annual_demand, ordering_cost, holding_cost_per_unit):
        """
        Economic Order Quantity calculation
        EOQ = √(2DS/H) where D=demand, S=ordering cost, H=holding cost
        """
        if holding_cost_per_unit <= 0 or annual_demand <= 0:
            return 0
        
        eoq = math.sqrt((2 * annual_demand * ordering_cost) / holding_cost_per_unit)
        return round(eoq)
    
    def reorder_point(self, daily_demand, lead_time_days, daily_demand_std_dev=0):
        """
        Calculate reorder point
        ROP = (Daily Demand × Lead Time) + Safety Stock
        """
        expected_demand = daily_demand * lead_time_days
        safety_stock = self.safety_stock_multiplier * daily_demand_std_dev * math.sqrt(lead_time_days)
        return round(expected_demand + safety_stock)
    
    def optimize_inventory(self, item_id, annual_demand, ordering_cost, holding_cost_per_unit, lead_time_days=7, daily_std_dev=5):
        """
        Complete inventory optimization for an item
        """
        # Calculate daily demand
        daily_demand = annual_demand / 365
        
        # Calculate EOQ
        eoq = self.eoq_calculate(annual_demand, ordering_cost, holding_cost_per_unit)
        
        # Calculate reorder point
        rop = self.reorder_point(daily_demand, lead_time_days, daily_std_dev)
        
        # Calculate number of orders per year
        orders_per_year = annual_demand / eoq if eoq > 0 else 0
        
        # Calculate total inventory cost
        total_cost = (ordering_cost * orders_per_year) + (holding_cost_per_unit * eoq / 2)
        
        result = {
            'item_id': item_id,
            'optimal_order_quantity': eoq,
            'reorder_point': rop,
            'annual_orders': round(orders_per_year, 2),
            'total_annual_cost': round(total_cost, 2),
            'daily_demand': round(daily_demand, 2),
            'lead_time_days': lead_time_days
        }
        
        # Store in inventory levels
        self.inventory_levels[item_id] = result
        
        return result
    
    def check_inventory_status(self, item_id, current_stock):
        """Check if inventory needs reordering"""
        if item_id not in self.inventory_levels:
            return "No optimization data available"
        
        reorder_point = self.inventory_levels[item_id]['reorder_point']
        
        if current_stock <= reorder_point:
            return f"⚠️  REORDER NEEDED! Current: {current_stock}, ROP: {reorder_point}"
        else:
            return f"✅ Stock OK. Current: {current_stock}, ROP: {reorder_point}"
    
    def get_inventory_summary(self):
        """Get summary of all optimized items"""
        return self.inventory_levels

# Test the agent
if __name__ == "__main__":
    agent = InventoryAgent()
    
    print("=== Inventory Optimization Demo ===")
    
    # Optimize for a sample item
    result = agent.optimize_inventory(
        item_id="PART_001",
        annual_demand=10000,
        ordering_cost=50,
        holding_cost_per_unit=2,
        lead_time_days=5,
        daily_std_dev=10
    )
    
    print(f"Item ID: {result['item_id']}")
    print(f"Optimal Order Quantity: {result['optimal_order_quantity']} units")
    print(f"Reorder Point: {result['reorder_point']} units")
    print(f"Annual Orders: {result['annual_orders']}")
    print(f"Total Annual Cost: ${result['total_annual_cost']}")
    
    # Check inventory status
    print(f"\nInventory Check: {agent.check_inventory_status('PART_001', 150)}")
    print(f"Inventory Check: {agent.check_inventory_status('PART_001', 50)}")