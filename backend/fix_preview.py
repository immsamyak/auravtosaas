import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    replacement = """function previewImage(input, previewId) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            var previewElement = document.getElementById(previewId);
            if(previewElement) {
                previewElement.src = e.target.result;
                previewElement.classList.remove('hidden');
                var container = document.getElementById(previewId + "_container");
                if(container) {
                    container.style.display = 'block';
                    container.classList.remove('hidden');
                }
            }
        }
        reader.readAsDataURL(input.files[0]);
    }
}"""
    
    # Replace the existing function
    pattern = re.compile(r'function previewImage\(input, previewId\).*?reader\.readAsDataURL\(input\.files\[0\]\);\n\s*\}\n\}', re.DOTALL)
    content = pattern.sub(replacement, content)
    
    with open(filepath, 'w') as f:
        f.write(content)

fix_file('apps/catalog/templates/catalog/create_product.html')
fix_file('apps/catalog/templates/catalog/edit_product.html')
