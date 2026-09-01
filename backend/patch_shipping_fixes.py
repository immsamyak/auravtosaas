import re

filepath = 'apps/orders/templates/orders/shipping_settings.html'
with open(filepath, 'r') as f:
    content = f.read()

# Fix Delete Modal hidden inputs x-if
old_delete_inputs = """ <input type="hidden" name="action" :value="'delete_' + deleteModal.type">
 <input x-if="deleteModal.type === 'province'" type="hidden" name="province_id" :value="deleteModal.id">
 <input x-if="deleteModal.type === 'district'" type="hidden" name="district_id" :value="deleteModal.id">
 <input x-if="deleteModal.type === 'city'" type="hidden" name="city_id" :value="deleteModal.id">"""

new_delete_inputs = """ <input type="hidden" name="action" :value="'delete_' + deleteModal.type">
 <template x-if="deleteModal.type === 'province'"><input type="hidden" name="province_id" :value="deleteModal.id"></template>
 <template x-if="deleteModal.type === 'district'"><input type="hidden" name="district_id" :value="deleteModal.id"></template>
 <template x-if="deleteModal.type === 'city'"><input type="hidden" name="city_id" :value="deleteModal.id"></template>"""

content = content.replace(old_delete_inputs, new_delete_inputs)

# Fix Input field padding/height
# Let's add px-4 py-2.5 to give it proper height
content = content.replace('class="block w-full bg-theme-bg text-theme-text-primary border-theme-input-border rounded-xl focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm shadow-sm"', 
                          'class="block w-full bg-theme-bg text-theme-text-primary border-theme-input-border rounded-xl px-4 py-2.5 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm shadow-sm"')
content = content.replace('class="block w-full bg-theme-bg text-theme-text-primary border-theme-input-border rounded-xl focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm shadow-sm mb-4"',
                          'class="block w-full bg-theme-bg text-theme-text-primary border-theme-input-border rounded-xl px-4 py-2.5 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm shadow-sm mb-4"')

with open(filepath, 'w') as f:
    f.write(content)
print("Updated shipping_settings.html fixes")
