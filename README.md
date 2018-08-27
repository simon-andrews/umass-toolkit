
UMass Toolkit [![Build Status](https://travis-ci.org/simon-andrews/umass-toolkit.svg?branch=master)](https://travis-ci.org/simon-andrews/umass-toolkit) [![Discord](https://img.shields.io/discord/469301310072684546.svg)](https://discord.gg/7Szhww5)
=============================================================================================================
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

Finding all soups at Berkshire with soy in them:
```python3
berkshire_lunch_menu = get_menu(4)['lunch'] # 4 is Berkshire's UMass dining location ID number
soups = berkshire_lunch_menu['Soups']
for soup_name in soups:
  if 'Soy' in soups[soup_name]['allergens']:
    print(soup_name)
```

Finding out who's in charge of the UMass club powerlifting team
```python3
key = student_organizations.search("Powerlifting")[0]["WebsiteKey"]
info = student_organizations.info(key)
contact = info["primaryContact"]
print("Run by {} {}".format(contact["firstName"], contact["lastName"]))
```

Contributing
------------
We'd love to have you contribute some code to this project! Patches from beginning programmers are welcome! We'll help polish up your code and everything.

Check out [CONTRIBUTING.md](https://github.com/simon-andrews/umass-toolkit/blob/master/CONTRIBUTING.md) to get up to speed. It has information on all sorts of stuff, like installing Python and submitting your code changes with GitHub.

Similar projects
----------------
Know of a similar project at another institution? Link to it here!
 * Boston University: [BU API Registry](https://webapi.bu.edu/)
 * Massachusetts Institute of Technology: [MIT Developer Connection](https://ist.mit.edu/apis)
 * University of Pennsylvania: [PennSDK](https://github.com/pennlabs/penn-sdk-python)
