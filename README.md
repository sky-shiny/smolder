Smolder
=======

"[Requests](https://github.com/kennethreitz/requests) for humans."  :)
[![Build Status](https://travis-ci.org/sky-shiny/smolder.svg?branch=master)](https://travis-ci.org/sky-shiny/smolder)

The prevalence of SOA, microservices and dev/stage/live environment build processes precipitated the development of smolder.
The challenges these technologies pose requires the use of restful api tests which are simple, and repeatable on 
different endpoints without modifying the tests or the endpoints.  A lot of these environments require agents running the
tests to be inside the network boundary and running inside internal build pipelines.  

Smolder aims to solve these problems by providing features such as:

- Smoke test your rest API.
- Validate response times.
- Validate redirects.
- Validate ssl certificates.
- Validate headers.
- Validate json object types using [validictory](https://github.com/jamesturk/validictory)
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

Documentation
=============

1. [tests](docs/tests.md)
    - [inputs](docs/inputs.md)
    - [outcomes](docs/outcomes.md)
2. [plugins](docs/plugins.md)
3. [examples](docs/examples.md)
4. [contributing](docs/contributing.md)
5. [history](HISTORY)

Alternatives
============

1. [Runscope](https://www.runscope.com/)
2. [vrest.io](http://vrest.io)
3. [Stackoverflow](http://stackoverflow.com/questions/12135309/automated-testing-for-rest-api)

Thanks
======

https://github.com/njsaunders

https://github.com/nielsdraaisma

https://github.com/lotia

https://github.com/casibbald
