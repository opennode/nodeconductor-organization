Organization list
-----------------

To get a list of organizations, run GET against **/api/organizations/** as authenticated user.

Filtering organization list is supported through HTTP query parameters, the following fields are supported:

- ?name=<organization name>
- ?native_name=<organization native name>
- ?abbreviation=<organization abbreviation>
- ?customer_uuid=<customer uuid>
- ?customer=<customer url>

Sorting is supported in ascending and descending order by specifying a field to an **?o=** parameter.

Ascending:

- ?o=name - sort by name
- ?o=native_name - sort by native name
- ?o=abbreviation - sort by abbreviation

Descending:

- ?o=-name - sort by name
- ?o=-native_name - sort by native name
- ?o=-abbreviation - sort by abbreviation


Create a Organization
---------------------

To create a new organization, issue a POST with organization details to **/api/organizations/** as a staff user.

Request parameters:

 - name - organization name (required)
 - native_name - organization native name (required)
 - abbreviation - organization abbreviation (required and unique)
 - customer - URL of organization customer (optional)


Example of a request:


.. code-block:: http

    POST /api/organizations/ HTTP/1.1
    Content-Type: application/json
    Accept: application/json
    Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
    Host: example.com

    {
        "customer": "http://example.com/api/customers/8bdbcd5be4d5452db1390199fa0a4756/",
        "name": "My organization",
        "abbreviation": "MO",
        "native_name": "Minu organisatsioon"
    }


Organization display
--------------------

To get organization data - issue GET request against **/api/organizations/<organization_uuid>/**.

Example rendering of the organization object for staff user:

.. code-block:: javascript

    {
        "url": "http://example.com/api/organizations/ab937a628b194c2dba9b414741e918ec/",
        "customer": "http://example.com/api/customers/8bdbcd5be4d5452db1390199fa0a4756/",
        "name": "My organization",
        "uuid": "ab937a628b194c2dba9b414741e918ec",
        "abbreviation": "MO",
        "native_name": "Minu organisatsioon"
    }


Delete Organization
-------------------

To delete organization - issue DELETE request against **/api/organizations/<organization_uuid>/** as staff user.
