from apps.catalog.models import Size, SizeChartRule

class SizeIntelligenceService:
    """
    Recommends sizes based on the user's FitPassport and product measurements.
    """

    @staticmethod
    def recommend_size(fit_passport, product_variant):
        """
        Returns a recommended Size object for the given user and product variant.
        Uses chest and waist measurements mapped to SizeChartRules.
        """
        # Get all sizes available for this variant's product
        available_sizes = Size.objects.filter(productvariant__product=product_variant.product).distinct()
        if not available_sizes.exists():
            return None

        if not fit_passport:
            return available_sizes.first()

        chest = fit_passport.chest_cm
        waist = fit_passport.waist_cm

        if not chest and not waist:
            # Fallback to BMI heuristic if measurements are missing
            height = fit_passport.height_cm
            weight = fit_passport.weight_kg
            if height and weight:
                height_m = height / 100.0
                bmi = weight / (height_m * height_m)
                if bmi < 18.5: target_size_name = 'S'
                elif 18.5 <= bmi < 24.9: target_size_name = 'M'
                elif 24.9 <= bmi < 29.9: target_size_name = 'L'
                else: target_size_name = 'XL'
                return SizeIntelligenceService._adjust_size_and_match(target_size_name, fit_passport.fit_preference, available_sizes)
            return available_sizes.first()

        # Find SizeChartRules for this product type
        rules = SizeChartRule.objects.filter(
            size_chart__product_type=product_variant.product.product_type,
            size_chart__is_active=True
        ).select_related('size')

        if not rules.exists():
            # If no size chart, fallback to M
            return SizeIntelligenceService._adjust_size_and_match('M', fit_passport.fit_preference, available_sizes)

        # Map measurements to size
        best_size = None
        for rule in rules:
            match_chest = True
            match_waist = True
            
            if chest and rule.min_chest_cm and rule.max_chest_cm:
                if not (rule.min_chest_cm <= chest <= rule.max_chest_cm):
                    match_chest = False
            
            if waist and rule.min_waist_cm and rule.max_waist_cm:
                if not (rule.min_waist_cm <= waist <= rule.max_waist_cm):
                    match_waist = False
                    
            if match_chest and match_waist:
                best_size = rule.size.name.upper()
                break
                
        if not best_size:
            # Pick largest matched or fallback to M
            best_size = 'M'
            
        return SizeIntelligenceService._adjust_size_and_match(best_size, fit_passport.fit_preference, available_sizes)

    @staticmethod
    def _adjust_size_and_match(target_size_name, fit_preference, available_sizes):
        sizes_ordered = ['XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL']
        
        try:
            current_index = sizes_ordered.index(target_size_name)
            if fit_preference == 'TIGHT' and current_index > 0:
                target_size_name = sizes_ordered[current_index - 1]
            elif fit_preference == 'LOOSE' and current_index < len(sizes_ordered) - 1:
                target_size_name = sizes_ordered[current_index + 1]
        except ValueError:
            pass

        # Find closest match in available sizes
        for size in available_sizes:
            if size.name.upper() == target_size_name or size.code.upper() == target_size_name:
                return size
                
        # If no size matches target, return the first available size, or None
        return available_sizes.first() if available_sizes.exists() else None
