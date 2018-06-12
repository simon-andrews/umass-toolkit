People Finder
=============

`People Finder <https://www.umass.edu/peoplefinder/>`_ is a service
that searches the SPIRE directory for people affiliated with UMass. This
includes students, faculty, and staff, as well as some retirees who have opted
to continue being listed.

From People Finder, you can look up any UMass person's full name and school
email address. Additionally, you can look up any student's majors and degree
program. You may also find any faculty or staff member's title and department
affiliation. If they have chosen to list it you may also find their phone
number, physical office location, and homepage.

API information
---------------

The main endpoint for the Person Finder API is
:code:`www.umass.edu/peoplefinder/engine/`. This endpoint only takes POST
requests, and will fail with HTTP error 405 on any other request type. It
requires two parameters, and accepts several other optional ones. The first is
:code:`q`, your search query. The second is :code:`time`, the time of the
request in milliseconds since the UNIX epoch as an integer.

.. note::
   The People Finder
   `source code <https://www.umass.edu/peoplefinder/res/js/pf.js>`_ does
   reference and use other POST request parameters that aren't documented here
   yet. We'll get around to those someday.

Response format
---------------

Upon a successful request, the People Finder API will return a JSON response
containing information on matching people. The basic format of the response is
as follows:

.. code:: json

   {
    'ErrorCode': integer,
    'ErrorHint': string,
    'ErrorMsg': string,
    'OverflowFlag': boolean,
    'Results': array
   }

The non-error values are 0 for :code:`ErrorCode`, and a blank string
(:code:`''`) for both :code:`ErrorHint` and :code:`ErrorMsg`. I've not been
able to trigger an error yet so I can't say for *sure* what happens when
there's an error, but I think the field names are pretty self-explanatory.

The :code:`OverflowFlag` field indicates whether there are more results for the
query than are listed in the results. Information on a maximum of 13 people per
query can be returned. If the overflow flag is set to true, be aware that there
are more matching results than are being given to you. There is no way to
paginate or get a different set of 13 people with the same query, so if you
didn't find the person you're looking for, you'll just have to try something
else.

.. tip::
   This 13 person limit doesn't happen with the UMass Directory on SPIRE.

The :code:`Results` field contains all the student data you're looking for. It
is an array of objects representing students. Fields are only included in the
objects if they have values. Possible fields include:
 * :code:`Name`: String of the person's full name. Not split into first and
   last names, even though that's how you enter it into SPIRE.
 * :code:`Email`: String of the person's school email. Generally @umass.edu,
   but graduate students and faculty often have email addresses for their
   specific departments. For example, computer science people usually have
   @cs.umass.edu emails.
 * :code:`Affil`: Array of strings detailing the person's affiliations to
   the university. It **is** possible to have more than one. Possible values
   include :code:`Student` and :code:`Employee`.
 * :code:`Major`: Array of strings of the person's majors and degree plans.
   Strings will *usually* be in the format of :code:`SUBJECT ([DEGREE])`.
   Examples include :code:`Computer Science (BS)` or :code:`Economics (PhD)`.
   This is **not** always the case. Here are some real major strings I've
   discovered that do not follow the usual format.
    * :code:`U. Without Walls OffCampus (Non Degree)`
    * :code:`Part-Time MBA`
    * :code:`Professional MBA (NonDeg)` *(WTF?!)*
 * :code:`Vcard`: The People Finder API also generates VCards! Throw the
   string in this field onto the end of :code:`www.umass.edu` and you've got
   yourself a VCard.
 * :code:`Title`: String of the person's title at UMass. Employees only.
 * :code:`Phone`: Array of strings containing phone numbers. Employees only.
 * :code:`Building`: Array of strings detailing where the person can be found.
   I'm guessing that users are free to enter whatever they please here, as the
   level of detail varies greatly between people. Employees only.
 * :code:`Dept`: Array of strings representing the departments the person is
   affiliated with. Employees only.
 * :code:`URL`: Array of strings of URLs to the person's personal websites.
   Employees only.

Reverse engineering tips
------------------------

The information on this page was found from the People Finder's JavaScript
`source code <https://www.umass.edu/peoplefinder/res/js/pf.js>`_. There's still
stuff in there that's not documented on this page yet. Most of the interesting
stuff is happing in the :code:`pf_search` function, found at around line
400-ish.
