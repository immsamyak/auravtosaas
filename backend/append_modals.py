import re

filepath = 'apps/orders/templates/orders/shipping_settings.html'
with open(filepath, 'a') as f:
    f.write("""<!-- Universal Modals -->
 <template x-teleport="body">
 
 <!-- Add/Edit Modal -->
 <div x-show="modal.isOpen" class="fixed inset-0 z-[100] overflow-y-auto" style="display: none;">
 <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
 <div class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm" @click="closeModal()"></div>
 <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
 <div x-show="modal.isOpen" x-transition class="inline-block align-bottom bg-theme-surface rounded-2xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg w-full relative z-[101]">
 
 <form method="post" action="{% url 'shipping_settings' %}">
 {% csrf_token %}
 <input type="hidden" name="action" :value="modal.isEdit ? 'edit_' + modal.type : 'add_' + modal.type">
 
 <!-- Parent IDs -->
 <template x-if="modal.type === 'district' && !modal.isEdit"><input type="hidden" name="province_id" :value="modal.parentId"></template>
 <template x-if="modal.type === 'city' && !modal.isEdit"><input type="hidden" name="district_id" :value="modal.parentId"></template>
 
 <!-- Edit IDs -->
 <template x-if="modal.type === 'province' && modal.isEdit"><input type="hidden" name="province_id" :value="modal.editId"></template>
 <template x-if="modal.type === 'district' && modal.isEdit"><input type="hidden" name="district_id" :value="modal.editId"></template>
 <template x-if="modal.type === 'city' && modal.isEdit"><input type="hidden" name="city_id" :value="modal.editId"></template>
 
 <div class="bg-theme-surface px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
 <div class="sm:flex sm:items-start">
 <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 text-indigo-600 sm:mx-0 sm:h-10 sm:w-10">
 <i class="fa-solid fa-map-location-dot"></i>
 </div>
 <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
 <h3 class="text-lg leading-6 font-extrabold text-theme-text-primary tracking-tight">
 <span x-text="modal.isEdit ? 'Edit' : 'Add'"></span> <span class="capitalize" x-text="modal.type"></span>
 </h3>
 <div class="mt-5 space-y-4">
 
 <div>
 <label class="block text-sm font-bold text-theme-text-secondary mb-1">Name</label>
 <input type="text" name="name" x-model="modal.name" required class="block w-full bg-theme-bg text-theme-text-primary border-theme-input-border rounded-xl px-4 py-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm shadow-sm" placeholder="e.g. Kathmandu">
 </div>
 
 <!-- City Specific Fields (Pricing) -->
 <template x-if="modal.type === 'city'">
 <div class="space-y-4 mt-4 pt-4 border-t border-theme-border-subtle">
 
 <div>
 <label class="block text-sm font-bold text-theme-text-secondary mb-1">Delivery Rate ({{ brand.currency_symbol|default:"Rs." }})</label>
 <input type="number" step="0.01" name="rate" x-model="modal.rate" required class="block w-full bg-theme-bg text-theme-text-primary border-theme-input-border rounded-xl px-4 py-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm shadow-sm">
 </div>
 
 <div>
 <label class="block text-sm font-bold text-theme-text-secondary mb-1">Estimated Days</label>
 <input type="text" name="estimated_days" x-model="modal.estimated_days" placeholder="e.g. 1-2 Days" class="block w-full bg-theme-bg text-theme-text-primary border-theme-input-border rounded-xl px-4 py-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm shadow-sm">
 </div>
 
 <div>
 <label class="block text-sm font-bold text-theme-text-secondary mb-1">Free Delivery Above ({{ brand.currency_symbol|default:"Rs." }}) (Optional)</label>
 <input type="number" step="0.01" name="is_free_above" x-model="modal.is_free_above" class="block w-full bg-theme-bg text-theme-text-primary border-theme-input-border rounded-xl px-4 py-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm shadow-sm">
 </div>
 
 <div class="flex items-center mt-2">
 <input type="checkbox" name="is_active" id="is_active" x-model="modal.is_active" class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-theme-input-border rounded">
 <label for="is_active" class="ml-2 block text-sm font-bold text-theme-text-secondary">Zone is Active</label>
 </div>
 </div>
 </template>
 
 </div>
 </div>
 </div>
 </div>
 <div class="bg-theme-bg px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse rounded-b-2xl border-t border-theme-border-subtle">
 <button type="submit" class="w-full inline-flex justify-center rounded-xl border border-transparent shadow-sm px-6 py-2 bg-indigo-600 text-base font-bold text-white hover:bg-indigo-700 sm:ml-3 sm:w-auto sm:text-sm">
 <span x-text="modal.isEdit ? 'Save Changes' : 'Create'"></span>
 </button>
 <button type="button" @click="closeModal()" class="mt-3 w-full inline-flex justify-center rounded-xl border border-theme-input-border shadow-sm px-6 py-2 bg-theme-surface text-base font-bold text-theme-text-secondary hover:bg-theme-surface-hover sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">Cancel</button>
 </div>
 </form>
 </div>
 </div>
 </div>

 <!-- Delete Modal -->
 <div x-show="deleteModal.isOpen" class="fixed inset-0 z-[100] overflow-y-auto" style="display: none;">
 <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
 <div class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm" @click="deleteModal.isOpen = false"></div>
 <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
 <div x-show="deleteModal.isOpen" x-transition class="inline-block align-bottom bg-theme-surface rounded-2xl text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg w-full relative z-[101]">
 
 <form method="post" action="{% url 'shipping_settings' %}">
 {% csrf_token %}
 <input type="hidden" name="action" :value="'delete_' + deleteModal.type">
 <template x-if="deleteModal.type === 'province'"><input type="hidden" name="province_id" :value="deleteModal.id"></template>
 <template x-if="deleteModal.type === 'district'"><input type="hidden" name="district_id" :value="deleteModal.id"></template>
 <template x-if="deleteModal.type === 'city'"><input type="hidden" name="city_id" :value="deleteModal.id"></template>
 
 <div class="bg-theme-surface px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
 <div class="sm:flex sm:items-start">
 <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-rose-100 sm:mx-0 sm:h-10 sm:w-10">
 <i class="fa-solid fa-triangle-exclamation text-rose-600"></i>
 </div>
 <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
 <h3 class="text-lg leading-6 font-extrabold text-theme-text-primary">Delete <span class="capitalize" x-text="deleteModal.type"></span></h3>
 <div class="mt-2">
 <p class="text-sm text-theme-text-muted font-medium">Are you sure you want to delete this <span x-text="deleteModal.type"></span>? <span x-show="deleteModal.type !== 'city'">All children locations inside it will also be permanently deleted!</span> This action cannot be undone.</p>
 </div>
 </div>
 </div>
 </div>
 <div class="bg-theme-bg px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse rounded-b-2xl border-t border-theme-border-subtle">
 <button type="submit" class="w-full inline-flex justify-center rounded-xl border border-transparent shadow-sm px-4 py-2 bg-rose-600 text-base font-bold text-white hover:bg-rose-700 sm:ml-3 sm:w-auto sm:text-sm">Delete Permanently</button>
 <button type="button" @click="deleteModal.isOpen = false" class="mt-3 w-full inline-flex justify-center rounded-xl border border-theme-input-border shadow-sm px-4 py-2 bg-theme-surface text-base font-bold text-theme-text-secondary hover:bg-theme-surface-hover sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">Cancel</button>
 </div>
 </form>
 </div>
 </div>
 </div>

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
 <input type="text" x-model="countrySearch" placeholder="Search for a country..." class="block w-full bg-theme-bg text-theme-text-primary border-theme-input-border rounded-xl px-4 py-2.5 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm shadow-sm mb-4">
 
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
 </template>
</div> <!-- CLOSE x-data="shippingDashboard()" DIV -->

<script>
function shippingDashboard() {
 return {
 expandAll: false,
 
 modal: {
 isOpen: false,
 isEdit: false,
 type: 'province', // province, district, city
 parentId: null,
 editId: null,
 
 name: '',
 rate: '0',
 estimated_days: '',
 is_free_above: '',
 is_active: true
 },
 
 deleteModal: {
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
 const res = await fetch('https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/json/countries.json');
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
 },
 
 openModal(type, parentId = null) {
 this.modal.isOpen = true;
 this.modal.isEdit = false;
 this.modal.type = type;
 this.modal.parentId = parentId;
 
 this.modal.name = '';
 this.modal.rate = '0';
 this.modal.estimated_days = '';
 this.modal.is_free_above = '';
 this.modal.is_active = true;
 },
 
 openEditProvince(id, name) {
 this.openModal('province');
 this.modal.isEdit = true;
 this.modal.editId = id;
 this.modal.name = name;
 },
 
 openEditDistrict(id, name) {
 this.openModal('district');
 this.modal.isEdit = true;
 this.modal.editId = id;
 this.modal.name = name;
 },
 
 openEditCity(id, name, rate, estimated, is_free, is_active) {
 this.openModal('city');
 this.modal.isEdit = true;
 this.modal.editId = id;
 this.modal.name = name;
 this.modal.rate = rate;
 this.modal.estimated_days = estimated;
 this.modal.is_free_above = is_free;
 this.modal.is_active = is_active;
 },
 
 closeModal() {
 this.modal.isOpen = false;
 },
 
 openDeleteModal(type, id) {
 this.deleteModal.type = type;
 this.deleteModal.id = id;
 this.deleteModal.isOpen = true;
 }
 }
}
</script>
{% endblock %}
""")
