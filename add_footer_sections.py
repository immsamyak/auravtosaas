import re

html_files = ['aura_codecanyon_preview.html', 'codecanyon-preview/index.html']

footer_addition = """
    <!-- 25, 26, 27. LOGS & SUPPORT -->
    <section class="py-24 bg-white border-t border-slate-200" id="docs">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-3 gap-8 text-center">
                <div class="p-8 bg-slate-50 rounded-2xl border border-slate-200">
                    <h3 class="text-2xl font-bold mb-4">Changelog</h3>
                    <p class="text-slate-500 mb-4">Current Version: 1.0.0<br>Initial release featuring complete VTO architecture, multi-tenant roles, and advanced catalog logic.</p>
                    <a href="CHANGELOG.md" class="text-primary font-bold hover:underline">View Full Changelog</a>
                </div>
                <div class="p-8 bg-slate-50 rounded-2xl border border-slate-200">
                    <h3 class="text-2xl font-bold mb-4">Support</h3>
                    <p class="text-slate-500 mb-4">We provide 6 months of dedicated support for installation, bug fixes, and general guidance on extending the platform.</p>
                    <a href="mailto:support@example.com" class="text-primary font-bold hover:underline">Contact Support</a>
                </div>
                <div class="p-8 bg-slate-50 rounded-2xl border border-slate-200">
                    <h3 class="text-2xl font-bold mb-4">License</h3>
                    <p class="text-slate-500 mb-4">Available under Standard and Extended licenses. The extended license is required if you plan to charge users for VTO generations.</p>
                    <a href="#" class="text-primary font-bold hover:underline">View License Details</a>
                </div>
            </div>
        </div>
    </section>

    <!-- FOOTER -->
"""

for f in html_files:
    with open(f, 'r') as file:
        content = file.read()

    content = content.replace('<!-- FOOTER -->', footer_addition)

    with open(f, 'w') as file:
        file.write(content)

print("Footer updated.")
