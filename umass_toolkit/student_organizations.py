from urllib.parse import urljoin

import requests

URI_BASE = "https://umass.campuslabs.com"
API_BASE = "engage/api/discovery/"

# The primary endpoint used by the webapp is 'engage/api/discovery/search/
# organizations', which appears to be Microsoft's Azure Search Service REST API.
# It's some sort of RPC controlled via GET parameters. Documentation available.
# <https://docs.microsoft.com/en-us/rest/api/searchservice/search-documents>

def _request(endpoint, params={}):
    uri = urljoin(urljoin(URI_BASE, API_BASE), endpoint)
    return requests.get(uri, params=params).json()


# TODO: Perhaps this should raise an exception rather than returning 0?
# TODO: Also, should this maybe be exposed to the public API?
def _num_organizations():
    # The necessary data is in the "@odata.count" field of every response, but
    # if the webapp does this, we might as well.
    resp = _request("search/organizations", {
        "top": 0,
        "facets[0]": "BranchId"
    })
    structs = resp.get("@search.facets", {}).get("BranchId", {})
    if len(structs) >= 1:
        return structs[0].get("count", 0)
    return 0


def _category_name(category_id):
    resp = _request("organization/category", {
        "categoryIds[0]": category_id
    })
    structs = resp.get("items", [])
    if len(structs) >= 1:
        return structs[0].get("name")


def _category_ids():
    resp = _request("search/organizations", {
        "top": 0,
        "facets[0]": "CategoryIds,count:{}".format(_num_organizations())
    })
    structs = resp.get("@search.facets", {}).get("CategoryIds", {})
    return [category.get("value") for category in structs]


def _additional_fields(organization_id):
    resp = _request("organization/{}/additionalFields".format(organization_id))
    return resp["items"]


def categories():
    """Returns a list of valid category strings, for use in the 'categories'
       parameter of 'student_organizations.search'.
    """
    return [_category_name(category) for category in _category_ids()]


def info(websitekey):
    """Returns all information on the organization with the given name. A valid
       'websitekey' parameter can be obtained from 'search'."""
    resp = _request("organization/bykey/{}".format(websitekey))
    organization_id = resp["id"]
    resp["additionalFields"] = _additional_fields(organization_id)
    return resp


def search(keywords="", categories=[]):
    """Return organizations matching the given keywords and categories."""
    # Reverse-lookup is expensive.
    filter_string = ""
    if len(categories) > 0:
        filter_string = []
        for category_id in _category_ids():
            if _category_name(category_id) in categories:
                filter_string.append(
                    "CategoryIds/any(x: x eq '{}')".format(category_id)
                )
        filter_string = "(" + " or ".join(filter_string) + ")"

    resp = _request("search/organizations", {
        "top": _num_organizations(),
        "filter": filter_string,
        "query": keywords
    })
    return resp.get("value", [])


def all_organizations():
    """Return a list of every registered organization."""
    return search()
