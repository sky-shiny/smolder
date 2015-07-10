Smolder Documentation
=====================

Usage
-----

```
usage: smolder [-h] [--force] host TEST_FILE
```

What it does
------------

It will run tests defined in your test file against a dns or ip address.

It wraps Kenneth Reitz' superb [requests](https://github.com/kennethreitz/requests) python library.
 
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
2. [inputs](inputs.md)
3. [outcomes](outcomes.md)
4. [plugins](plugins.md)
5. [examples](examples.md)
6. [contributing](contributing.md)
7. [history](../HISTORY)
