Inputs
======

Inputs are passed through to "requests" unmodified.

Inputs | Description | Default
-------|-------------|-------
headers (recommended) |  header object to append to requests instantiation.  The host header is probably the most likely requirement. | None
username | basic auth username | None
password | basic auth password | None
cookie | cookie object to append to requests instantiation | None
data | data for POST or PUT. | None
file | provide dummy "filename" and dummy "content" as json arguments. Uploads the content as filename to the specified host. | None
verify | Should we verify the ssl cert when making an https request? | False
allow_redirects | Follow links. Defaults to False so that you can be explicit about the redirect. | False
timeout | timeout for the request. | 30
proxies | Proxy key value json for http and https | None
