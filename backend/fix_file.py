import re

filepath = 'apps/orders/templates/orders/shipping_settings.html'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Clean up duplicated "Load Default Data" buttons in the header
# We'll just replace the entire header action block to be sure
old_header_start = ' <div class="mb-8 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">'
old_header_end = ' </div>\n </div>'
header_match = re.search(re.escape(old_header_start) + r'.*?' + re.escape(old_header_end), content, re.DOTALL)
if header_match:
    clean_header = """ <div class="mb-8 flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
 <div>
 <h1 class="text-4xl font-extrabold text-theme-text-primary tracking-tight">Delivery <span class="text-indigo-600 font-light">Locations</span></h1>
 <p class="text-theme-text-muted mt-2 text-sm font-medium">Configure a strict hierarchy of Provinces, Districts, and Cities to manage precise delivery routing and pricing.</p>
 </div>
 <div class="flex space-x-3">
 <button type="button" @click="loadDataModal.isOpen = true; fetchCountries();" class="inline-flex items-center justify-center px-5 py-2.5 border border-theme-input-border rounded-xl shadow-sm text-sm font-bold text-theme-text-secondary bg-theme-surface hover:bg-theme-surface-hover focus:outline-none transition-all">
 <i class="fa-solid fa-cloud-arrow-down mr-2"></i> Load Default Data
 </button>
 <button @click="openModal('province')" class="inline-flex items-center justify-center px-5 py-2.5 border border-transparent rounded-xl shadow-sm text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all">
 <i class="fa-solid fa-plus mr-2"></i> Add Province
 </button>
 </div>
 </div>"""
    content = content[:header_match.start()] + clean_header + content[header_match.end():]

# 2. Re-write the Universal Modals block and put it INSIDE the x-data div
# Find where x-teleport starts
teleport_start = content.find('<!-- Universal Modals -->')
if teleport_start != -1:
    # Find where the script starts
    script_start = content.find('<!-- Alpine.js Plugin for Collapse -->', teleport_start)
    if script_start != -1:
        # we will extract everything between teleport_start and script_start
        content = content[:teleport_start] + content[script_start:]

# Now, we know that before <!-- Alpine.js Plugin for Collapse -->, we should have the closing </div> for x-data.
# But since we might have messed up the </div> count, let's just count them.
# A much safer way is to rewrite the bottom half of the file.
