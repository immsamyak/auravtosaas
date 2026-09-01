from bs4 import BeautifulSoup

html = """
<footer class="bg-black text-white">
    <div class="container">
        {% if brand.logo %}
        <img src="{{ brand.logo.url }}" alt="Logo">
        {% endif %}
        <div>
            <h4>Newsletter</h4>
            <form id="newsletter-subscribe-form" action="{% url 'newsletter_subscribe' brand.slug %}">
                <input type="email">
            </form>
        </div>
    </div>
</footer>
"""

soup = BeautifulSoup(html, 'html.parser')
form = soup.find('form', id='newsletter-subscribe-form')
form.parent.decompose()

final_html = str(soup)
final_html = final_html.replace('&lt;', '<').replace('&gt;', '>')
print(final_html)
