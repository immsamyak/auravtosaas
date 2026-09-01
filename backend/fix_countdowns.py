import glob

old_code = """        endDate: new Date(new Date().getTime() + 14 * 24 * 60 * 60 * 1000).getTime(), 
        days: 0, hours: 0, mins: 0, 
        init() { this.update(); setInterval(() => this.update(), 60000); },
        update() {
            let distance = this.endDate - new Date().getTime();
            if (distance < 0) { this.days = 0; this.hours = 0; this.mins = 0; return; }
            this.days = Math.floor(distance / (1000 * 60 * 60 * 24));
            this.hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            this.mins = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        }"""

new_code = """        endDate: {% if settings.target_date %}new Date('{{ settings.target_date }}').getTime(){% else %}new Date(new Date().getTime() + 14 * 24 * 60 * 60 * 1000).getTime(){% endif %}, 
        days: 0, hours: 0, mins: 0, secs: 0,
        init() { this.update(); setInterval(() => this.update(), 1000); },
        update() {
            let distance = this.endDate - new Date().getTime();
            if (distance < 0) { this.days = 0; this.hours = 0; this.mins = 0; this.secs = 0; return; }
            this.days = Math.floor(distance / (1000 * 60 * 60 * 24));
            this.hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            this.mins = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            this.secs = Math.floor((distance % (1000 * 60)) / 1000);
        }"""

themes = glob.glob('templates/storefront/theme_*/sections/countdown.html')
replaced = 0
for theme in themes:
    with open(theme, 'r') as f:
        content = f.read()

    if old_code in content:
        content = content.replace(old_code, new_code)
        with open(theme, 'w') as f:
            f.write(content)
        replaced += 1
    else:
        print(f"Could not find exact block in {theme}")

print(f"Fixed {replaced} countdown templates safely.")
