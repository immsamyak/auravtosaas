import os

target_class = 'inline-block border-2 border-white text-white hover:bg-white hover:text-black font-sans font-bold uppercase tracking-wider px-10 py-4 rounded-lg transition-colors shadow-lg shadow-black/25'

replacements = {
    'theme_boho': 'inline-block border-2 border-boho-terra text-boho-terra font-sans font-bold text-sm uppercase tracking-widest px-10 py-4 rounded-full hover:bg-boho-terra hover:text-white transition-colors',
    'theme_couture': 'inline-block border border-black text-black font-sans font-bold text-xs uppercase tracking-[0.2em] px-8 py-3 hover:bg-black hover:text-white transition-colors w-fit',
    'theme_cyberpunk': 'inline-block border-2 border-cyber-magenta text-cyber-magenta font-display font-bold text-xl uppercase tracking-wider px-8 py-3 hover:bg-cyber-magenta hover:text-black transition-colors',
    'theme_glass': 'inline-block border border-white/50 bg-white/10 backdrop-blur-md text-white font-semibold px-8 py-3 rounded-xl hover:bg-white/20 transition-all shadow-lg',
    'theme_goth': 'inline-block border border-goth-purple text-goth-purple font-display text-sm tracking-[0.2em] uppercase px-10 py-4 hover:bg-goth-purple hover:text-white transition-all duration-500',
    'theme_popart': 'inline-block bg-white text-pop-black font-display text-xl px-10 py-4 neo-brutal border-4 border-pop-black hover:bg-pop-blue hover:text-white transition-colors',
    'theme_resort': 'inline-block border-2 border-resort-ocean text-resort-ocean font-sans font-semibold px-10 py-4 rounded-full hover:bg-resort-ocean hover:text-white transition-colors shadow-lg shadow-black/5',
    'theme_skate': 'inline-block bg-transparent border-4 border-skate-dark text-skate-dark font-display text-2xl tracking-wider px-8 py-3 hover:bg-skate-dark hover:text-skate-cream transition-colors',
    'theme_sneaker': 'inline-block border-2 border-snkr-bg text-snkr-bg font-sans font-bold uppercase tracking-wider px-10 py-4 rounded-lg hover:bg-snkr-bg hover:text-white transition-colors shadow-lg shadow-black/10',
    'theme_street': 'inline-flex items-center justify-center bg-black text-white font-bold uppercase tracking-wider px-8 py-4 brutal-border hover:bg-neon hover:text-black hover:-translate-y-1 hover:brutal-shadow transition-all w-fit',
    'theme_vintage': 'inline-block border-2 border-sepia-900 text-sepia-900 font-sans font-bold uppercase tracking-widest px-8 py-4 rounded hover:bg-sepia-900 hover:text-sepia-50 transition-colors',
    'theme_vogue': 'inline-block border border-black text-black px-8 py-3 text-xs uppercase tracking-widest font-bold hover:bg-black hover:text-white transition-colors duration-300 bg-white/80 backdrop-blur-sm'
}

for theme, new_class in replacements.items():
    filepath = f"templates/storefront/{theme}/sections/hero.html"
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        
        if target_class in content:
            content = content.replace(target_class, new_class)
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"Updated {theme}")
        else:
            print(f"Target class not found in {theme}")

