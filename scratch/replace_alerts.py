import os
import re

backend_dir = "/Users/saamyak/COllege Project/Aura/backend/templates"

toastify_snippet = """
<!-- Toastify Setup -->
<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/toastify-js/src/toastify.min.css">
<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/toastify-js"></script>
<script>
  window.showToast = function(msg, type='info') {
    let bgColor = type === 'error' ? '#ef4444' : (type === 'success' ? '#10b981' : '#333');
    Toastify({
      text: msg,
      duration: 3000,
      gravity: "bottom",
      position: "right",
      style: {
        background: bgColor,
        borderRadius: '8px',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        padding: '12px 24px',
        fontSize: '14px',
        fontWeight: '500'
      }
    }).showToast();
  };
</script>
"""

files_modified = 0

for root, _, files in os.walk(backend_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            modified = False
            
            # 1. Inject Toastify into base layouts
            if file in ["base.html", "admin_base.html"]:
                if "Toastify Setup" not in content and "</head>" in content:
                    content = content.replace("</head>", toastify_snippet + "\n</head>")
                    modified = True
            
            # 2. Replace all instances of alert(
            if "alert(" in content:
                content = content.replace("alert(", "showToast(")
                modified = True
            
            if modified:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Updated {path}")
                files_modified += 1

print(f"Total files updated: {files_modified}")
