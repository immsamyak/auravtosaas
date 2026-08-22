import time
import hashlib

def analyze_body_proportions(image_file_path):
    """
    Computer Vision sizing function (Fallback Mode).
    Uses file path hashing to deterministically generate measurements
    until the production ML endpoint is fully integrated.
    """
    # Deterministic generation based on file path to simulate consistent ML output
    hash_val = int(hashlib.md5(str(image_file_path).encode('utf-8')).hexdigest(), 16)
    
    # Map hash to realistic ranges
    shoulder = 38.0 + (hash_val % 120) / 10.0 # 38 - 50
    chest = 85.0 + (hash_val % 250) / 10.0 # 85 - 110
    waist = 70.0 + (hash_val % 300) / 10.0 # 70 - 100
    
    seasons = ['Winter', 'Autumn', 'Spring', 'Summer']
    color_season = seasons[hash_val % 4]
    
    return {
        "shoulder_width_cm": round(shoulder, 1),
        "chest_cm": round(chest, 1),
        "waist_cm": round(waist, 1),
        "skin_tone_category": color_season
    }

def get_size_recommendation(consumer_profile, product):
    """
    Real recommendation engine.
    Compares the ConsumerProfile measurements to the product's SizeChartRules.
    """
    from apps.catalog.models import SizeChartRule
    
    if not consumer_profile or not consumer_profile.chest_cm or not consumer_profile.waist_cm:
        return None, "Profile measurements incomplete"
        
    rules = SizeChartRule.objects.filter(
        size_chart__brand=product.brand,
        size_chart__product_type=product.product_type,
        size_chart__is_active=True
    )
    
    if not rules.exists():
        return None, "No active size chart found for this product type"
        
    for rule in rules.order_by('size__display_order'):
        chest_matches = True
        waist_matches = True
        
        if rule.min_chest_cm and consumer_profile.chest_cm < rule.min_chest_cm:
            chest_matches = False
        if rule.max_chest_cm and consumer_profile.chest_cm > rule.max_chest_cm:
            chest_matches = False
            
        if rule.min_waist_cm and consumer_profile.waist_cm < rule.min_waist_cm:
            waist_matches = False
        if rule.max_waist_cm and consumer_profile.waist_cm > rule.max_waist_cm:
            waist_matches = False
            
        if chest_matches and waist_matches:
            return rule.size, "True to Size"
            
    # If no strict match, fallback to finding closest size by chest measurement
    # (Simple heuristic for demonstration)
    closest_rule = None
    min_diff = float('inf')
    for rule in rules:
        if rule.min_chest_cm and rule.max_chest_cm:
            midpoint = (rule.min_chest_cm + rule.max_chest_cm) / 2
            diff = abs(consumer_profile.chest_cm - midpoint)
            if diff < min_diff:
                min_diff = diff
                closest_rule = rule
                
    if closest_rule:
        return closest_rule.size, "Recommended based on closest chest measurement"
        
    return None, "Could not determine size"
