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

# soup.find(self, name=None, attrs={}, recursive=True, string=None, **kwargs)
# soup.find_all(
#    self, name=None, attrs={}, recursive=True,
#    limit=None, string=None, **kwargs
# )

# text = soup.get_text()
# text_list = text.split('\n')
# text_list_filtered = list(filter(lambda x: x != '', text.split('\n')))
# print(text_list)
# print(text_list_filtered)

# text = all_tags.get_text()
# print(text)

# soup.select(self, selector, namespaces=None, limit=None, **kwargs) -> [tags]
# e.g. soup.select('#div1 .highlight', '#div2 .highlight')
# soup.select('p.highlight') == soup.select("p[@class='hightlight']")

# soup.select_one(self, selector, namespaces=None, **kwargs)

# tag.decompose() -> удаляет тег и его потомков
# e.g.
# main_div = soup.find('div', {id: 'main'})
# main_div_child = main_div.find('p', {class: 'info'})
# main_div_child.decompose() -> soup (или main_div) - main_div_child

# tag.extract() -> удаляет тег с потомками и возвращает его(тег)

# soup.new_tag(
#     self, name, namespace=None, nsprefix=None, attrs={},
#     sourceline=None, sourcepos=None, **kwargs
# )
# :sourceline - номер строки в HTML где тег создан
# :sourcepos - позиция тега в HTML
# e.g.
# new_h1 = soup.new_tag('h1', class_='some class')
# new_h1.string = 'Yo!'
# soup.tag_name.insert(ix, new_h1)

# tag.insert_after(new_tag) -> вставляет тег перед тем к кот прим метод
# tag.insert_before(new_tag) -> вставляет тег после того к кот прим метод
# e.g. tag.insert()
# main_div = soup.select('div ul')[0]
# new_tag = soup.new_tag('li')
# new_tag.string = 'Item 4 insert_index'
# main_div.insert(-1, new_tag)
# print(soup)

# tag.wrap()
# some_tag = soup.body.some_tag
# wrapper_tag = soup.new_tag('div', class_='wrapper')
# some_tag.wrap(wrapper_tag)
# print(some_tag.parent) -> wrapper_tag
