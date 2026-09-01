function shippingDashboard() {
 return {
 expandAll: false,
 
 modal: {
 isOpen: false,
 isEdit: false,
 type: 'province', // province, district, city
 parentId: null,
 editId: null,
 
 // Form Fields
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
 // Fetch from the public github DB (dr5hn)
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
 
 // Reset fields
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
