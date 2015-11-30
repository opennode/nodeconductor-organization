List organizations
------------------

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


Create a organization
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


Display organization
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


Delete organization
-------------------

To delete organization - issue DELETE request against **/api/organizations/<organization_uuid>/** as staff user.

List organization users
-----------------------

To get list of all organization users - issue GET request against **/api/organization-users/**.

**Permissions:**

- Staff user can see users of all organizations.
- Customer owner can see users of the connected organization.
- Regular user can see only his organization user.

Response example:

.. code-block:: javascript

    [
        {
            "url": "http://example.com/api/organization-users/2de6bc633e56403f9a73c7a3baf9677e/",
            "user": "http://example.com/api/users/ba3f5a1c36a94075a53fd9ab180967de/",
            "username": "Alice",
            "uuid": "2de6bc633e56403f9a73c7a3baf9677e",
            "is_approved": false,
            "organization": "http://example.com/api/organizations/33e17c07683a4d0db0b9376a14b9e2a1/"
        },
        {
            "url": "http://example.com/api/organization-users/701e29fbc30f44c895cafc6848a9bda8/",
            "user": "http://example.com/api/users/95db7c9c9a7c4109b3791a1fa3a7a6a8/",
            "username": "Bob",
            "uuid": "701e29fbc30f44c895cafc6848a9bda8",
            "is_approved": false,
            "organization": "http://example.com/api/organizations/c2a045dfc2bb4cf981cafd35a2e88368/"
        }
    ]


Filtering organization users list is supported through HTTP query parameters,
the following fields are supported:

- ?organization=<organization url>
- ?organization_uuid=<organization uuid>
- ?user=<user url>
- ?user_uuid=<user uuid>
- ?is_approved=<True or False>

Sorting is supported in ascending and descending order by specifying a field to an **?o=** parameter.

- ?o=is_approved - approved at the end
- ?o=-is_approved - approved at the beginning

Create organization user
------------------------

To create new organization user - issue POST request against **/api/organization-users/**.

**Permissions:**

- Staff user can create organization user for every user account.
- Regular user can create organization user only for his user account.

Note that every user can have only one user account.

Request parameters:

 - user - user url (required, unique)
 - organization - organization url (required)

Example of a request:


.. code-block:: http

    POST /api/organization-users/24156c367e3a41eea81e374073fa1060/ HTTP/1.1
    Content-Type: application/json
    Accept: application/json
    Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
    Host: example.com

    {
        "user": "http://example.com/api/users/95db7c9c9a7c4109b3791a1fa3a7a6a8/",
        "organization": "http://example.com/api/organizations/33e17c07683a4d0db0b9376a14b9e2a1/"
    }


Display organization user
-------------------------

To get organization user data - issue GET request against **/api/organization-users/<user_uuid>/**.

Example rendering of the organization object for staff user:

.. code-block:: javascript

    {
        "url": "http://example.com/api/organization-users/2de6bc633e56403f9a73c7a3baf9677e/",
        "user": "http://example.com/api/users/ba3f5a1c36a94075a53fd9ab180967de/",
        "username": "Alice",
        "uuid": "2de6bc633e56403f9a73c7a3baf9677e",
        "is_approved": false,
        "organization": "http://example.com/api/organizations/33e17c07683a4d0db0b9376a14b9e2a1/"
    }


Approve organization user
-------------------------

To approve user participation in the organization issue POST request against
**/api/organization-users/<user_uuid>/approve/** as organization customer owner or staff user.
`is_approved` field will change to **True**.


Reject organization user
------------------------

To reject user participation in the organization issue POST request against
**/api/organization-users/<user_uuid>/reject/** as organization customer owner or staff user.
`is_approved` field will change to **False**.


Delete organization user
------------------------

To delete organization user - issue DELETE request against **/api/organization-users/<user_uuid>/**.
Note that user can delete his organization user only when it is not approved.

