from bs4 import BeautifulSoup

with open('backend/templates/dashboard_base.html', 'r') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

headers = soup.find_all('header')
for i, h in enumerate(headers):
    print(f"Header {i+1} classes: {h.get('class')}")
