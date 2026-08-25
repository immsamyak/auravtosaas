files = ['aura_codecanyon_preview.html', 'codecanyon-preview/index.html']

for f in files:
    with open(f, 'r') as file:
        content = file.read()

    # Admin global settings
    content = content.replace('Admin_Authorized_GlobalSettings_Desktop_1787585216.png', 'Admin_GlobalSettings.png')
    
    # Brand dashboard
    content = content.replace('BrandOwner_Valid_Auth_Dashboard_Desktop_1787585220.png', 'Brand_Dashboard.png')
    
    # Brand catalog/products
    content = content.replace('BrandOwner_CreateProductUI_1787586646.png', 'Brand_Catalog.png')
    
    # Brand orders
    content = content.replace('BrandOwner_OrderList_1787586646.png', 'Brand_Orders.png')
    
    # Brand settings
    content = content.replace('BrandOwner_StoreSettings_1787586646.png', 'Brand_Settings.png')
    
    # Admin users
    content = content.replace('Admin_UserList_1787586644.png', 'Admin_Users.png')

    with open(f, 'w') as file:
        file.write(content)

print("Images replaced.")
