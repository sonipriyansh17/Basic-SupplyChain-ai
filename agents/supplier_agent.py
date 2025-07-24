"""
Supplier Agent - Evaluates and ranks suppliers based on multiple criteria
"""

class SupplierAgent:
    def __init__(self):
        # Mock supplier database
        self.suppliers = {
            'supplier_a': {
                'name': 'Global Parts Co.',
                'cost': 10,  # Lower is better (1-10 scale)
                'quality': 8,  # Higher is better (1-10 scale)
                'delivery': 9,  # Higher is better (1-10 scale)
                'reliability': 7,
                'lead_time': 5  # Days
            },
            'supplier_b': {
                'name': 'Premium Suppliers Inc.',
                'cost': 12,
                'quality': 9,
                'delivery': 7,
                'reliability': 8,
                'lead_time': 3
            },
            'supplier_c': {
                'name': 'Budget Components Ltd.',
                'cost': 8,
                'quality': 6,
                'delivery': 8,
                'reliability': 6,
                'lead_time': 7
            }
        }
    
    def evaluate_suppliers(self, priority='balanced'):
        """
        Evaluate suppliers based on different priorities
        priority: 'cost', 'quality', 'delivery', or 'balanced'
        """
        scores = {}
        
        for supplier_id, metrics in self.suppliers.items():
            if priority == 'cost':
                # Cost-focused: lower cost gets higher score
                score = (10 - metrics['cost']) * 0.6 + metrics['quality'] * 0.2 + metrics['delivery'] * 0.2
            elif priority == 'quality':
                # Quality-focused
                score = metrics['quality'] * 0.6 + metrics['delivery'] * 0.2 + (10 - metrics['cost']) * 0.2
            elif priority == 'delivery':
                # Delivery-focused
                score = metrics['delivery'] * 0.6 + metrics['quality'] * 0.2 + (10 - metrics['cost']) * 0.2
            else:  # balanced
                # Balanced scoring
                score = (10 - metrics['cost']) * 0.3 + metrics['quality'] * 0.3 + metrics['delivery'] * 0.2 + metrics['reliability'] * 0.2
            
            scores[supplier_id] = {
                'score': round(score, 2),
                'details': metrics
            }
        
        # Sort by score (highest first)
        ranked_suppliers = sorted(scores.items(), key=lambda x: x[1]['score'], reverse=True)
        return ranked_suppliers
    
    def get_best_supplier(self, priority='balanced'):
        """Get the single best supplier"""
        ranked = self.evaluate_suppliers(priority)
        return ranked[0] if ranked else None
    
    def add_supplier(self, supplier_id, metrics):
        """Add a new supplier"""
        self.suppliers[supplier_id] = metrics

# Test the agent
if __name__ == "__main__":
    agent = SupplierAgent()
    print("=== Supplier Evaluation Results ===")
    print("\nBalanced Ranking:")
    for supplier, data in agent.evaluate_suppliers('balanced'):
        print(f"{supplier}: {data['score']} points")