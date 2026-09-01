import re

filepath = 'apps/orders/templates/orders/shipping_settings.html'
with open(filepath, 'r') as f:
    content = f.read()

# Fix hidden inputs x-if
old_inputs = """ <!-- Parent IDs -->
 <input x-if="modal.type === 'district' && !modal.isEdit" type="hidden" name="province_id" :value="modal.parentId">
 <input x-if="modal.type === 'city' && !modal.isEdit" type="hidden" name="district_id" :value="modal.parentId">
 
 <!-- Edit IDs -->
 <input x-if="modal.type === 'province' && modal.isEdit" type="hidden" name="province_id" :value="modal.editId">
 <input x-if="modal.type === 'district' && modal.isEdit" type="hidden" name="district_id" :value="modal.editId">
 <input x-if="modal.type === 'city' && modal.isEdit" type="hidden" name="city_id" :value="modal.editId">"""

new_inputs = """ <!-- Parent IDs -->
 <template x-if="modal.type === 'district' && !modal.isEdit"><input type="hidden" name="province_id" :value="modal.parentId"></template>
 <template x-if="modal.type === 'city' && !modal.isEdit"><input type="hidden" name="district_id" :value="modal.parentId"></template>
 
 <!-- Edit IDs -->
 <template x-if="modal.type === 'province' && modal.isEdit"><input type="hidden" name="province_id" :value="modal.editId"></template>
 <template x-if="modal.type === 'district' && modal.isEdit"><input type="hidden" name="district_id" :value="modal.editId"></template>
 <template x-if="modal.type === 'city' && modal.isEdit"><input type="hidden" name="city_id" :value="modal.editId"></template>"""

content = content.replace(old_inputs, new_inputs)

# Fix input fields bg/text color
content = content.replace('class="block w-full border-theme-input-border rounded-xl', 'class="block w-full bg-theme-bg text-theme-text-primary border-theme-input-border rounded-xl')

with open(filepath, 'w') as f:
    f.write(content)
print("Updated shipping_settings.html inputs")
