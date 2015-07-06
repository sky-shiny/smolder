Smolder
=======

"Requests for humans."  :)
[![Build Status](https://travis-ci.org/sky-shiny/smolder.svg)](https://travis-ci.org/sky-shiny/smolder)

- Smoke test your rest API.
- Validate response times.
- Validate redirects.
- Validate ssl certificates.
- Validate headers.
- More

Installation
============

```
pip install git+git://github.com/sky-shiny/smolder.git
```

Example
=======

```
$> smolder status.github.com examples/github_status.json

Success connecting to status.github.com on port 80
Preparing to execute 2 tests

------------------------------- Github Status -------------------------------
                          http://status.github.com:80/
-----------------------------------------------------------------------------

curl -v -s -o /dev/null -H "User-Agent: Smolder smoke test library"  -X GET \
"http://status.github.com:80/"
Request took 227ms
Status code == 301 and redirect == https://status.github.com/ ........ [PASS]

------------------------------- Github Status -------------------------------
                         https://status.github.com:443/
-----------------------------------------------------------------------------

curl -v -s -o /dev/null -H "User-Agent: Smolder smoke test library"  -X GET \
"https://status.github.com:443/"
Request took 541ms
Status code == 200 ................................................... [PASS]
Body contains "All systems operational" .............................. [PASS]
Response time was 341ms longer than 200ms max (541ms) ................ [FAIL]
FOUND 1 FAILURES IN 4 TESTS
```

Example [Readme](https://github.com/sky-shiny/smolder/blob/master/examples/README.md)

Thanks
======

https://github.com/njsaunders

https://github.com/nielsdraaisma

https://github.com/lotia

https://github.com/casibbald
