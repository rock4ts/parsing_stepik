from bs4 import BeautifulSoup

html = """
<html>
    <body>
        <h1>Example Page</h1>
        <p>This is some text.</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
            <li>Item 3</li>
        </ul>
        <p>This is some more text.</p>
        <p>This is even more text.</p>
    </body>
</html>
"""
soup = BeautifulSoup(html, 'html.parser')

# tag parent
# html_doc = """<html>...</html>"""
# soup = BeautifulSoup(html_doc, 'html.parser')
# element = soup.find('element')
# parent = element.parent
# print(parent.name)

# tag.next_sibling - возвращает элемент (тег/текст/пробел) следующий за текущим

# soup = BeautifulSoup(html, 'html.parser')
# lis = soup.find_all('li')
# lis_count = len(lis)
# siblings = []
# prev_elem = lis[-1]

# next_sibling = lis[0]
# while next_sibling:
#     siblings.append(next_sibling)
#     next_sibling = next_sibling.next_sibling
# print(siblings)

# while prev_elem:
#     siblings.append(prev_elem)
#     prev_elem = prev_elem.previous_sibling
#
# print(siblings)

# tag.next_element -> следующий элемент (тег, строка или текст)
# tag.previous_element -> предидущий элемент

# last_p = soup.find_all('p')[-1]
# print(last_p)
# prev_elem = last_p.previous_element
#
# while prev_elem:
#     print(prev_elem)
#     prev_elem = prev_elem.previous_element
