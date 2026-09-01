import re

filepath = 'apps/orders/templates/orders/shipping_settings.html'
with open(filepath, 'r') as f:
    content = f.read()

# Add button
old_button_html = """ <div class="flex space-x-3">
 <button @click="openModal('province')" class="inline-flex items-center justify-center px-5 py-2.5 border border-transparent rounded-xl shadow-sm text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all">
 <i class="fa-solid fa-plus mr-2"></i> Add Province
 </button>"""

new_button_html = """ <div class="flex space-x-3">
 <button type="button" @click="loadDataModal.isOpen = true; fetchCountries();" class="inline-flex items-center justify-center px-5 py-2.5 border border-theme-input-border rounded-xl shadow-sm text-sm font-bold text-theme-text-secondary bg-theme-surface hover:bg-theme-surface-hover focus:outline-none transition-all">
 <i class="fa-solid fa-cloud-arrow-down mr-2"></i> Load Default Data
 </button>
 <button @click="openModal('province')" class="inline-flex items-center justify-center px-5 py-2.5 border border-transparent rounded-xl shadow-sm text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all">
 <i class="fa-solid fa-plus mr-2"></i> Add Province
 </button>"""

content = content.replace(old_button_html, new_button_html)

# Add Load Default Data Modal before </template> for Universal Modals
modal_insertion_point = " </template>"
load_modal_html = """
 <!-- Load Default Data Modal -->
 <div x-show="loadDataModal.isOpen" class="fixed inset-0 z-[100] overflow-y-auto" style="display: none;">
 <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
 <div class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm" @click="loadDataModal.isOpen = false"></div>
 <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
 <div x-show="loadDataModal.isOpen" x-transition class="inline-block align-bottom bg-theme-surface rounded-2xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-xl w-full relative z-[101]">
 
 <div class="bg-theme-surface px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
 <div class="sm:flex sm:items-start">
 <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 text-indigo-600 sm:mx-0 sm:h-10 sm:w-10">
 <i class="fa-solid fa-earth-americas"></i>
 </div>
 <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
 <h3 class="text-lg leading-6 font-extrabold text-theme-text-primary tracking-tight">Load Country Defaults</h3>
 <p class="text-sm text-theme-text-muted mt-1">Select a country to automatically load its Provinces/States and Districts/Counties.</p>
 
 <div class="mt-5">
 <input type="text" x-model="countrySearch" placeholder="Search for a country..." class="block w-full bg-theme-bg text-theme-text-primary border-theme-input-border rounded-xl focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm shadow-sm mb-4">
 
 <div class="max-h-60 overflow-y-auto border border-theme-border rounded-xl divide-y divide-theme-border">
 <template x-if="countries.length === 0 && !isLoadingCountries">
 <div class="p-4 text-center text-theme-text-muted text-sm">Failed to load countries or none found.</div>
 </template>
 <template x-if="isLoadingCountries">
 <div class="p-4 text-center text-theme-text-muted text-sm"><i class="fa-solid fa-spinner fa-spin mr-2"></i> Fetching countries...</div>
 </template>
 <template x-for="country in filteredCountries" :key="country.iso2">
 <div @click="selectCountry(country)" class="p-3 hover:bg-theme-surface-hover cursor-pointer flex items-center justify-between group transition-colors" :class="{'bg-indigo-50 dark:bg-indigo-900/20': selectedCountry && selectedCountry.iso2 === country.iso2}">
 <div class="flex items-center">
 <span class="text-xl mr-3" x-text="country.emoji"></span>
 <span class="font-bold text-theme-text-primary text-sm" x-text="country.name"></span>
 </div>
 <i class="fa-solid fa-check text-indigo-600 opacity-0 transition-opacity" :class="{'opacity-100': selectedCountry && selectedCountry.iso2 === country.iso2, 'group-hover:opacity-50': !(selectedCountry && selectedCountry.iso2 === country.iso2)}"></i>
 </div>
 </template>
 </div>
 </div>
 </div>
 </div>
 </div>
 <div class="bg-theme-bg px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse rounded-b-2xl border-t border-theme-border-subtle">
 <form method="post" action="{% url 'shipping_settings' %}" class="w-full sm:w-auto sm:ml-3" @submit.prevent="submitCountryLoad($event)">
 {% csrf_token %}
 <input type="hidden" name="action" value="load_default_data">
 <input type="hidden" name="country_iso2" :value="selectedCountry ? selectedCountry.iso2 : ''">
 <input type="hidden" name="country_name" :value="selectedCountry ? selectedCountry.name : ''">
 <button type="submit" :disabled="!selectedCountry || isSubmitting" class="w-full inline-flex justify-center items-center rounded-xl border border-transparent shadow-sm px-6 py-2 bg-indigo-600 text-base font-bold text-white hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed sm:w-auto sm:text-sm transition-all">
 <i x-show="isSubmitting" class="fa-solid fa-spinner fa-spin mr-2" style="display: none;"></i>
 <span x-text="isSubmitting ? 'Loading...' : 'Load Data'"></span>
 </button>
 </form>
 <button type="button" @click="loadDataModal.isOpen = false" class="mt-3 w-full inline-flex justify-center rounded-xl border border-theme-input-border shadow-sm px-6 py-2 bg-theme-surface text-base font-bold text-theme-text-secondary hover:bg-theme-surface-hover sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm transition-all">Cancel</button>
 </div>
 </div>
 </div>
 </div>
 </template>"""

content = content.replace(modal_insertion_point, load_modal_html)

# Add alpine logic to shippingDashboard()
alpine_script_old = """ deleteModal: {
 isOpen: false,
 type: 'province',
 id: null
 },"""

alpine_script_new = """ deleteModal: {
 isOpen: false,
 type: 'province',
 id: null
 },
 
 loadDataModal: {
 isOpen: false
 },
 countries: [],
 countrySearch: '',
 selectedCountry: null,
 isLoadingCountries: false,
 isSubmitting: false,
 
 get filteredCountries() {
 if (!this.countrySearch) return this.countries;
 return this.countries.filter(c => c.name.toLowerCase().includes(this.countrySearch.toLowerCase()));
 },
 
 async fetchCountries() {
 if (this.countries.length > 0) return;
 this.isLoadingCountries = true;
 try {
 // Fetch from the public github DB (dr5hn)
 const res = await fetch('https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/countries.json');
 const data = await res.json();
 this.countries = data.map(c => ({ name: c.name, iso2: c.iso2, emoji: c.emoji }));
 } catch (e) {
 console.error('Failed to load countries', e);
 }
 this.isLoadingCountries = false;
 },
 
 selectCountry(country) {
 this.selectedCountry = country;
 },
 
 submitCountryLoad(e) {
 if (!this.selectedCountry) return;
 this.isSubmitting = true;
 e.target.submit();
 },"""

content = content.replace(alpine_script_old, alpine_script_new)

with open(filepath, 'w') as f:
    f.write(content)
print("Updated shipping_settings.html with load data modal")
