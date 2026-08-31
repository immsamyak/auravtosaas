import os

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
</head>
"""

files = [
    "/Users/saamyak/COllege Project/Aura/backend/templates/dashboard_base.html",
    "/Users/saamyak/COllege Project/Aura/backend/templates/base_bare.html",
    "/Users/saamyak/COllege Project/Aura/backend/apps/orders/templates/pos/customer_display.html"
]

for path in files:
    if os.path.exists(path):
        with open(path, "r") as f:
            content = f.read()
        if "Toastify Setup" not in content and "</head>" in content:
            content = content.replace("</head>", toastify_snippet)
            with open(path, "w") as f:
                f.write(content)
            print(f"Injected Toastify into {path}")

