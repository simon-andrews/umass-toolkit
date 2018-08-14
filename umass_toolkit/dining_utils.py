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
