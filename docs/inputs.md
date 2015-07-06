Inputs
======

Inputs | Description
---------------|-------------
headers (recommended) |  header object to append to requests instantiation.  The host header is probably the most likely requirement.
username | basic auth username
password | basic auth password
cookie | cookie object to append to requests instantiation
data | data for POST or PUT.
file | provide dummy "filename" and dummy "content" as json arguments. Uploads the content as filename to the specified host.
verify | Should we verify the ssl cert when making an https request?  Defaults to False.
allow_redirects | Follow links. Defauts to False so that you can be explicit about the redirect.
timeout | timeout for the request. Defaults to 30

