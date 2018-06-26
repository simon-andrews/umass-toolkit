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
people = people_finder.search('kumble')
for person in people['results']:
  print(person)
if people['overflow_flag']:
  print('Heads up: there were more matching results than the server gave us.')
```

Finding food trucks:
```python3
from umass_toolkit.dining import get_food_trucks
for truck in get_food_trucks():
  if truck['longitude'] is not None and truck['latitude'] is not None:
    print('GMaps for truck #{id}: https://www.google.com/maps/?q={long},{lat}'.format(id=truck.id, long=truck.longitude, lat=truck.latitude))
  else:
    print('Truck #%d is not open for business right now. Sorry! :(' % truck['id'])
```
