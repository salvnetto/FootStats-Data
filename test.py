from requests_html import HTMLSession

url = 'https://fbref.com/en/comps/9/2019-2020/2019-2020-Premier-League-Stats'
session = HTMLSession()
response = session.get(url)
response.html.render()  # Executes JavaScript

print(response.text)  # Check if content loads properly
