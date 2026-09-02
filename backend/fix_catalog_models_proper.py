filepath = 'apps/catalog/models.py'
with open(filepath, 'r') as f:
    content = f.read()

target = """        if self.pk and self.brand:
            self.seo_title = self.seo_title or f"{self.name} - {self.brand.name}"
        super().save(*args, **kwargs)"""

replacement = """        if self.pk and self.brand:
            self.seo_title = self.seo_title or f"{self.name} - {self.brand.name}"
        super().save(*args, **kwargs)

    @property
    def total_stock(self):
        return sum(v.total_stock for v in self.variants.all())"""

if target in content:
    content = content.replace(target, replacement)

with open(filepath, 'w') as f:
    f.write(content)
