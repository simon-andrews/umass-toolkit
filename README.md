UMass Toolkit
=============
Tools for working with various APIs serving up data related to the University of Massachusetts Amherst.

Installation
------------
The UMass Toolkit is currently not available on PyPI, as it's very new and not quite release-ready yet. The only way to install it right now is from source. To do this:

1. **Fetch the source code:** The easiest way to do this is with Git. Simply run `git clone https://github.com/simon-andrews`. Otherwise you can download a ZIP archive from GitHub.
2. **Install the package:** From the directory of the downloaded source code, run `python3 setup.py install`. You may need administrator privileges for this to run properly.
3. **Verify that it worked:** Running `python3 -c "import umass_toolkit"` should not cause any errors.

Recipes
-------
Searching for people:
```python3
from umass_toolkit import people_finder
results = people_finder.search('kumble')
for person in results['people']:
  print('{name} <{email}>'.format_map(person))
if results['overflow_flag']:
  print('Heads up: there were more matching results than the server gave us.')
```

Finding food trucks:
```python3
from umass_toolkit.dining import get_food_trucks
for truck in get_food_trucks():
  if truck['is_open']:
    print('GMaps for truck #{id}: https://www.google.com/maps/?q={longitude},{latitude}'.format_map(truck))
  else:
    print('Truck #%d is not open for business right now. Sorry! :(' % truck['id'])
```

Finding all soups at Worcester with soy in them:
```python3
worcester_lunch_menu = get_menu(4)['lunch'] # 4 is Worcester's UMass dining location ID number
soups = worcester_lunch_menu['Soups']
for soup_name in soups:
  if 'Soy' in soups[soup_name]['allergens']:
    print(soup_name)
```

Similar projects
----------------
Know of a similar project at another institution? Link to it here!
 * University of Pennsylvania: [PennSDK (Python)](https://github.com/pennlabs/penn-sdk-python)
