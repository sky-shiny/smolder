Smolder
=======

"[Requests](https://github.com/kennethreitz/requests) for humans."  :)
[![Build Status](https://travis-ci.org/sky-shiny/smolder.svg?branch=master)](https://travis-ci.org/sky-shiny/smolder)

The prevalence of SOA, microservices and dev/stage/live environment build processes precipitated the development of smolder.
The challenges these technologies pose requires the use of restful api tests which are simple and repeatable on
different endpoints without modifying the tests or the endpoints.  A lot of these environments require agents running the
tests to be inside the network boundary and running inside internal build pipelines.

Smolder aims to solve these problems by providing features such as:

- Smoke test your rest API.
- Validate response times.
- Validate redirects.
- Validate ssl certificates.
- Validate headers.
- Validate json object types using [validictory](https://github.com/jamesturk/validictory)
- Write plugins using [Yapsy](https://github.com/tibonihoo/yapsy)
- More

Installation
============

```
pip install git+https://github.com/sky-shiny/smolder.git
```

Example
=======

After installing copy/paste the following into a bash shell:
```
cat <<EOF > github_status.yaml
---
tests:
  -
    name: "Github Status"
    outcomes:
      expect_status_code: 301
      response_redirect: "https://status.github.com/api/status.json"
    inputs:
      headers:
        User-Agent: "Smolder smoke test library"
    uri: /api/status.json
  -
    inputs:
      headers:
        User-Agent: "Smolder smoke test library"
    name: "Github Status ssl"
    outcomes:
      response_json_contains:
        status: good
      response_max_time_ms: 200
    port: 443
    protocol: https
    uri: /api/status.json
EOF
smolder status.github.com github_status.yaml
```

Expected Output:
![Output](https://raw.githubusercontent.com/sky-shiny/smolder/master/docs/output.png)

Documentation
=============

[readthedocs](http://smolder.readthedocs.org/en/latest/)

1. [tests](docs/tests.md)
    - [inputs](docs/inputs.md)
    - [outcomes](docs/outcomes.md)
2. [plugins](docs/plugins.md)
3. [examples](docs/examples.md)
4. [contributing](docs/contributing.md)
5. [history](./HISTORY)

Similar Projects
================

1. [Runscope](https://www.runscope.com/)
2. [vrest.io](http://vrest.io)
3. [Stackoverflow](http://stackoverflow.com/questions/12135309/automated-testing-for-rest-api)

Thanks
======

https://github.com/njsaunders

https://github.com/nielsdraaisma

https://github.com/lotia

https://github.com/casibbald
