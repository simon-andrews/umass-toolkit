Contribute to UMTK!
===================

General rules:
 * Don't be a jerk
 * Feel free to ask for help with anything
 * Read [this](https://stackoverflow.com/help/how-to-ask) for some tips on how
   to ask good questions.
 * Issues marked ["good first issue"](https://github.com/simon-andrews/umass-toolkit/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) are for beginners only

Getting set up
---------------
You'll need some stuff before you get started.

### Python 3
Python is the programming language that UMTK is written in. It's important that
you use Python _3_. Python _2_ is around and still popular because a lot of old
software still runs on it. More info can be found
[here](https://wiki.python.org/moin/Python2orPython3).

Open a terminal or command prompt or whatever your system calls it and run
`python`. You should see something like:
```
Python 2.7.14 (default, Sep 23 2017, 22:06:14)
[GCC 7.2.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
The version number is in the first line. If you have a 2.x version, try running
`python3` instead:
```
Python 3.6.3 (default, Oct  3 2017, 21:45:48)
[GCC 7.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

If you don't have Python 3, you'll need to install it.
[See the official Python website](https://www.python.org/).

### requests
requests is a Python library for interacting with HTTP servers. To install it,
fire up your terminal and run `pip install requests`.

### BeautifulSoup
BeautifulSoup is a Python library for parsing HTML documents. To install it,
fire up your terminal and run `pip install BeautifulSoup`

### Git
Git is software for managing source code. Here's how to
[install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git),
a [quick overview](https://rogerdudler.github.io/git-guide/), and some
[tutorials by GitHub](https://try.github.io/).

Git's confusing-ness and hostility to newcomers is a
[bit of a joke](https://xkcd.com/1597/). Don't stress if you don't "get" it
right away.

### A GitHub account
You should be able to figure out how to sign up. Once you've done that, tell
@simon-andrews to add you as a collaborator.

Installing UMTK
---------------
Now that your environment is set up, we need to get UMTK. In your terminal,
`cd` to where you want your code downloaded to then run `git clone
https://github.com/simon-andrews/umass-toolkit`. This will download a copy of
UMTK's source code to your computer from GitHub. `cd` into the new
umass-toolkit folder you just created.

From there, run `python3 setup.py install`. This will install UMTK so that
Python can see and use it.

Now, run `python3 -c 'import umass_toolkit'`. If there are no errors, UMTK has
been installed! Hooray! Two things we just did there:
 - An `import` in Python is basically telling Python to make a library someone
   else has written available to you to use.
 - `python3 -c ...` basically tells Python "run this code, then exit."

Start developing
----------------
Python is a good language to start learning to program with. I've not used it
personally, but I hear very good things about the
[_Automate the Boring stuff with Python_](https://automatetheboringstuff.com/) book.

Developing UMTK will also require familiarity with requests and BeautifulSoup.
 * [requests quickstart](http://docs.python-requests.org/en/master/user/quickstart/)
 * [BeautifulSoup 4 documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

Here's a basic program that'll give you like 80% of what you need to know.

```python3
# Import our libraries
import bs4
import requests

# Download a webpage
r = requests.get('https://umass-cs-187.github.io/')
html_source = r.text

# Parse HTML with BeautifulSoup
soup = bs4.BeautifulSoup(html_source)

# Get all the links
# This is how a link looks in HTML
#   <a href="google.com">Click me to go to Google!</a>
# a is the tag
# href is an attribute
# Click me to... is what shows up on your screen (sometimes called value)
# <tag>...</tag> is an element. Every <...> needs a corresponding </...>
links = soup.find_all('a')
for link in links:
  print(link.get('href'))
```
Which will result in:
```
mailto:[email address removed]
mailto:[email address removed]
mailto:[email address removed]
mailto:[email address removed]
mailto:[email address removed]
https://www.umass.edu/registrar/calendars/academic-calendar
http://piazza.com
http://piazza.com
https://gradescope.com/
https://www.amazon.com/Data-Structures-Algorithms-Java-Edition/dp/0672324539
https://www.amazon.com/Java-Precisely-Press-Peter-Sestoft/dp/0262529076/
http://chimera.labs.oreilly.com/books/1234000001805
https://moodle.umass.edu/
http://piazza.com
https://piazza.com/support/help
https://moodle.umass.edu/
https://www.eclipse.org/downloads/
https://www.eclipse.org/downloads/
https://gradescope.com/
mailto:[email address removed]
http://www.umass.edu/registrar
http://www.umass.edu/registrar/sites/default/files/academicregs.pdf
```

What we just did above is something called "web scraping" and it's generally
something you want to avoid doing. Web pages are made for humans, not
machines. Some people are nice enough to provide machine-friendly sites too,
usually written in languages like JSON or XML. JSON
```json
{
  'looks': ['like', 'this']
}
```

For example: https://www.umassdining.com/umassapi/truck_location

requests provides a nice way to work with these. Check this out:
```python3
import requests

r = requests.get('https://www.umassdining.com/umassapi/truck_location')
trucks = r.json()
```

requests is smart enough to parse the JSON code the web server gave us and
returns a Python dictionary to us ready to go! No need to muck around with
BeautifulSoup at all!

### Upload your changes
You've made a change! Hooray! Now, in a terminal:
 1. `git checkout SOME_DESCRIPTIVE_NAME`: This makes a "branch", so you won't
    accidentally mess with the master branch.
 2. `git add -A`: Add all the files you've changed to your "staging area."
    This is basically where you prepare your changes before you upload them.
 3. `git commit --dry-run`: This shows you your changes before you make them,
    giving you one last chance to look everything over
 4. `git commit -m "Some descriptive message"`: Actually commit your changes,
    with a message for the log (see `git log`) explaining what you did.
 5. `git push origin SOME_DESCRIPTIVE_NAME`: Now that your changes have been
    made, upload them to GitHub!

Now go to GitHub and make a pull request for your branch. I don't remember
exactly how to do it, but it _should_ be pretty self explanatory. Don't worry
about any complaints from GitHub about merge conflicts, if that should happen
to you.

Someone will then look over your pull request, and merge it into the master
branch if it looks good or give you some change to make. If there are changes
to make, do this whole thing over but skip the step about making a new pull
request.
