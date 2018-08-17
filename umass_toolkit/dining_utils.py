from bs4 import BeautifulSoup
import pint


ureg = pint.UnitRegistry()


#TODO: handle multiple levels of parentheses
#e.g. Chili (spicy (but not too spicy))
def parse_list(ingredients):
    if ingredients == '':
        return []
    naive_split = ingredients.split(', ')
    ingredient_list = []
    
    # for (i = 0; i < len(naive_split); i++)
    i = 0
    while i < len(naive_split):
        ingredient = ''
        if '(' in naive_split[i]:
            while i < len(naive_split):
                ingredient += naive_split[i]
                if ')' in naive_split[i]:
                    break
                else:
                    ingredient += ', '
                i += 1
        else:
            ingredient = naive_split[i]
        ingredient.strip()
        ingredient_list.append(ingredient)
        i += 1
    return ingredient_list

def category_html_to_dict(html_string, meal, category):
    soup = BeautifulSoup(html_string, 'html.parser')
    items = soup.find_all('a', href='#inline')
    ret = []
    for item in items:
        dish = {}
        dish['category-name'] = category
        dish['meal-name'] = meal
        for attribute in item.attrs.keys():
            if attribute.startswith('data-') and not attribute.endswith('dv'):
                attribute_name = attribute[5:]
                data = item.attrs[attribute]
                if attribute_name == 'calories' or attribute_name == 'calories-from-fat':
                    data = int(data) if data else None
                elif attribute_name == 'clean-diet-str':
                    data = data.split(', ')
                    attribute_name = 'diets'
                elif attribute_name in ['allergens', 'ingredient-list']:
                    data = parse_list(data)
                elif attribute_name in ['cholesterol', 'sodium', 'dietary-fiber', 'protein', 'sat-fat', 'sugars',
                                        'total-carb', 'total-fat', 'trans-fat']:
                    data = ureg.Quantity(data) if data else None
                dish[attribute_name] = data
        ret.append(dish)
    return ret
