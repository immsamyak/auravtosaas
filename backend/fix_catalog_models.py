filepath = 'apps/catalog/models.py'
with open(filepath, 'r') as f:
    content = f.read()

target_product = """    @property
    def avg_rating(self):
        reviews = self.reviews.filter(status='APPROVED')
        if not reviews:
            return 0
        return sum([r.rating for r in reviews]) / reviews.count()"""

replacement_product = """    @property
    def total_stock(self):
        return sum(v.total_stock for v in self.variants.all())

    @property
    def avg_rating(self):
        reviews = self.reviews.filter(status='APPROVED')
        if not reviews:
            return 0
        return sum([r.rating for r in reviews]) / reviews.count()"""

if target_product in content:
    content = content.replace(target_product, replacement_product)

with open(filepath, 'w') as f:
    f.write(content)
