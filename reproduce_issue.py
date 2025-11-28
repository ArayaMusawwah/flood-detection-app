from fuzzy_engine import FuzzyFloodEngine

def test_engine():
    engine = FuzzyFloodEngine()
    
    # Test case from user:
    # Rainfall > 300 (e.g., 350)
    # River Level > 5 (e.g., 6)
    # Duration > 24 (e.g., 25)
    
    cr = 350
    wl = 6
    du = 25
    
    print(f"Testing with inputs: CR={cr}, WL={wl}, DU={du}")
    
    mu_cr, mu_wl, mu_du = engine.fuzzify_sample(cr, wl, du)
    print("Memberships:")
    print(f"CR: {mu_cr}")
    print(f"WL: {mu_wl}")
    print(f"DU: {mu_du}")
    
    active = engine.evaluate_rules(mu_cr, mu_wl, mu_du)
    print(f"Active rules: {len(active)}")
    
    agg = engine.aggregate_and_defuzz(active)
    print("Result:")
    print(f"Flood Val: {agg['flood_val']}")
    print(f"Depth Val: {agg['depth_val']}")

if __name__ == "__main__":
    test_engine()
