Smolder Documentation
=====================

Github repo
-----------
[smolder](https://github.com/sky-shiny/smolder)

Demo
----

Copy/paste the following into a bash shell:
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
docker run -v $(pwd)/github_status.yaml:/tmp/smolder.yaml mcameron/smolder status.github.com /tmp/smolder.yaml
```


Usage
-----

```
usage: smolder [-h] [--force] host TEST_FILE
```

Installation
------------

```
git clone git@github.com:sky-shiny/smolder.git.
cd smolder
pip install .
```

What it does
------------

It will run tests defined in your test file against a dns or ip address.

It wraps Kenneth Reitz' [requests](https://github.com/kennethreitz/requests) python library.

It inserts some sane defaults and passes through options from your definition (headers, authentication etc).

It checks the response from the server for expected status-codes/body/header/dpath-json
contents and passes or fails the test based on your definition.

Can be used to specify and pass/fail on performance of api response.

A copy/paste curl equivalent of the request is included in the output for
convenience.

Easily introduced into a CI/CD deploy pipeline.

Without --force, any API requests that are not a GET will be skipped as a safety
mechanism (to ensure you're not overwriting or creating data unconsciously).

1. [tests](tests.md)
    - [inputs](inputs.md)
    - [outcomes](outcomes.md)
2. [plugins](plugins.md)
3. [examples](examples.md)
4. [contributing](contributing.md)
5. [history](../HISTORY)
